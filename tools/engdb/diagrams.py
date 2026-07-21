"""
tools/engdb/diagrams.py

Generates Mermaid diagrams from engineering database metadata.

Reads all Markdown files with YAML front matter from the repository,
extracts metadata (id, title, type, status, revision, related) and
produces deterministic Mermaid diagram files under docs/_generated/.

Rules:
- Never modify manually written documentation.
- Diagrams are fully regenerated on every run.
- Output is deterministic (sorted).
- No duplicate nodes or edges.
- Node IDs use the document ID; labels use the title.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GENERATED_DIR = "docs/_generated"

# Mapping from ID prefix to artifact type name
PREFIX_TYPE: dict[str, str] = {
    "REQ": "requirement",
    "ADR": "decision",
    "COMP": "component",
    "TEST": "test",
    "SIM": "simulation",
    "BOM": "bom",
    "DRW": "drawing",
    "SUP": "supplier",
    "MFG": "manufacturing",
    "ECO": "engineering_change",
    "JRN": "journal",
    "PROD": "product",
    "UTV": "utv_system",
    "VAL": "validation",
}

# Directories to skip entirely (not engineering artefacts)
SKIP_DIRS = {
    ".git",
    "docs/_generated",
    "node_modules",
    ".github",
    "assets",
}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


class Document:
    """Represents a single engineering document parsed from a Markdown file."""

    __slots__ = (
        "path",
        "id",
        "title",
        "artifact_type",
        "status",
        "revision",
        "related",
        "tags",
    )

    def __init__(
        self,
        path: str,
        doc_id: str,
        title: str,
        artifact_type: str,
        status: str,
        revision: str,
        related: list[str],
        tags: list[str],
    ) -> None:
        self.path = path
        self.id = doc_id
        self.title = title
        self.artifact_type = artifact_type
        self.status = status
        self.revision = revision
        self.related = related
        self.tags = tags

    def node_id(self) -> str:
        """Return a Mermaid-safe node identifier (alphanumeric + underscores)."""
        return re.sub(r"[^A-Za-z0-9_]", "_", self.id)

    def label(self) -> str:
        """Return a Mermaid-safe label string (double-quoted)."""
        safe = self.title.replace('"', "'")
        return f'"{self.id}<br/>{safe}"'

    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, type={self.artifact_type!r})"


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def _detect_type(doc_id: str, file_path: str = "") -> str:
    """Infer artifact type from the ID prefix and optionally the file path."""
    prefix = doc_id.split("-")[0].upper()
    artifact_type = PREFIX_TYPE.get(prefix, "other")
    # Disambiguate COMP- prefix: company/ directory docs are not components.
    if artifact_type == "component" and (
        file_path.startswith("company/") or "/company/" in file_path
    ):
        artifact_type = "company"
    return artifact_type


def _parse_front_matter(text: str) -> Optional[dict]:
    """Extract YAML front matter from a Markdown file string."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    yaml_block = text[3:end].strip()
    try:
        return yaml.safe_load(yaml_block)
    except yaml.YAMLError:
        return None


def load_documents(repo_root: str) -> list[Document]:
    """Walk *repo_root* and return all Documents with valid front matter."""
    root = Path(repo_root)
    docs: list[Document] = []
    seen_ids: set[str] = set()

    for md_file in sorted(root.rglob("*.md")):
        # Skip hidden / generated / dependency directories
        parts = set(md_file.relative_to(root).parts)
        if parts & SKIP_DIRS:
            continue
        # Skip template files (they contain placeholder IDs like PREFIXO-XXXX)
        if "templates" in md_file.relative_to(root).parts:
            continue

        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        fm = _parse_front_matter(text)
        if not fm:
            continue

        doc_id = str(fm.get("id", "")).strip()
        title = str(fm.get("title", "")).strip()
        if not doc_id or not title:
            continue
        if doc_id in seen_ids:
            continue
        seen_ids.add(doc_id)

        related_raw = fm.get("related", []) or []
        related = [str(r).strip() for r in related_raw if r]

        tags_raw = fm.get("tags", []) or []
        tags = [str(t).strip() for t in tags_raw if t]

        docs.append(
            Document(
                path=str(md_file.relative_to(root)),
                doc_id=doc_id,
                title=title,
                artifact_type=_detect_type(doc_id, str(md_file.relative_to(root))),
                status=str(fm.get("status", "")).strip(),
                revision=str(fm.get("revision", "")).strip(),
                related=related,
                tags=tags,
            )
        )

    return docs


