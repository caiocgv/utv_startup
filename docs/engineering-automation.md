---
title: Automação de Documentação de Engenharia
id: DOC-0001
status: active
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /tools/README.md
  - /docs/README.md
tags: [documentation, automation, engineering, ci]
---

# Automação de Documentação de Engenharia

Este documento descreve a automação criada para validar documentos Markdown,
verificar referências cruzadas e regenerar automaticamente índices e relatórios
de rastreabilidade a cada `push` na branch `main`.

---

## Como Funciona

O sistema é composto por três partes:

1. **`tools/engdb.py`** — ferramenta Python que valida e gera relatórios.
2. **`requirements-engdb.txt`** — dependências Python (apenas PyYAML).
3. **`.github/workflows/engineering-docs.yml`** — GitHub Action que orquestra a execução.

### Fluxo da Action

```
push para main
      │
      ▼
python tools/engdb.py validate
      │  falha → Action falha, nenhum arquivo gerado
      ▼
python tools/engdb.py generate
      │
      ▼
git add docs/_generated/
      │  sem mudanças → nenhum commit
      ▼
git commit + git push  (com "[skip ci]" para evitar loop)
```

---

## Formato do Front Matter

Todo artefato de engenharia deve começar com um bloco YAML entre `---`:

```yaml
---
id: REQ-0001
title: Capacidade de Carga Mínima
status: draft
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - SYS-0001
validated_by:
  - TST-0001
tags: [requirement, utv]
---
```

### Campo `id`

O campo `id` é o identificador único do artefato. Deve seguir o formato:

```
PREFIXO-NNNN
```

onde `PREFIXO` é um dos tipos suportados e `NNNN` é um número com exatamente
4 dígitos (com zeros à esquerda se necessário).

**Exemplos válidos:** `REQ-0001`, `ADR-0042`, `TST-0100`

---

## Tipos de Artefatos Suportados

| Prefixo | Tipo | Exemplo |
|---------|------|---------|
| `REQ` | Requisito | `REQ-0001` |
| `SYS` | Sistema | `SYS-0001` |
| `CMP` | Componente | `CMP-0001` |
| `ADR` | Decisão (Architecture Decision Record) | `ADR-0001` |
| `DRW` | Desenho | `DRW-0001` |
| `BOM` | Lista de Materiais | `BOM-0001` |
| `SIM` | Simulação | `SIM-0001` |
| `TST` | Teste | `TST-0001` |
| `VAL` | Validação | `VAL-0001` |
| `DOC` | Documento | `DOC-0001` |
| `MFG` | Fabricação | `MFG-0001` |
| `SUP` | Fornecedor | `SUP-0001` |

Arquivos com prefixos não listados acima (como `JRN-`, `ENG-`, `ROOT-`) são
ignorados pela ferramenta e não são indexados nem validados como artefatos.

---

## Campos Aceitos

### Campos obrigatórios

Todos os artefatos devem conter:

| Campo | Descrição |
|-------|-----------|
| `id` | Identificador único no formato `PREFIXO-NNNN` |
| `title` | Título descritivo do artefato |
| `status` | Estado atual (`draft`, `active`, `obsolete`, `archived`, etc.) |
| `revision` | Revisão atual (ex.: `"1.0"`, `"A"`) |

### Campos de referência

Estes campos podem conter IDs de outros artefatos (`PREFIX-NNNN`) ou caminhos
de arquivo. Apenas valores que correspondam ao padrão `PREFIX-NNNN` são
validados como referências cruzadas entre artefatos.

| Campo | Uso típico |
|-------|-----------|
| `related` | Relação genérica |
| `relates_to` | Relação genérica (alternativo) |
| `requirements` | Requisitos implementados |
| `implements` | Artefatos que este implementa |
| `implemented_by` | Artefatos que implementam este |
| `validated_by` | Validações que cobrem este artefato |
| `verifies` | O que este artefato verifica |
| `tested_by` | Testes que cobrem este artefato |
| `tests` | O que este artefato testa |
| `components` | Componentes relacionados |
| `systems` | Sistemas relacionados |
| `products` | Produtos relacionados |
| `decisions` | Decisões (ADRs) relacionadas |
| `drawings` | Desenhos relacionados |
| `bom` | Listas de materiais relacionadas |
| `simulations` | Simulações relacionadas |
| `suppliers` | Fornecedores relacionados |
| `affected` | Artefatos afetados |
| `depends_on` | Dependências |
| `parent` | Artefato pai (hierarquia) |
| `children` | Artefatos filhos (hierarquia) |

