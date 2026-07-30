---
title: Sistema de Suspensão Independente para o UTV
id: ADR-0004
status: proposed
revision: "1.1"
owner: fundador
created: "2026-07-22"
updated: "2026-07-30"
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
| **Suspensão independente duplo A com pull rod (dianteira)** | **Médio** | **Alto** | **Médio** | **Excelente** | **Médio** |
| Suspensão eixo rígido (Beam axle) | Baixo | Baixo | Fácil | Boa | Alto |
| Suspensão McPherson | Baixo | Médio | Fácil | Boa | Baixo |
| Suspensão semi-independente (torção) | Médio | Médio | Fácil | Boa | Baixo |
| Suspensão independente multilink | Alto | Alto | Difícil | Excelente | Alto |

---

## Decisão Proposta

**Suspensão independente duplo A (Double Wishbone) com pull rod e amortecedor XTZ-250** na dianteira e **suspensão traseira McPherson derivada do VW Gol, adaptada às necessidades do projeto** na traseira, priorizando disponibilidade de componentes, empacotamento e capacidade de adaptação ao uso off-road.

---

## Justificativa

1. **Curso adequado** — a suspensão duplo A com pull rod permite curso compatível com o uso off-road e melhor liberdade de posicionamento do amortecedor dianteiro
2. **Geometria controlada** — camber e toe dianteiros são controlados pela geometria dos braços sobrepostos
3. **Aproveitamento de componentes nacionais** — o amortecedor XTZ-250 e o conjunto McPherson do VW Gol oferecem base conhecida, de fácil reposição e adaptação
4. **Empacotamento traseiro simplificado** — a solução McPherson traseira reduz a quantidade de componentes dedicados em relação a alternativas multilink
5. **Custo-benefício** — combinação equilibra desempenho, disponibilidade de peças e esforço de desenvolvimento

---

## Consequências

### Positivas
- Excelente desempenho off-road
- Curso de suspensão adequado aos requisitos
- Boa disponibilidade de componentes nacionais adaptáveis

### Negativas
- Necessidade de adaptação estrutural e geométrica do conjunto McPherson traseiro ao chassi do projeto
- Necessidade de geometria cuidadosa para evitar desgaste prematuro
- Integração do pull rod dianteiro aumenta a complexidade de projeto e fabricação

### Riscos
- Geometria mal calculada pode gerar comportamento instável
- Seleção inadequada de relações de alavanca no pull rod pode comprometer curso e esforço no amortecedor
- Adaptação insuficiente do conjunto traseiro pode reduzir durabilidade em uso severo

---

## Relacionamentos

- Gerado por: [REQ-0004](../requirements/REQ-0004.md)
- Relacionado: [ADR-0002 — Chassis Tubular](./ADR-0002-chassis-tubular.md)
- Relacionado: [ADR-0005 — Sistema de Freios](./ADR-0005-freios.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.1 | 2026-07-30 | Copilot | Atualiza definições de suspensão dianteira e traseira |
| 1.0 | 2026-07-22 | Fundador | Criação inicial |