# ---------------------------------------------------------------------------
# Helpers for building edge sets
# ---------------------------------------------------------------------------


def _id_index(docs: list[Document]) -> dict[str, Document]:
    return {d.id: d for d in docs}


def _edges_by_type(
    docs: list[Document],
    source_types: set[str],
    target_types: set[str],
    id_map: dict[str, Document],
) -> list[tuple[Document, Document]]:
    """
    Return sorted unique edges (source → target) where source is in
    *source_types*, and target ID is resolvable to a document in *target_types*.
    """
    edges: set[tuple[str, str]] = set()
    for doc in docs:
        if doc.artifact_type not in source_types:
            continue
        for rel in doc.related:
            # related entries are file paths like /requirements/REQ-0001.md
            # or bare IDs; try to extract an ID from the basename
            target_id = _extract_id_from_ref(rel, id_map)
            if target_id and target_id in id_map:
                target_doc = id_map[target_id]
                if target_doc.artifact_type in target_types:
                    edges.add((doc.id, target_id))
    result = []
    for src_id, tgt_id in sorted(edges):
        result.append((id_map[src_id], id_map[tgt_id]))
    return result


def _extract_id_from_ref(ref: str, id_map: dict[str, Document]) -> Optional[str]:
    """
    Try to resolve a 'related' reference to a known document ID.

    Handles:
    - Bare IDs: "REQ-0001"
    - File paths: "/requirements/REQ-0001.md" → try stem
    """
    ref = ref.strip()
    # Direct ID match
    if ref in id_map:
        return ref
    # Extract stem from path
    stem = Path(ref).stem
    if stem in id_map:
        return stem
    # Try stripping leading slash and matching
    bare = ref.lstrip("/")
    if bare in id_map:
        return bare
    return None


def _node_block(doc: Document) -> str:
    return f'    {doc.node_id()}[{doc.label()}]'


# ---------------------------------------------------------------------------
# Diagram generators
# ---------------------------------------------------------------------------

_HEADER = """\
---
title: {title}
id: {file_id}
status: generated
revision: "auto"
owner: automation
created: "{date}"
updated: "{date}"
tags: [generated, diagram, mermaid]
---

# {title}

> ⚠️ **Arquivo gerado automaticamente.** Não edite manualmente.

"""


def _make_header(title: str, file_id: str, date: str) -> str:
    return _HEADER.format(title=title, file_id=file_id, date=date)


# 1. System Map ---------------------------------------------------------------


