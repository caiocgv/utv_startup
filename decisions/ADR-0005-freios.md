---
title: Sistema de Freios a Disco Hidráulico nos 4 Rodas
id: ADR-0005
status: proposed
revision: "1.0"
owner: fundador
created: "2026-07-22"
updated: "2026-07-22"
related:
  - /decisions/README.md
  - /requirements/REQ-0005.md
  - /products/utv/brakes/architecture.md
tags: [adr, freios, brakes, disco, hidraulico, seguranca, utv]
---

# ADR-0005 — Sistema de Freios a Disco Hidráulico nos 4 Rodas

## Status

🟡 **Proposto** — Aguardando validação de requisitos completos

---

## Contexto

O sistema de freios é um componente crítico de segurança ativa. Para um UTV com 500 kg de carga útil, operando em terrenos acidentados e descidas, a escolha do tipo de freio impacta diretamente a distância de parada, a manutenção e o custo do veículo.

---

## Alternativas Consideradas

| Alternativa | Desempenho | Manutenção | Custo | Durabilidade | Disponibilidade BR |
|-------------|------------|------------|-------|-------------|-------------------|
| **Disco hidráulico 4 rodas** | **Excelente** | **Médio** | **Médio** | **Boa** | **Boa** |
| Tambor mecânico 4 rodas | Boa | Fácil | Baixo | Boa | Excelente |
| Disco dianteiro + tambor traseiro | Boa | Médio | Médio | Boa | Excelente |
| Disco hidráulico apenas traseiro | Básico | Médio | Baixo | Boa | Boa |
| Sistema ABS hidráulico | Excelente | Difícil | Alto | Excelente | Limitada |

---

## Decisão Proposta

**Freios a disco hidráulico nos 4 rodas**, com cilindro mestre duplo, circuito diagonal independente e freio de estacionamento mecânico nas rodas traseiras.

---

## Justificativa

1. **Desempenho superior** — discos hidráulicos atendem às distâncias de parada exigidas com carga
2. **Dissipação de calor** — discos ventilados eliminam melhor o calor em descidas prolongadas
3. **Resposta proporcional** — pedal de freio progressivo facilita o controle em terreno irregular
4. **Circuito duplo diagonal** — falha em um circuito mantém 50% da força de frenagem
5. **Disponibilidade** — pastilhas e discos para veículos nacionais são amplamente disponíveis

---

## Consequências

### Positivas
- Distância de frenagem dentro dos requisitos mesmo com carga máxima
- Manutenção possível em oficinas comuns
- Peças de reposição com vasta disponibilidade nacional

### Negativas
- Custo superior ao sistema a tambor
- Requer fluido de freio com troca periódica (DOT 4 recomendado)
- Mangueiras hidráulicas podem desgastar com vibração off-road

### Riscos
- Aquecimento excessivo em uso intenso (mitigado: discos ventilados)
- Contaminação do fluido por umidade (mitigado: manutenção preventiva anual)

---

## Relacionamentos

- Gerado por: [REQ-0005](../requirements/REQ-0005.md)
- Relacionado: [ADR-0004 — Suspensão](./ADR-0004-suspensao.md)
- Relacionado: [ADR-0002 — Chassis Tubular](./ADR-0002-chassis-tubular.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-22 | Fundador | Criação inicial |
