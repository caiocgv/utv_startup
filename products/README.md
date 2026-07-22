---
title: Produtos
id: PROD-README
status: active
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /README.md
  - /requirements/README.md
  - /products/utv/components/README.md
tags: [products, index]
---

# Produtos

Este diretório concentra toda a documentação técnica de cada produto da empresa.

---

## Filosofia

```mermaid
flowchart TD
    CONCEPT[Conceito] --> REQ[Requisitos]
    REQ --> ARCH[Arquitetura]
    ARCH --> SYSTEMS[Sistemas]
    SYSTEMS --> CAD[CAD / Projeto]
    CAD --> BOM[BOM]
    BOM --> SIM[Simulação]
    SIM --> TEST[Testes]
    TEST --> VAL[Validação]
    VAL --> PROD[Produção]
```

---

## Produtos Ativos

| Produto | Status | Fase | Link |
|---------|--------|------|------|
| UTV Utilitário Modular | 🟡 Em desenvolvimento | Fundação | [utv/](./utv/README.md) |

---

## Produtos Futuros

| Produto | Status | Previsão |
|---------|--------|----------|
| Carreta Homologada | 🔵 Planejado | 2031 |
| Implementos Agrícolas | 🔵 Planejado | 2032 |
| Plataforma Modular Gen2 | 🔵 Planejado | 2033 |

---

## Links Relacionados

- [Roadmap de Produto](../roadmap/product/README.md)
- [Componentes Reutilizáveis](./utv/components/README.md)
- [Requisitos](../requirements/README.md)
- [Decisões](./utv/decisions/README.md)