def generate_system_map(docs: list[Document], date: str) -> str:
    """
    Flowchart: Company → Product → UTV → Systems → Subcomponents.
    """
    lines: list[str] = []
    lines.append(_make_header("System Map", "GEN-SYSTEM-MAP", date))
    lines.append("```mermaid")
    lines.append("flowchart TD")

    id_map = _id_index(docs)

    company_docs = [d for d in docs if d.artifact_type == "other" and "company" in d.tags]
    product_docs = [d for d in docs if d.artifact_type == "product"]
    # Find the main UTV product document directly by ID
    utv_main = next((d for d in docs if d.id == "PROD-UTV-001"), None)
    # Systems: UTV sub-system docs (id starts with UTV-)
    system_docs = [d for d in docs if d.id.startswith("UTV-") and "system" in d.tags]
    # Subcomponents: COMP-*
    comp_docs = [d for d in docs if d.artifact_type == "component"]

    # Static top-level nodes
    lines.append('    COMPANY["🏢 Empresa"]')
    lines.append('    STARTUP["UTV Startup"]')
    lines.append("    COMPANY --> STARTUP")

    # Products
    for p in sorted(product_docs, key=lambda d: d.id):
        lines.append(f"    STARTUP --> {p.node_id()}[{p.label()}]")

    # If PROD-UTV-001 is not in product_docs, add it directly
    if utv_main and utv_main not in product_docs:
        lines.append(f"    STARTUP --> {utv_main.node_id()}[{utv_main.label()}]")

    # Systems connected to UTV product
    utv_parent_id = utv_main.node_id() if utv_main else "STARTUP"
    for s in sorted(system_docs, key=lambda d: d.id):
        lines.append(f"    {utv_parent_id} --> {s.node_id()}[{s.label()}]")

    # Components connected to systems if related, else to a generic COMP node
    added_comp_node = False
    for c in sorted(comp_docs, key=lambda d: d.id):
        # Resolve all related references once
        resolved_ids = {
            _extract_id_from_ref(r, id_map)
            for r in c.related
            if _extract_id_from_ref(r, id_map) is not None
        }
        connected = False
        for s in system_docs:
            if s.id in resolved_ids:
                lines.append(f"    {s.node_id()} --> {c.node_id()}[{c.label()}]")
                connected = True
                break
        if not connected:
            if not added_comp_node:
                if utv_main:
                    lines.append(f'    {utv_main.node_id()} --> COMP_LIB["🔩 Biblioteca de Componentes"]')
                else:
                    lines.append('    STARTUP --> COMP_LIB["🔩 Biblioteca de Componentes"]')
                added_comp_node = True
            lines.append(f"    COMP_LIB --> {c.node_id()}[{c.label()}]")

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# 2. Product Breakdown Structure -----------------------------------------------


def generate_product_breakdown(docs: list[Document], date: str) -> str:
    """
    Hierarchical tree: Product → Systems → Subsystems → Components.
    """
    lines: list[str] = []
    lines.append(_make_header("Product Breakdown Structure (PBS)", "GEN-PBS", date))
    lines.append("```mermaid")
    lines.append("graph TD")

    product_docs = [d for d in docs if d.artifact_type == "product" and d.id.startswith("PROD")]
    system_docs = [d for d in docs if d.id.startswith("UTV-") and "system" in d.tags]
    comp_docs = [d for d in docs if d.artifact_type == "component"]

    lines.append('    PROD_ROOT["📦 Produto"]')

    # Only connect the main UTV product (PROD-UTV-001) and its systems to avoid clutter
    utv_main = next((d for d in product_docs if d.id == "PROD-UTV-001"), None)
    other_products = [d for d in product_docs if d.id != "PROD-UTV-001"]

    for p in sorted(other_products, key=lambda d: d.id):
        lines.append(f"    PROD_ROOT --> {p.node_id()}[{p.label()}]")

    if utv_main:
        lines.append(f"    PROD_ROOT --> {utv_main.node_id()}[{utv_main.label()}]")
        for s in sorted(system_docs, key=lambda d: d.id):
            lines.append(f"    {utv_main.node_id()} --> {s.node_id()}[{s.label()}]")

    if not utv_main and not other_products:
        for s in sorted(system_docs, key=lambda d: d.id):
            lines.append(f"    PROD_ROOT --> {s.node_id()}[{s.label()}]")

    for c in sorted(comp_docs, key=lambda d: d.id):
        lines.append(f'    COMP_LIB["🔩 Componentes"] --> {c.node_id()}[{c.label()}]')

    if comp_docs:
        if utv_main:
            lines.append(f'    {utv_main.node_id()} --> COMP_LIB["🔩 Componentes"]')
        elif other_products:
            for p in sorted(other_products, key=lambda d: d.id):
                lines.append(f'    {p.node_id()} --> COMP_LIB["🔩 Componentes"]')
        else:
            lines.append('    PROD_ROOT --> COMP_LIB["🔩 Componentes"]')

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# 3. Requirements Traceability Graph -------------------------------------------


