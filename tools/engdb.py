#!/usr/bin/env python3
"""
engdb.py — Engineering Documentation Database Tool

Validates Markdown documents with YAML front matter and generates
index and traceability reports for the engineering documentation.

Usage:
    python tools/engdb.py validate
    python tools/engdb.py generate
    python tools/engdb.py all
"""

import sys
import os
import re
import argparse
import textwrap
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install PyYAML", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Supported artifact ID prefixes mapped to their human-readable type names
ARTIFACT_TYPES: Dict[str, str] = {
    "REQ": "Requisito",
    "SYS": "Sistema",
    "CMP": "Componente",
    "ADR": "Decisão",
    "DRW": "Desenho",
    "BOM": "Lista de Materiais",
    "SIM": "Simulação",
    "TST": "Teste",
    "VAL": "Validação",
    "DOC": "Documento",
    "MFG": "Fabricação",
    "SUP": "Fornecedor",
}

# Valid artifact ID pattern: PREFIX-NNNN (exactly 4 digits)
ARTIFACT_ID_PATTERN = re.compile(
    r"^(" + "|".join(re.escape(p) for p in ARTIFACT_TYPES) + r")-(\d{4})$"
)

# Front matter fields that may contain references to other artifact IDs
REFERENCE_FIELDS: List[str] = [
    "related",
    "relates_to",
    "requirements",
    "implements",
    "implemented_by",
    "validated_by",
    "verifies",
    "tested_by",
    "tests",
    "components",
    "systems",
    "products",
    "decisions",
    "drawings",
    "bom",
    "simulations",
    "suppliers",
    "affected",
    "depends_on",
    "parent",
    "children",
]

# Fields that must be present in every artifact document
REQUIRED_FIELDS: List[str] = ["id", "title", "status", "revision"]

# Output directory for generated files (relative to repo root)
GENERATED_DIR = Path("docs/_generated")

# Warning banner prepended to all generated files
GENERATED_BANNER = (
    "<!-- ⚠️  ARQUIVO GERADO AUTOMATICAMENTE — NÃO EDITE MANUALMENTE  ⚠️ -->\n"
    "<!-- Regenerado por `python tools/engdb.py generate`."
    " Alterações manuais serão sobrescritas. -->\n\n"
)

# Markdown link pattern:  [label](url)
_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

# URL prefixes that indicate external or non-file links
_EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "//")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


class Artifact:
    """Represents a validated engineering artifact document."""

    def __init__(self, artifact_id: str, path: Path, front_matter: Dict[str, Any]):
        self.id = artifact_id
        self.path = path
        self.front_matter = front_matter

    @property
    def prefix(self) -> str:
        return self.id.split("-")[0]

    @property
    def type_name(self) -> str:
        return ARTIFACT_TYPES.get(self.prefix, "Desconhecido")

    @property
    def title(self) -> str:
        return str(self.front_matter.get("title", "(sem título)"))

    @property
    def status(self) -> str:
        return str(self.front_matter.get("status", ""))

    @property
    def revision(self) -> str:
        return str(self.front_matter.get("revision", ""))

    def get_references(self) -> Dict[str, List[str]]:
        """Return {field_name: [value, ...]} for all reference fields present."""
        result: Dict[str, List[str]] = {}
        for field in REFERENCE_FIELDS:
            val = self.front_matter.get(field)
            if val is None:
                continue
            if isinstance(val, str):
                items: List[str] = [val]
            elif isinstance(val, list):
                items = [str(v) for v in val]
            else:
                items = [str(val)]
            result[field] = items
        return result


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def find_markdown_files(root: Path) -> List[Path]:
    """
    Find all .md files under *root*, excluding:
    - The generated output directory (docs/_generated/)
    - Hidden directories (those starting with '.')
    """
    generated_abs = (root / GENERATED_DIR).resolve()
    result: List[Path] = []

    for path in sorted(root.rglob("*.md")):
        # Exclude generated directory
        try:
            path.resolve().relative_to(generated_abs)
            continue
        except ValueError:
            pass
        # Exclude hidden directories
        parts = path.relative_to(root).parts
        if any(p.startswith(".") for p in parts):
            continue
        result.append(path)

    return result


