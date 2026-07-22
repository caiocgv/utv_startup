---
title: Ergonomia com Banco Ajustável e Proteção ROPS Integrada
id: ADR-0007
status: proposed
revision: "1.0"
owner: fundador
created: "2026-07-22"
updated: "2026-07-22"
related:
  - /decisions/README.md
  - /requirements/REQ-0008.md
  - /requirements/REQ-0007.md
  - /products/utv/ergonomics/architecture.md
tags: [adr, ergonomia, ergonomics, rops, banco, seguranca, utv]
---

# ADR-0007 — Ergonomia com Banco Ajustável e Proteção ROPS Integrada

## Status

🟡 **Proposto** — Aguardando validação de requisitos completos

---

## Contexto

A interface operador-máquina define a segurança e a produtividade do UTV em jornadas de trabalho rural. O projeto deve atender ao perfil antropométrico do trabalhador rural brasileiro (P5 a P95), garantir proteção ao capotamento e oferecer conforto suficiente para operação contínua.

---

## Alternativas Consideradas

### Banco

| Alternativa | Ajuste | Conforto | Custo | Manutenção |
|-------------|--------|---------|-------|------------|
| **Banco deslizante com regulagem longitudinal** | **Alto** | **Bom** | **Médio** | **Fácil** |
| Banco fixo sem ajuste | Nenhum | Básico | Baixo | Nenhuma |
| Banco com ajuste longitudinal + altura | Alto | Excelente | Alto | Média |
| Assento tipo bucket (automobilístico) | Fixo | Boa | Médio | Fácil |

### Proteção ao Capotamento (ROPS)

| Alternativa | Proteção | Custo | Peso | Complexidade |
|-------------|----------|-------|------|--------------|
| **ROPS tubular integrado ao chassis** | **Excelente** | **Baixo** | **Médio** | **Baixa** |
| Cabine fechada em aço | Excelente | Alto | Alto | Alta |
| Rollbar desmontável | Boa | Baixo | Baixo | Baixa |
| Sem proteção | Nenhuma | Zero | Zero | Nenhuma |

---

## Decisão Proposta

**Banco deslizante com regulagem longitudinal** fixado ao chassis, com encosto reclinável, e **ROPS tubular fixo integrado ao chassis** conforme ISO 3471, com cinto de segurança de 3 pontos.

---

## Justificativa

1. **Ajuste longitudinal** — atende ao percentil P5 a P95 do operador rural brasileiro
2. **ROPS integrado** — proteção permanente sem necessidade de montagem antes do uso
3. **Cinto de 3 pontos** — retém o operador durante tombamento mantendo-o no interior do ROPS
4. **Custo-efetivo** — ROPS tubular de baixo custo de fabricação nacional
5. **Norma ISO 3471** — certificação reconhecida internacionalmente para ROPS agrícolas

---

## Consequências

### Positivas
- Segurança passiva atendida para tombamento lateral e frontal
- Conforto adequado para jornadas de 8 horas
- Fabricação do ROPS integrada à linha de produção do chassis

### Negativas
- ROPS fixo aumenta levemente o peso do conjunto chassis-ergonomia
- Necessidade de gabarito de soldagem para ROPS certificável

### Riscos
- Não-conformidade dimensional do ROPS compromete a certificação (mitigado: ensaio por laboratório credenciado)

---

## Relacionamentos

- Gerado por: [REQ-0008](../requirements/REQ-0008.md)
- Relacionado: [ADR-0002 — Chassis Tubular](./ADR-0002-chassis-tubular.md)
- Relacionado: [ADR-0008 — Carroceria e Proteções](./ADR-0008-carroceria.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-22 | Fundador | Criação inicial |
