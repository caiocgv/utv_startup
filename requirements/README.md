---
title: Sistema de Requisitos
id: REQ-README
status: active
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /README.md
  - /products/utv/README.md
  - /tests/README.md
  - /validation/README.md
tags: [requirements, system, traceability]
---

# Sistema de Requisitos

Todos os requisitos do produto são registrados e rastreados neste diretório.

---

## Estrutura de Rastreabilidade

```mermaid
flowchart TD
    REQ[Requisito REQ-XXXX]
    REQ --> ARCH[Arquitetura]
    ARCH --> CAD[Projeto CAD]
    CAD --> BOM[BOM]
    BOM --> TEST[Teste TEST-XXXX]
    TEST --> VAL[Validação]
    VAL --> MFG[Fabricação]
    MFG --> PROD[Produto]
```

---

## Índice de Requisitos

| ID | Título | Produto | Sistema | Status |
|----|--------|---------|---------|--------|
| [REQ-0001](./REQ-0001.md) | Capacidade de Carga Mínima | UTV | Chassis | 🟡 Em revisão |
| [REQ-0002](./REQ-0002.md) | Motorização Nacional | UTV | Powertrain | 🟡 Em revisão |
| [REQ-0003](./REQ-0003.md) | Homologação DENATRAN | UTV | Global | 🔴 Aberto |

---

## Formato do Identificador

```
REQ-XXXX
```

Exemplos: `REQ-0001`, `REQ-0042`, `REQ-1000`

---

## Status dos Requisitos

| Status | Significado |
|--------|-------------|
| 🔴 Aberto | Requisito identificado, não detalhado |
| 🟡 Em revisão | Em processo de detalhamento/revisão |
| 🟢 Aprovado | Revisado e aprovado |
| 🔵 Implementado | Solução de engenharia existente |
| ✅ Validado | Testado e validado |
| ⚫ Obsoleto | Cancelado ou substituído |

---

## Como Criar um Requisito

Use o [template de requisito](../templates/requirement.md).

---

## Links Relacionados

- [Produto UTV](../products/utv/README.md)
- [Testes](../tests/README.md)
- [Validação](../validation/README.md)
- [Decisões](../decisions/README.md)