def generate_requirements_graph(docs: list[Document], date: str) -> str:
    """
    Graph: REQ → SYS → CMP → DRW → SIM → TST → VAL → MFG.
    """
    lines: list[str] = []
    lines.append(_make_header("Requirements Traceability Graph", "GEN-REQ-GRAPH", date))
    lines.append("```mermaid")
    lines.append("flowchart LR")

    id_map = _id_index(docs)
    type_buckets: dict[str, list[Document]] = {}
    for d in docs:
        type_buckets.setdefault(d.artifact_type, []).append(d)

    ordered_types = [
        ("requirement", "📋 REQ"),
        ("utv_system", "🏗️ SYS"),
        ("component", "🔩 CMP"),
        ("drawing", "📐 DRW"),
        ("simulation", "🖥️ SIM"),
        ("test", "🧪 TST"),
        ("validation", "✅ VAL"),
        ("manufacturing", "🏭 MFG"),
    ]

    # Emit nodes per type (subgraph per layer)
    for type_key, label in ordered_types:
        bucket = sorted(type_buckets.get(type_key, []), key=lambda d: d.id)
        if bucket:
            lines.append(f'    subgraph SG_{type_key.upper()}["{label}"]')
            for d in bucket:
                lines.append(f"        {d.node_id()}[{d.label()}]")
            lines.append("    end")

    # Emit edges based on 'related' cross-references
    edges: set[tuple[str, str]] = set()
    for doc in docs:
        for rel in doc.related:
            target_id = _extract_id_from_ref(rel, id_map)
            if target_id and target_id in id_map and target_id != doc.id:
                edges.add((doc.id, target_id))

    for src_id, tgt_id in sorted(edges):
        if src_id in id_map and tgt_id in id_map:
            src = id_map[src_id]
            tgt = id_map[tgt_id]
            lines.append(f"    {src.node_id()} --> {tgt.node_id()}")

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# 4. Architecture Decision Graph -----------------------------------------------


def generate_adr_graph(docs: list[Document], date: str) -> str:
    """
    ADR → Components → Requirements → Systems.
    """
    lines: list[str] = []
    lines.append(_make_header("Architecture Decision Graph", "GEN-ADR-GRAPH", date))
    lines.append("```mermaid")
    lines.append("flowchart TD")

    id_map = _id_index(docs)
    adr_docs = sorted([d for d in docs if d.artifact_type == "decision" and d.id.startswith("ADR-")], key=lambda d: d.id)

    if not adr_docs:
        lines.append('    NO_ADR["Nenhum ADR encontrado"]')
    else:
        for adr in adr_docs:
            lines.append(f"    {adr.node_id()}[{adr.label()}]")

        edges: set[tuple[str, str]] = set()
        for adr in adr_docs:
            for rel in adr.related:
                target_id = _extract_id_from_ref(rel, id_map)
                if target_id and target_id in id_map and target_id != adr.id:
                    edges.add((adr.id, target_id))

        for src_id, tgt_id in sorted(edges):
            if src_id in id_map and tgt_id in id_map:
                src = id_map[src_id]
                tgt = id_map[tgt_id]
                lines.append(f"    {tgt.node_id()}[{tgt.label()}]")
                lines.append(f"    {src.node_id()} --> {tgt.node_id()}")

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# 5. Component Dependency Graph ------------------------------------------------


def generate_component_dependencies(docs: list[Document], date: str) -> str:
    """
    Dependencies between components.
    """
    lines: list[str] = []
    lines.append(_make_header("Component Dependency Graph", "GEN-COMP-DEP", date))
    lines.append("```mermaid")
    lines.append("graph LR")

    id_map = _id_index(docs)
    comp_docs = sorted([d for d in docs if d.artifact_type == "component"], key=lambda d: d.id)

    if not comp_docs:
        lines.append('    NO_COMP["Nenhum componente encontrado"]')
    else:
        for c in comp_docs:
            lines.append(f"    {c.node_id()}[{c.label()}]")

        edges: set[tuple[str, str]] = set()
        for c in comp_docs:
            for rel in c.related:
                target_id = _extract_id_from_ref(rel, id_map)
                if target_id and target_id in id_map:
                    target = id_map[target_id]
                    if target.artifact_type == "component" and target_id != c.id:
                        edges.add((c.id, target_id))

        if edges:
            for src_id, tgt_id in sorted(edges):
                lines.append(f"    {id_map[src_id].node_id()} --> {id_map[tgt_id].node_id()}")
        else:
            lines.append('    COMP_NOTE["Componentes sem dependências cruzadas definidas"]')

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# 6. BOM Tree ------------------------------------------------------------------


