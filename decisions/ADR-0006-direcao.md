---
title: Direção por Cremalheira Mecânica
id: ADR-0006
status: proposed
revision: "1.0"
owner: fundador
created: "2026-07-22"
updated: "2026-07-22"
related:
  - /decisions/README.md
  - /requirements/REQ-0006.md
  - /products/utv/steering/architecture.md
tags: [adr, direcao, steering, cremalheira, mecanica, utv]
---

# ADR-0006 — Direção por Cremalheira Mecânica

## Status

🟡 **Proposto** — Aguardando validação de requisitos completos

---

## Contexto

O sistema de direção define a manobrabilidade, a segurança e o conforto de operação do UTV. Para um veículo utilitário de campo, a escolha deve equilibrar esforço de direção, robustez, custo e simplicidade de manutenção em ambiente rural.

---

## Alternativas Consideradas

| Alternativa | Custo | Esforço | Manutenção | Precisão | Disponibilidade BR |
|-------------|-------|---------|------------|----------|-------------------|
| **Cremalheira mecânica** | **Baixo** | **Médio** | **Fácil** | **Boa** | **Excelente** |
| Direção hidráulica assistida | Médio | Baixo | Médio | Boa | Boa |
| Direção elétrica assistida (EPS) | Alto | Baixo | Difícil | Excelente | Limitada |
| Caixa de direção de recirculação de esferas | Médio | Baixo | Médio | Boa | Boa |
| Direção por alavanca (skid steer) | Baixo | Alto | Fácil | Baixa | Limitada |

---

## Decisão Proposta

**Caixa de direção por cremalheira mecânica** com relação de desmultiplicação entre 14:1 e 16:1, adaptada de veículo de passeio nacional, com barras de direção ajustáveis.

---

## Justificativa

1. **Custo** — cremalheiras mecânicas são as mais baratas e fáceis de obter no mercado nacional
2. **Manutenção simples** — sem sistema hidráulico ou elétrico a gerenciar
3. **Robustez** — sistema puramente mecânico, resistente a contaminação e vibração
4. **Sensação de direção** — feedback direto do terreno auxilia o operador em campo
5. **Reaproveitamento** — possibilidade de reaproveitamento de caixa de veículo nacional

---

## Consequências

### Positivas
- Menor custo de fabricação e manutenção
- Zero dependência de fluido hidráulico ou sistema elétrico auxiliar
- Peças de reposição amplamente disponíveis

### Negativas
- Maior esforço físico do operador em manobras lentas com carga
- Transmissão de impactos do terreno para o volante (precisa de amortecimento nas barras)

### Riscos
- Esforço excessivo em manobras de baixa velocidade (mitigado: relação de desmultiplicação adequada + ajuste de geometria)

---

## Relacionamentos

- Gerado por: [REQ-0006](../requirements/REQ-0006.md)
- Relacionado: [ADR-0004 — Suspensão](./ADR-0004-suspensao.md)
- Relacionado: [ADR-0002 — Chassis Tubular](./ADR-0002-chassis-tubular.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-22 | Fundador | Criação inicial |
