---
title: UTV Utilitário Modular
id: PROD-UTV-001
status: active
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /products/README.md
  - /requirements/README.md
  - /architecture/README.md
  - /decisions/README.md
tags: [utv, product, overview]
---

# UTV Utilitário Modular

## Visão Geral

O UTV Utilitário Modular é o primeiro produto da empresa.  
Projetado para aplicações agrícolas, rurais e de trabalho pesado no mercado brasileiro.

---

## Conceito

```mermaid
graph TD
    UTV[UTV Utilitário Modular]

    UTV --> CHASSIS[🔧 Chassis]
    UTV --> SUSP[🔩 Suspensão]
    UTV --> STEER[🔄 Direção]
    UTV --> BRAKE[🛑 Freios]
    UTV --> POWER[⚙️ Powertrain]
    UTV --> ELEC[⚡ Elétrica]
    UTV --> BODY[🚗 Carroceria]
    UTV --> CARGO[📦 Plataforma de Carga]
    UTV --> ERGO[👤 Ergonomia]
```

---

## Sistemas

| Sistema | Descrição | Status | Link |
|---------|-----------|--------|------|
| Chassis | Estrutura principal do veículo | 🟡 Em definição | [chassis/](./chassis/README.md) |
| Suspensão | Sistema de suspensão dianteiro e traseiro | 🟡 Em definição | [suspension/](./suspension/README.md) |
| Direção | Sistema de direção | 🟡 Em definição | [steering/](./steering/README.md) |
| Freios | Sistema de frenagem | 🟡 Em definição | [brakes/](./brakes/README.md) |
| Powertrain | Motor, transmissão e diferencial | 🟡 Em definição | [powertrain/](./powertrain/README.md) |
| Elétrica | Sistema elétrico e eletrônico | 🟡 Em definição | [electrical/](./electrical/README.md) |
| Carroceria | Painel, cabine e acabamentos | 🟡 Em definição | [body/](./body/README.md) |
| Plataforma de Carga | Plataforma modular traseira | 🟡 Em definição | [cargo_platform/](./cargo_platform/README.md) |
| Ergonomia | Posto de operação e conforto | 🟡 Em definição | [ergonomics/](./ergonomics/README.md) |

---

## Especificações Preliminares

| Parâmetro | Valor Alvo | Status |
|-----------|------------|--------|
| Capacidade de carga | ≥ 500 kg | A definir |
| Motorização | Motor diesel / gasolina nacional | A definir |
| Bitola | Compatível com implementos nacionais | A definir |
| Homologação | DENATRAN / INMETRO | A definir |
| Acionamento | 4x4 com tração traseira | A definir |

---

## Fases de Desenvolvimento

```mermaid
gantt
    title UTV — Fases de Desenvolvimento
    dateFormat  YYYY-MM
    section Fundação
    Requisitos               :req, 2026-08, 2026-12
    Arquitetura              :arch, 2026-10, 2027-02
    section Projeto
    CAD Conceitual           :cad1, 2027-01, 2027-06
    CAD Detalhado            :cad2, 2027-06, 2027-12
    section Prototipagem
    Protótipo #1             :p1, 2027-07, 2028-03
    Testes P1                :t1, 2028-01, 2028-06
    section Validação
    Protótipo #2             :p2, 2028-04, 2028-12
    Campanha de Testes       :t2, 2028-09, 2029-06
    section Homologação
    Homologação              :hom, 2029-01, 2029-12
    section Lançamento
    Lançamento Comercial     :launch, 2030-01, 2030-06
```

---

## Links Relacionados

- [Requisitos do UTV](../../requirements/README.md)
- [Arquitetura do Sistema](../../architecture/README.md)
- [BOM Principal](../../bom/README.md)
- [Plano de Testes](../../tests/README.md)
- [Simulações](../../simulations/README.md)
- [Decisões](../../decisions/README.md)