---

## Validações Obrigatórias

A ferramenta falha quando encontra:

| Erro | Descrição |
|------|-----------|
| ID duplicado | Dois arquivos com o mesmo `id` |
| YAML inválido | Front matter não parseável |
| Campo obrigatório ausente | `id`, `title`, `status` ou `revision` faltando |
| ID fora do padrão | Prefixo reconhecido mas formato inválido |
| Referência inexistente | Campo de referência aponta para um ID que não existe |
| Link local quebrado | Link Markdown `[texto](caminho)` aponta para arquivo inexistente |
| Auto-referência | Campo de referência contém o próprio `id` do artefato |

---

## Arquivos Gerados

Os relatórios são escritos em `docs/_generated/` e **não devem ser editados
manualmente** — serão sobrescritos na próxima execução da Action.

| Arquivo | Conteúdo |
|---------|----------|
| `ARTIFACT_INDEX.md` | Tabela com todos os artefatos (ID, título, tipo, status, revisão, link) |
| `TRACEABILITY.md` | Matriz de rastreabilidade: relações de origem/destino e referências recebidas |
| `DASHBOARD.md` | Contagem de artefatos por tipo e por status, com links para os relatórios |

### Regras de geração

- Apenas arquivos dentro de `docs/_generated/` são modificados.
- Um novo commit só é feito quando o conteúdo dos arquivos muda.
- A saída é determinística: mesma entrada sempre produz mesma saída.
- Cada arquivo começa com um aviso de que não deve ser editado manualmente.

---

## Como Testar Localmente

### Pré-requisitos

```bash
pip install -r requirements-engdb.txt
```

### Executar validação

```bash
python tools/engdb.py validate
```

### Gerar relatórios

```bash
python tools/engdb.py generate
```

### Executar tudo (validação + geração)

```bash
python tools/engdb.py all
```

### Especificar raiz do repositório

```bash
python tools/engdb.py --root /caminho/para/repo validate
```

---

## Como Configurar Permissões do GitHub Actions

Para que a Action consiga fazer `git push` com os arquivos gerados, é necessário
conceder permissão de escrita ao token do GitHub Actions.

### Opção 1 — Permissão no arquivo de workflow (já configurado)

O arquivo `.github/workflows/engineering-docs.yml` já inclui:

```yaml
permissions:
  contents: write
```

### Opção 2 — Configuração no repositório (recomendado para maior controle)

1. Acesse **Settings → Actions → General** no repositório.
2. Em **Workflow permissions**, selecione **Read and write permissions**.
3. Clique em **Save**.

---

## Prevenção de Loop

A Action utiliza duas camadas de proteção contra loop infinito:

1. **Verificação do autor:** A Action só executa quando o `github.actor` não é
   `github-actions[bot]`. Execuções manuais via `workflow_dispatch` são sempre
   permitidas.

2. **`[skip ci]` na mensagem de commit:** O commit de geração inclui `[skip ci]`
   na mensagem, o que faz o GitHub ignorar o push para fins de disparo de workflows.

---

## Limitações da Primeira Versão

- **Verificação de links apenas em artefatos:** Links locais quebrados são
  verificados somente em arquivos com IDs de artefatos válidos (`PREFIX-NNNN`).
  Arquivos como templates, journals e READMEs não têm seus links verificados.

- **Referências por ID apenas:** A validação de referências cruzadas cobre apenas
  valores no formato `PREFIX-NNNN`. Caminhos de arquivo em campos de referência
  não são validados como referências cruzadas.

- **Sem suporte a subtipos de ID:** O formato é sempre `PREFIX-NNNN` (4 dígitos).
  Não há suporte a versões, subcomponentes ou sufixos no ID.

- **Sem geração de PDF ou HTML:** Os relatórios são apenas arquivos Markdown.

- **Sem notificações:** A ferramenta não envia notificações por e-mail, Slack, etc.