def generate_bom_tree(docs: list[Document], date: str) -> str:
    """
    BOM tree.
    """
    lines: list[str] = []
    lines.append(_make_header("BOM Tree", "GEN-BOM-TREE", date))
    lines.append("```mermaid")
    lines.append("graph TD")

    id_map = _id_index(docs)
    bom_docs = sorted([d for d in docs if d.artifact_type == "bom"], key=lambda d: d.id)
    comp_docs = sorted([d for d in docs if d.artifact_type == "component"], key=lambda d: d.id)
    product_docs = sorted(
        [d for d in docs if d.artifact_type in ("product", "utv_system") and d.id.startswith("PROD")],
        key=lambda d: d.id,
    )

    lines.append('    BOM_ROOT["📋 BOM — Bill of Materials"]')

    for p in product_docs:
        lines.append(f"    BOM_ROOT --> {p.node_id()}[{p.label()}]")

    for b in bom_docs:
        lines.append(f"    BOM_ROOT --> {b.node_id()}[{b.label()}]")

    for c in comp_docs:
        lines.append(f'    COMP_GROUP["🔩 Componentes"] --> {c.node_id()}[{c.label()}]')

    if comp_docs:
        if bom_docs:
            for b in bom_docs:
                lines.append(f'    {b.node_id()} --> COMP_GROUP["🔩 Componentes"]')
        elif product_docs:
            for p in product_docs:
                lines.append(f'    {p.node_id()} --> COMP_GROUP["🔩 Componentes"]')
        else:
            lines.append('    BOM_ROOT --> COMP_GROUP["🔩 Componentes"]')

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# 7. Validation Graph ----------------------------------------------------------


def generate_validation_flow(docs: list[Document], date: str) -> str:
    """
    Requisito → Projeto → Simulação → Teste → Validação.
    """
    lines: list[str] = []
    lines.append(_make_header("Validation Flow", "GEN-VAL-FLOW", date))
    lines.append("```mermaid")
    lines.append("flowchart LR")

    id_map = _id_index(docs)

    req_docs = sorted([d for d in docs if d.artifact_type == "requirement"], key=lambda d: d.id)
    sim_docs = sorted([d for d in docs if d.artifact_type == "simulation"], key=lambda d: d.id)
    test_docs = sorted([d for d in docs if d.artifact_type == "test"], key=lambda d: d.id)
    val_docs = sorted([d for d in docs if d.artifact_type == "validation"], key=lambda d: d.id)

    # Static flow backbone
    lines.append('    REQ_STAGE["📋 Requisito"]')
    lines.append('    DESIGN_STAGE["🏗️ Projeto"]')
    lines.append('    SIM_STAGE["🖥️ Simulação"]')
    lines.append('    TEST_STAGE["🧪 Teste"]')
    lines.append('    VAL_STAGE["✅ Validação"]')
    lines.append("    REQ_STAGE --> DESIGN_STAGE")
    lines.append("    DESIGN_STAGE --> SIM_STAGE")
    lines.append("    SIM_STAGE --> TEST_STAGE")
    lines.append("    TEST_STAGE --> VAL_STAGE")

    for d in req_docs:
        lines.append(f"    {d.node_id()}[{d.label()}] --> REQ_STAGE")
    for d in sim_docs:
        lines.append(f"    SIM_STAGE --> {d.node_id()}[{d.label()}]")
    for d in test_docs:
        lines.append(f"    TEST_STAGE --> {d.node_id()}[{d.label()}]")
    for d in val_docs:
        lines.append(f"    VAL_STAGE --> {d.node_id()}[{d.label()}]")

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# 8. Project Roadmap -----------------------------------------------------------


