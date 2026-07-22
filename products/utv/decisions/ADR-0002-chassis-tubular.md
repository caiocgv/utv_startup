---
title: Chassis Tubular como Estrutura Principal
id: ADR-0002
status: proposed
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /products/utv/decisions/README.md
  - /products/utv/chassis/architecture.md
  - /requirements/REQ-0001.md
tags: [adr, chassis, structure, manufacturing, utv]
---

# ADR-0002 — Chassis Tubular como Estrutura Principal

## Status

🟡 **Proposto** — Aguardando validação de requisitos completos

---

## Contexto

O chassis é o componente estrutural mais crítico do UTV. A escolha do conceito estrutural define custos de fabricação, peso, rigidez, capacidade de reparo e complexidade de homologação. Para uma startup com recursos limitados, a escolha deve equilibrar custo de fabricação com performance técnica.

---

## Alternativas Consideradas

| Alternativa | Custo Fab. | Peso | Rigidez | Reparo | Complexidade |
|-------------|------------|------|---------|--------|--------------|
| **Chassis tubular soldado** | **Baixo** | **Médio** | **Boa** | **Fácil** | **Baixa** |
| Chassis em chapa estampada | Alto | Baixo | Excelente | Difícil | Muito Alta |
| Chassis em perfil laminado | Baixo | Alto | Boa | Fácil | Baixa |
| Chassis híbrido (tubo + chapa) | Médio | Médio | Excelente | Médio | Média |

---

## Decisão Proposta

Chassis **tubular em aço soldado**, com tubo quadrado e redondo de perfis disponíveis no mercado nacional.

---

## Justificativa

1. **Fabricabilidade local** — serralheiros e metalúrgicas com capacidade nacional
2. **Custo reduzido** — material e processo de baixo custo
3. **Reparo simples** — qualquer soldador qualificado pode fazer reparos
4. **Flexibilidade de projeto** — geometria facilmente ajustável em protótipos
5. **Compatibilidade** — mesmos processos utilizados em UTVs e implementos nacionais

---

## Consequências

### Positivas
- Custo de fabricação reduzido para prototipagem
- Facilidade de iteração no projeto
- Base de fornecedores ampla no Brasil

### Negativas
- Peso maior que estamparia
- Precisão dimensional dependente de gabaritos de soldagem
- Necessidade de tratamento superficial rigoroso (anticorrosão)

---

## Relacionamentos

- Gerado por: [REQ-0001](../../../requirements/REQ-0001.md)
- Relacionado: [Arquitetura do Chassis](../chassis/architecture.md)
- Relacionado: [ADR-0001](./ADR-0001-repositorio-plm.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-21 | Fundador | Criação inicial |
