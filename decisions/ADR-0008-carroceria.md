---
title: Carroceria em Aço com Plataforma Basculante
id: ADR-0008
status: proposed
revision: "1.0"
owner: fundador
created: "2026-07-22"
updated: "2026-07-22"
related:
  - /decisions/README.md
  - /requirements/REQ-0009.md
  - /requirements/REQ-0001.md
  - /products/utv/body/architecture.md
tags: [adr, carroceria, body, plataforma, basculante, aco, utv]
---

# ADR-0008 — Carroceria em Aço com Plataforma Basculante

## Status

🟡 **Proposto** — Aguardando validação de requisitos completos

---

## Contexto

A carroceria define a funcionalidade de trabalho, a durabilidade e a identidade visual do UTV. Para uso rural intensivo com carga de até 500 kg, a escolha do material e do conceito de plataforma de carga impacta diretamente a utilidade do veículo para o produtor.

---

## Alternativas Consideradas

### Material da Carroceria

| Alternativa | Custo | Peso | Resistência | Reparo | Disponibilidade BR |
|-------------|-------|------|-------------|--------|-------------------|
| **Aço carbono (chapa 1,5–2,0 mm)** | **Baixo** | **Médio** | **Excelente** | **Fácil** | **Excelente** |
| Fibra de vidro | Baixo | Baixo | Boa | Difícil | Boa |
| Alumínio | Médio | Baixo | Boa | Médio | Média |
| PEAD (polietileno) | Médio | Baixo | Boa | Difícil | Boa |
| GFRP (fibra de carbono) | Alto | Muito Baixo | Excelente | Muito Difícil | Limitada |

### Plataforma de Carga

| Alternativa | Custo | Praticidade | Peso | Complexidade |
|-------------|-------|-------------|------|--------------|
| **Plataforma fixa com basculamento manual** | **Baixo** | **Alta** | **Baixo** | **Baixa** |
| Plataforma fixa sem basculamento | Muito Baixo | Média | Muito Baixo | Nenhuma |
| Plataforma com basculamento hidráulico | Médio | Muito Alta | Médio | Média |
| Container/caçamba removível | Médio | Boa | Médio | Média |

---

## Decisão Proposta

**Carroceria em chapa de aço carbono** (1,5 mm em painéis externos, 2,0 mm na plataforma de carga) com **plataforma traseira basculante manualmente** por mecanismo de dobradiça e trava, acabamento em primer epoxi + tinta poliuretano.

---

## Justificativa

1. **Custo** — chapa de aço é o material mais barato e acessível para fabricação nacional
2. **Reparo** — qualquer chapeador ou funileiro pode reparar danos de campo
3. **Soldabilidade** — compatível com o chassis tubular em aço (mesmos processos)
4. **Basculamento manual** — elimina sistema hidráulico, reduzindo custo e manutenção
5. **Proteção anticorrosiva** — primer epoxi + PU atende 500 h salt spray exigidos

---

## Consequências

### Positivas
- Baixo custo de fabricação e reparo
- Base de fornecedores de chaparia amplamente disponível no Brasil
- Plataforma basculante facilita descarga de granéis e terra

### Negativas
- Peso superior a fibra ou alumínio
- Tratamento anticorrosão exige processo rigoroso de jateamento + fosfatização

### Riscos
- Corrosão acelerada em ambiente de alta umidade/sal (mitigado: processo anticorrosão rigoroso + manutenção preventiva)
- Deformação permanente sob carga excessiva (mitigado: design com reforços estruturais na plataforma)

---

## Relacionamentos

- Gerado por: [REQ-0009](../requirements/REQ-0009.md)
- Gerado por: [REQ-0001](../requirements/REQ-0001.md)
- Relacionado: [ADR-0002 — Chassis Tubular](./ADR-0002-chassis-tubular.md)
- Relacionado: [ADR-0007 — Ergonomia](./ADR-0007-ergonomia.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-22 | Fundador | Criação inicial |