def generate_project_roadmap(docs: list[Document], date: str) -> str:
    """
    Gantt chart built from milestone/release metadata, falling back to
    a static skeleton when no dedicated milestone docs are present.
    """
    lines: list[str] = []
    lines.append(_make_header("Project Roadmap", "GEN-ROADMAP", date))
    lines.append("```mermaid")
    lines.append("gantt")
    lines.append("    title Roadmap — UTV Startup")
    lines.append("    dateFormat  YYYY-MM")
    lines.append("    section Fundação")
    lines.append("    Estrutura do repositório          :done,    rep,  2026-07, 2026-08")
    lines.append("    Definição de requisitos UTV       :active,  req,  2026-08, 2026-10")
    lines.append("    Arquitetura do sistema            :         arch, 2026-10, 2026-12")
    lines.append("    section Engenharia Conceitual")
    lines.append("    CAD conceitual — Chassis          :         cad1, 2027-01, 2027-04")
    lines.append("    CAD conceitual — Suspensão        :         cad2, 2027-03, 2027-06")
    lines.append("    BOM inicial                       :         bom1, 2027-04, 2027-06")
    lines.append("    section Prototipagem")
    lines.append("    Protótipo #1 — Chassis            :         prt1, 2027-07, 2027-12")
    lines.append("    Testes estruturais iniciais       :         tst1, 2027-10, 2028-02")
    lines.append("    section Validação")
    lines.append("    Protótipo #2 — Sistema completo   :         prt2, 2028-01, 2028-06")
    lines.append("    Campanha de testes                :         tst2, 2028-06, 2028-12")
    lines.append("    section Homologação")
    lines.append("    Processo DENATRAN/INMETRO         :         hom,  2029-01, 2029-12")
    lines.append("    section Comercialização")
    lines.append("    Lançamento UTV v1.0               :         launch, 2030-01, 2030-06")
    lines.append("```")
    lines.append("")

    # Append a table of active requirements as release milestones
    req_docs = sorted([d for d in docs if d.artifact_type == "requirement"], key=lambda d: d.id)
    if req_docs:
        lines.append("## Requisitos Ativos")
        lines.append("")
        lines.append("| ID | Título | Status | Revisão |")
        lines.append("|----|--------|--------|---------|")
        for d in req_docs:
            lines.append(f"| {d.id} | {d.title} | {d.status} | {d.revision} |")
        lines.append("")

    return "\n".join(lines)


# 9. Engineering Workflow ------------------------------------------------------


def generate_engineering_workflow(docs: list[Document], date: str) -> str:
    """
    Static engineering workflow:
    Necessidade → Requisitos → Arquitetura → Projeto → CAD →
    BOM → Simulação → Protótipo → Teste → Validação → Produção.
    """
    lines: list[str] = []
    lines.append(_make_header("Engineering Workflow", "GEN-ENG-WORKFLOW", date))
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append('    NEED["💡 Necessidade"]')
    lines.append('    REQ_S["📋 Requisitos"]')
    lines.append('    ARCH_S["🏗️ Arquitetura"]')
    lines.append('    DESIGN_S["✏️ Projeto"]')
    lines.append('    CAD_S["🖥️ CAD"]')
    lines.append('    BOM_S["📦 BOM"]')
    lines.append('    SIM_S["🔬 Simulação"]')
    lines.append('    PROTO_S["🔧 Protótipo"]')
    lines.append('    TEST_S["🧪 Teste"]')
    lines.append('    VAL_S["✅ Validação"]')
    lines.append('    PROD_S["🏭 Produção"]')
    lines.append("    NEED --> REQ_S")
    lines.append("    REQ_S --> ARCH_S")
    lines.append("    ARCH_S --> DESIGN_S")
    lines.append("    DESIGN_S --> CAD_S")
    lines.append("    CAD_S --> BOM_S")
    lines.append("    BOM_S --> SIM_S")
    lines.append("    SIM_S --> PROTO_S")
    lines.append("    PROTO_S --> TEST_S")
    lines.append("    TEST_S --> VAL_S")
    lines.append("    VAL_S --> PROD_S")
    lines.append("    VAL_S -->|Não conforme| REQ_S")
    lines.append("```")
    lines.append("")

    # Annotation table
    id_map = _id_index(docs)
    all_types = [
        ("requirement", "📋 Requisitos", "requirements/"),
        ("simulation", "🖥️ Simulações", "simulations/"),
        ("test", "🧪 Testes", "tests/"),
        ("validation", "✅ Validações", "validation/"),
        ("manufacturing", "🏭 Fabricação", "manufacturing/"),
    ]
    for type_key, label, _ in all_types:
        bucket = sorted([d for d in docs if d.artifact_type == type_key], key=lambda d: d.id)
        if bucket:
            lines.append(f"## {label}")
            lines.append("")
            lines.append("| ID | Título | Status |")
            lines.append("|----|--------|--------|")
            for d in bucket:
                lines.append(f"| {d.id} | {d.title} | {d.status} |")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


