---
title: Simulações
id: SIM-README
status: active
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /tests/README.md
  - /products/utv/README.md
tags: [simulations, fea, analysis]
---

# Simulações

Simulações computacionais realizadas durante o desenvolvimento do produto.

## Tipos de Simulação

| Tipo | Descrição | Software | Link |
|------|-----------|----------|------|
| FEA Estática | Análise de elementos finitos estática | FreeCAD/CalculiX | [fea/](./fea/) |
| Centro de Gravidade | Cálculo do CG do veículo | FreeCAD | [cg/](./cg/) |
| Peso | Análise de peso e distribuição | FreeCAD | [weight/](./weight/) |
| Rigidez | Rigidez torsional e flexional | FreeCAD/CalculiX | [stiffness/](./stiffness/) |
| Fadiga | Análise de fadiga estrutural | FreeCAD/CalculiX | [fatigue/](./fatigue/) |
| Resultados | Consolidação dos resultados | — | [results/](./results/) |

## Registro de Simulações

| ID | Tipo | Sistema | Data | Status |
|----|------|---------|------|--------|
| SIM-0001 | A criar | — | — | 🔴 Pendente |

## Software Utilizado

- **FreeCAD** — CAD e pré/pós-processamento (gratuito)
- **CalculiX** — Solver FEA (gratuito, integrado ao FreeCAD)

## Links Relacionados

- [Testes](../../../tests/README.md)
- [Produtos](../../README.md)
