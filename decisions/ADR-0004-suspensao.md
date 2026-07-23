---
title: Sistema de Suspensão Independente para o UTV
id: ADR-0004
status: proposed
revision: "1.0"
owner: fundador
created: "2026-07-22"
updated: "2026-07-22"
related:
  - /decisions/README.md
  - /requirements/REQ-0004.md
  - /products/utv/suspension/architecture.md
tags: [adr, suspensao, suspension, off-road, utv]
---

# ADR-0004 — Sistema de Suspensão Independente para o UTV

## Status

🟡 **Proposto** — Aguardando validação de requisitos completos

---

## Contexto

A escolha do conceito de suspensão define diretamente o conforto do operador, o desempenho off-road, o custo de fabricação e a complexidade de manutenção em campo. Para um UTV de uso rural com capacidade de 500 kg, o sistema deve equilibrar curso de suspensão, robustez e custo.

---

## Alternativas Consideradas

| Alternativa | Custo | Curso | Manutenção | Off-road | Peso |
|-------------|-------|-------|------------|----------|------|
| **Suspensão independente duplo A (dianteira)** | **Médio** | **Alto** | **Médio** | **Excelente** | **Médio** |
| Suspensão eixo rígido (Beam axle) | Baixo | Baixo | Fácil | Boa | Alto |
| Suspensão McPherson | Baixo | Médio | Fácil | Boa | Baixo |
| Suspensão semi-independente (torção) | Médio | Médio | Fácil | Boa | Baixo |
| Suspensão independente multilink | Alto | Alto | Difícil | Excelente | Alto |

---

## Decisão Proposta

**Suspensão independente duplo A (Double Wishbone)** na dianteira e **suspensão de eixo rígido com molas de lâmina ou molas helicoidais e 4 braços** na traseira, priorizando robustez para carga e facilidade de fabricação nacional.

---

## Justificativa

1. **Curso adequado** — suspensão duplo A proporciona curso ≥ 150 mm necessário ao off-road
2. **Geometria controlada** — camber e toe controlados pela geometria dos braços
3. **Fabricabilidade local** — braços de suspensão podem ser fabricados por metalúrgica nacional
4. **Robustez traseira** — eixo rígido traseiro mais adequado à carga de 500 kg
5. **Custo-benefício** — combinação equilibra performance e custo de produção em série

---

## Consequências

### Positivas
- Excelente desempenho off-road
- Curso de suspensão adequado aos requisitos
- Fabricação nacional viável

### Negativas
- Maior complexidade que suspensão de eixo rígido
- Necessidade de geometria cuidadosa para evitar desgaste prematuro
- Mais pontos de articulação que requerem manutenção periódica

### Riscos
- Geometria mal calculada pode gerar comportamento instável
- Desgaste de buchas em campo (mitigado: buchas standard disponíveis)

---

## Relacionamentos

- Gerado por: [REQ-0004](../requirements/REQ-0004.md)
- Relacionado: [ADR-0002 — Chassis Tubular](./ADR-0002-chassis-tubular.md)
- Relacionado: [ADR-0005 — Sistema de Freios](./ADR-0005-freios.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-22 | Fundador | Criação inicial |