_DIAGRAMS = [
    ("system-map.md", "🗺️ System Map", "Mapa do sistema: Empresa → Produto → UTV → Sistemas → Componentes"),
    ("product-breakdown.md", "📦 Product Breakdown Structure (PBS)", "Árvore hierárquica do produto"),
    ("requirements-graph.md", "📋 Requirements Traceability Graph", "Grafo de rastreabilidade: REQ → SYS → CMP → DRW → SIM → TST → VAL → MFG"),
    ("adr-graph.md", "🧠 Architecture Decision Graph", "ADR e seus relacionamentos com componentes, requisitos e sistemas"),
    ("component-dependencies.md", "🔩 Component Dependency Graph", "Dependências entre componentes"),
    ("bom-tree.md", "📦 BOM Tree", "Árvore da lista de materiais"),
    ("validation-flow.md", "✅ Validation Flow", "Fluxo: Requisito → Projeto → Simulação → Teste → Validação"),
    ("project-roadmap.md", "📅 Project Roadmap", "Gantt: marcos, releases e status"),
    ("engineering-workflow.md", "⚙️ Engineering Workflow", "Fluxo padrão de engenharia"),
]


def generate_dashboard(docs: list[Document], date: str) -> str:
    lines: list[str] = []
    lines.append(_make_header("Dashboard de Diagramas", "GEN-DASHBOARD", date))

    lines.append("## Diagramas Gerados Automaticamente")
    lines.append("")
    lines.append("| Diagrama | Descrição | Link |")
    lines.append("|----------|-----------|------|")
    for filename, title, description in _DIAGRAMS:
        lines.append(f"| {title} | {description} | [{filename}](./{filename}) |")
    lines.append("")

    # Statistics
    from collections import Counter
    type_counts = Counter(d.artifact_type for d in docs)
    lines.append("## Estatísticas do Banco de Dados")
    lines.append("")
    lines.append("| Tipo | Quantidade |")
    lines.append("|------|-----------|")
    for artifact_type, count in sorted(type_counts.items()):
        lines.append(f"| {artifact_type} | {count} |")
    lines.append(f"| **Total** | **{len(docs)}** |")
    lines.append("")
    lines.append(f"*Última atualização: {date}*")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def generate_all(repo_root: str, date: str) -> dict[str, str]:
    """
    Read all documents from *repo_root* and return a dict mapping
    output filename (relative to docs/_generated/) → file content.
    """
    docs = load_documents(repo_root)

    return {
        "system-map.md": generate_system_map(docs, date),
        "product-breakdown.md": generate_product_breakdown(docs, date),
        "requirements-graph.md": generate_requirements_graph(docs, date),
        "adr-graph.md": generate_adr_graph(docs, date),
        "component-dependencies.md": generate_component_dependencies(docs, date),
        "bom-tree.md": generate_bom_tree(docs, date),
        "validation-flow.md": generate_validation_flow(docs, date),
        "project-roadmap.md": generate_project_roadmap(docs, date),
        "engineering-workflow.md": generate_engineering_workflow(docs, date),
        "DASHBOARD.md": generate_dashboard(docs, date),
    }