def parse_front_matter(path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Parse YAML front matter from a Markdown file.

    Returns:
        (data_dict, None)         — successfully parsed front matter
        (None, None)              — file has no front matter
        (None, error_message)     — malformed front matter
    """
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"Cannot read file: {exc}"

    if not content.startswith("---"):
        return None, None

    lines = content.splitlines()
    close_idx: Optional[int] = None
    for i in range(1, len(lines)):
        stripped = lines[i].rstrip()
        if stripped in ("---", "..."):
            close_idx = i
            break

    if close_idx is None:
        return None, "Front matter not closed (missing closing '---')"

    yaml_text = "\n".join(lines[1:close_idx])
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        return None, f"Invalid YAML front matter: {exc}"

    if not isinstance(data, dict):
        return None, "Front matter must be a YAML mapping"

    return data, None


def _extract_body(content: str) -> str:
    """Return the Markdown body text after the front matter block."""
    if not content.startswith("---"):
        return content
    lines = content.splitlines()
    for i in range(1, len(lines)):
        if lines[i].rstrip() in ("---", "..."):
            return "\n".join(lines[i + 1 :])
    return content


def _strip_code_spans(text: str) -> str:
    """
    Remove fenced code blocks and inline code spans from Markdown text
    so that links inside them are not checked.
    """
    # Remove fenced code blocks (``` ... ```)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Remove indented code blocks (4-space / tab prefix lines) — skip line-by-line
    # Remove inline code spans (`...`)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text


# ---------------------------------------------------------------------------
# Loading artifacts
# ---------------------------------------------------------------------------


def _is_artifact_candidate(path: Path, root: Path) -> bool:
    """
    Return True if *path* should be checked for artifact registration.

    Excluded from artifact validation:
    - Files named README.md (section navigation/index files, not artifacts)
    - Files inside the ``templates/`` directory (placeholder documents)
    """
    if path.name.lower() == "readme.md":
        return False
    parts = path.relative_to(root).parts
    if parts and parts[0] == "templates":
        return False
    return True


def load_artifacts(
    files: List[Path], root: Path
) -> Tuple[Dict[str, "Artifact"], List[str]]:
    """
    Scan *files* and collect every engineering artifact.

    An artifact is a Markdown file whose ``id`` front-matter field strictly
    matches the pattern ``PREFIX-NNNN`` (4 digits) for a supported prefix.

    README files and files in the ``templates/`` directory are excluded from
    artifact registration (they serve as navigation/placeholder documents).

    Returns:
        artifacts — dict mapping artifact_id → Artifact
        errors    — list of human-readable error strings
    """
    artifacts: Dict[str, Artifact] = {}
    errors: List[str] = []
    seen_ids: Dict[str, Path] = {}  # id → first file path (for duplicate detection)

    for path in files:
        rel = path.relative_to(root)
        fm, err = parse_front_matter(path)

        if err is not None:
            errors.append(f"{rel}: {err}")
            continue

        if fm is None:
            # No front matter — not an artifact
            continue

        raw_id = fm.get("id")
        if not isinstance(raw_id, str) or not raw_id.strip():
            # No id field, or empty — not a managed artifact
            continue

        artifact_id = raw_id.strip()
        prefix = artifact_id.split("-")[0] if "-" in artifact_id else ""

        # Only process IDs whose prefix is in our supported list
        if prefix not in ARTIFACT_TYPES:
            continue

        # README and template files are excluded from artifact validation.
        # Their IDs use the prefix as a namespace (e.g. BOM-README) rather
        # than as an artifact identifier, so we skip them silently.
        if not _is_artifact_candidate(path, root):
            continue

        # Validate ID format (PREFIX-NNNN) for non-excluded files
        if not ARTIFACT_ID_PATTERN.match(artifact_id):
            errors.append(
                f"{rel}: ID '{artifact_id}' has invalid format — "
                f"expected {prefix}-NNNN with exactly 4 digits (e.g. {prefix}-0001)"
            )
            continue

        # Duplicate ID detection
        if artifact_id in seen_ids:
            errors.append(
                f"{rel}: Duplicate ID '{artifact_id}' "
                f"(already defined in {seen_ids[artifact_id]})"
            )
            continue

        # Missing required fields
        missing = [f for f in REQUIRED_FIELDS if f not in fm]
        if missing:
            errors.append(
                f"{rel}: Missing required field(s): {', '.join(missing)} "
                f"(id={artifact_id})"
            )
            # Still register the artifact so cross-reference checks work

        seen_ids[artifact_id] = rel
        artifacts[artifact_id] = Artifact(artifact_id, path, fm)

    return artifacts, errors


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def validate_references(
    artifacts: Dict[str, Artifact], root: Path
) -> List[str]:
    """
    For every artifact, inspect all reference fields and verify that any
    value matching the artifact ID pattern actually refers to a known artifact.
    Also catches self-references.
    """
    errors: List[str] = []

    for artifact in artifacts.values():
        rel = artifact.path.relative_to(root)
        for field, values in artifact.get_references().items():
            for raw_val in values:
                val = str(raw_val).strip()
                # Only validate values that look like artifact IDs
                if not ARTIFACT_ID_PATTERN.match(val):
                    continue
                # Self-reference check
                if val == artifact.id:
                    errors.append(
                        f"{rel}: Self-reference in field '{field}': '{val}'"
                    )
                    continue
                # Referenced artifact must exist
                if val not in artifacts:
                    errors.append(
                        f"{rel}: Reference to non-existent artifact '{val}' "
                        f"in field '{field}'"
                    )

    return errors


def check_broken_links(path: Path, root: Path) -> List[str]:
    """
    Scan the Markdown body of *path* for local hyperlinks and report
    any whose target file does not exist on disk.

    Links in fenced code blocks and inline code spans are ignored.
    External URLs (http, https, mailto, …) and pure anchors (#) are ignored.
    """
    errors: List[str] = []

    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return errors

    body = _extract_body(content)
    body = _strip_code_spans(body)
    rel = path.relative_to(root)

    for match in _LINK_RE.finditer(body):
        url = match.group(2).strip()

        # Skip external links and pure anchors
        if any(url.startswith(prefix) for prefix in _EXTERNAL_PREFIXES):
            continue
        if url.startswith("#"):
            continue

        # Strip fragment identifier
        url_no_fragment = url.split("#")[0]
        if not url_no_fragment:
            continue

        # Resolve target path
        if url_no_fragment.startswith("/"):
            target = root / url_no_fragment.lstrip("/")
        else:
            target = path.parent / url_no_fragment

        try:
            target_resolved = target.resolve()
        except OSError:
            errors.append(f"{rel}: Broken link '{url}' (cannot resolve path)")
            continue

        if not target_resolved.exists():
            errors.append(f"{rel}: Broken link '{url}' (file not found)")

    return errors


# ---------------------------------------------------------------------------
# validate command
# ---------------------------------------------------------------------------


def run_validate(root: Path) -> int:
    """
    Run all validation checks against the repository.

    Exit codes:
        0 — all checks passed
        1 — one or more errors found
    """
    print("🔍  Scanning for Markdown files…")
    files = find_markdown_files(root)
    print(f"    Found {len(files)} Markdown file(s)")

    print("\n📋  Loading artifacts…")
    artifacts, load_errors = load_artifacts(files, root)
    print(f"    Found {len(artifacts)} artifact(s)")

    print("\n🔗  Validating cross-references…")
    ref_errors = validate_references(artifacts, root)

    print("\n🔗  Checking local links in artifact files…")
    link_errors: List[str] = []
    for artifact in artifacts.values():
        link_errors.extend(check_broken_links(artifact.path, root))

    all_errors = load_errors + ref_errors + link_errors

    if all_errors:
        print(f"\n❌  Validation failed — {len(all_errors)} error(s):\n")
        for err in all_errors:
            print(f"  • {err}")
        return 1

    print(f"\n✅  Validation passed — {len(artifacts)} artifact(s), no errors found")
    return 0


# ---------------------------------------------------------------------------
# Generation helpers
# ---------------------------------------------------------------------------


def _rel_link(from_dir: Path, to_path: Path) -> str:
    """Compute a forward-slash relative path from *from_dir* to *to_path*."""
    try:
        rel = os.path.relpath(to_path, from_dir)
    except ValueError:
        rel = str(to_path)
    return rel.replace("\\", "/")


def _generate_artifact_index(
    artifacts: Dict[str, Artifact], root: Path, output_dir: Path
) -> str:
    """Return the full text content for ARTIFACT_INDEX.md."""
    rows: List[str] = []
    for art in sorted(artifacts.values(), key=lambda a: a.id):
        link = _rel_link(output_dir, art.path)
        rel_path = str(art.path.relative_to(root)).replace("\\", "/")
        rows.append(
            f"| {art.id} | {art.title} | {art.type_name} | "
            f"{art.status} | {art.revision} | [{rel_path}]({link}) |"
        )

    table = "\n".join(rows) if rows else "| (nenhum artefato encontrado) | | | | | |"

    return (
        GENERATED_BANNER
        + "# Índice de Artefatos\n\n"
        + "| ID | Título | Tipo | Status | Revisão | Link |\n"
        + "|----|--------|------|--------|---------|------|\n"
        + table
        + "\n"
    )


def _generate_traceability(artifacts: Dict[str, Artifact]) -> str:
    """Return the full text content for TRACEABILITY.md."""
    outgoing_rows: List[str] = []
    incoming: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

    for art in sorted(artifacts.values(), key=lambda a: a.id):
        for field, values in art.get_references().items():
            for val in values:
                val = str(val).strip()
                if ARTIFACT_ID_PATTERN.match(val):
                    outgoing_rows.append(f"| {art.id} | `{field}` | {val} |")
                    incoming[val].append((art.id, field))

    outgoing_table = (
        "\n".join(outgoing_rows)
        if outgoing_rows
        else "| (nenhuma relação encontrada) | | |"
    )

    incoming_rows: List[str] = []
    for art_id in sorted(artifacts.keys()):
        refs = incoming.get(art_id, [])
        if refs:
            sources = ", ".join(
                f"{src} (`{fld}`)" for src, fld in sorted(refs)
            )
        else:
            sources = "—"
        title = artifacts[art_id].title
        incoming_rows.append(f"| {art_id} | {title} | {sources} |")

    incoming_table = (
        "\n".join(incoming_rows) if incoming_rows else "| (nenhum artefato) | | |"
    )

    return (
        GENERATED_BANNER
        + "# Matriz de Rastreabilidade\n\n"
        + "## Relações de Origem → Destino\n\n"
        + "| Origem | Tipo de Relação | Destino |\n"
        + "|--------|----------------|----------|\n"
        + outgoing_table
        + "\n\n"
        + "---\n\n"
        + "## Referências Recebidas por Artefato\n\n"
        + "| Artefato | Título | Referenciado por |\n"
        + "|----------|--------|------------------|\n"
        + incoming_table
        + "\n"
    )


def _generate_dashboard(artifacts: Dict[str, Artifact]) -> str:
    """Return the full text content for DASHBOARD.md."""
    total = len(artifacts)

    by_type: Dict[str, int] = defaultdict(int)
    by_status: Dict[str, int] = defaultdict(int)
    for art in artifacts.values():
        by_type[art.prefix] += 1
        by_status[art.status or "(sem status)"] += 1

    type_rows = "\n".join(
        f"| {prefix} | {ARTIFACT_TYPES[prefix]} | {count} |"
        for prefix, count in sorted(by_type.items())
    ) or "| — | — | 0 |"

    status_rows = "\n".join(
        f"| {status} | {count} |"
        for status, count in sorted(by_status.items())
    ) or "| — | 0 |"

    return (
        GENERATED_BANNER
        + "# Dashboard de Engenharia\n\n"
        + f"## Total de Artefatos: **{total}**\n\n"
        + "---\n\n"
        + "## Por Tipo\n\n"
        + "| Prefixo | Tipo | Quantidade |\n"
        + "|---------|------|------------|\n"
        + type_rows
        + "\n\n"
        + "---\n\n"
        + "## Por Status\n\n"
        + "| Status | Quantidade |\n"
        + "|--------|------------|\n"
        + status_rows
        + "\n\n"
        + "---\n\n"
        + "## Relatórios Gerados\n\n"
        + "| Relatório | Link |\n"
        + "|-----------|------|\n"
        + "| Índice de Artefatos | [ARTIFACT_INDEX.md](./ARTIFACT_INDEX.md) |\n"
        + "| Matriz de Rastreabilidade | [TRACEABILITY.md](./TRACEABILITY.md) |\n"
        + "| Dashboard | [DASHBOARD.md](./DASHBOARD.md) |\n"
    )


# ---------------------------------------------------------------------------
# generate command
# ---------------------------------------------------------------------------


def run_generate(root: Path) -> int:
    """
    Generate all report files under docs/_generated/.

    Files are written only when their content has changed to avoid
    unnecessary commits.

    Returns 0 on success.
    """
    print("📂  Scanning for artifacts…")
    files = find_markdown_files(root)
    artifacts, load_errors = load_artifacts(files, root)

    if load_errors:
        print(
            f"⚠️   {len(load_errors)} loading error(s) detected "
            "— some artifacts may be absent from the reports:"
        )
        for err in load_errors:
            print(f"  • {err}")

    print(f"    Found {len(artifacts)} artifact(s)")

    out_dir = root / GENERATED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    reports = {
        "ARTIFACT_INDEX.md": _generate_artifact_index(artifacts, root, out_dir),
        "TRACEABILITY.md": _generate_traceability(artifacts),
        "DASHBOARD.md": _generate_dashboard(artifacts),
    }

    changed = False
    for filename, content in reports.items():
        out_path = out_dir / filename
        existing = out_path.read_text(encoding="utf-8") if out_path.exists() else None
        if existing != content:
            out_path.write_text(content, encoding="utf-8")
            print(f"✅  Generated: {out_path.relative_to(root)}")
            changed = True
        else:
            print(f"⏭️   No changes: {out_path.relative_to(root)}")

    if changed:
        print(f"\n✅  Reports written to {GENERATED_DIR}/")
    else:
        print("\n✅  All generated files are up to date — no changes written")

    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="engdb.py",
        description="Engineering Documentation Database Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            commands:
              validate   Validate all Markdown documents
              generate   Generate index and traceability reports
              all        Run validate, then generate (fails fast on errors)

            The tool scans all .md files in the repository (excluding docs/_generated/).
            Only files with IDs matching a supported artifact prefix are processed as
            artifacts. See ARTIFACT_TYPES in the source for the full list.
            """
        ),
    )
    parser.add_argument(
        "command",
        choices=["validate", "generate", "all"],
        help="Command to run",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help=(
            "Repository root directory. "
            "Defaults to the parent of the directory containing this script."
        ),
    )

    args = parser.parse_args()

    # Determine repo root: parent of tools/ directory
    if args.root is not None:
        root = args.root.resolve()
    else:
        root = Path(__file__).resolve().parent.parent

    if not root.is_dir():
        print(f"ERROR: Root directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"📁  Repository root: {root}\n")

    if args.command == "validate":
        sys.exit(run_validate(root))
    elif args.command == "generate":
        sys.exit(run_generate(root))
    elif args.command == "all":
        rc = run_validate(root)
        if rc != 0:
            sys.exit(rc)
        print()
        sys.exit(run_generate(root))


if __name__ == "__main__":
    main()
