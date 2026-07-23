---
title: Motor VW AP 1.6/1.8 como Propulsão do UTV
id: ADR-0003
status: accepted
revision: "3.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-22"
related:
  - /decisions/README.md
  - /products/utv/powertrain/architecture.md
  - /requirements/REQ-0002.md
  - /requirements/REQ-0003.md
tags: [adr, powertrain, motor, vw-ap, propulsion, utv]
---

# ADR-0003 — Motor VW AP 1.6/1.8 como Propulsão do UTV

## Status

✅ **Aceito** — Motor pré-definido; aguardando integração no projeto de powertrain

---

## Contexto

A escolha do sistema de propulsão define peso, custo, performance e experiência do usuário. O mercado-alvo (rural/agrícola brasileiro) exige combustível acessível, manutenção simples e peças de reposição consolidadas em todo o país. O motor VW AP (Ar/Água, Polo) nas versões 1.6 e 1.8 é um dos motores mais difundidos no Brasil, com décadas de produção, extensa rede de mecânicos especializados e peças disponíveis em qualquer estado.

---

## Alternativas Consideradas

| Alternativa | Custo | Manutenção | Homologação | Potência | Autonomia | Mercado-alvo |
|-------------|-------|------------|-------------|----------|-----------|--------------|
| **Motor VW AP 1.6/1.8 (gasolina/flex)** | **Baixo** | **Excelente** | **Padrão** | **~65–85 cv** | **Boa** | **Rural** |
| Motor diesel estacionário | Baixo | Excelente | Padrão | ~20–30 cv | Excelente | Rural |
| Motor elétrico | Alto | Baixa | Complexa | Variável | Limitada | Urbano |
| Motor automotivo genérico segunda mão | Baixo | Boa | Padrão | Variável | Boa | Rural |
| Motor gasolina estacionário (tipo gerador) | Muito Baixo | Excelente | Padrão | ~10–20 cv | Boa | Rural |

---

## Decisão

**Motor VW AP 1.6 ou 1.8 (gasolina/flex) com câmbio integrado** (caixa de 4 ou 5 marchas do mesmo conjunto), obtido como conjunto completo de segunda mão ou novo via mercado de reposição nacional.

---

## Justificativa

1. **Potência adequada** — 65–85 cv atende aos requisitos de REQ-0003 (≥ 60 cv) e garante folga de performance
2. **Torque** — torque na faixa de 120–140 N·m atende REQ-0003 (≥ 120 N·m)
3. **Infraestrutura de manutenção** — mecânicos especializados e peças em todo o Brasil
4. **Custo** — conjunto motor/câmbio amplamente disponível a baixo custo no mercado de reposição
5. **Câmbio integrado** — elimina a necessidade de projeto de transmissão adicional
6. **Homologação** — processo estabelecido para motor de combustão flex/gasolina (PROCONVE)
7. **Peças de reposição** — cadeia logística nacional consolidada com décadas de histórico

---

## Consequências

### Positivas
- Facilidade de manutenção pelo usuário final em qualquer região do Brasil
- Peças de reposição amplamente disponíveis e baratas
- Conjunto motor/câmbio compacto e bem documentado
- Flexibilidade de combustível (gasolina e etanol)

### Negativas
- Impacto ambiental maior que elétrico
- Dependência de combustível fóssil (risco de longo prazo)
- Conjunto de segunda mão exige avaliação de condição e possível retífica
- Adaptação do câmbio ao sistema de transmissão final do UTV requer projeto mecânico

### Riscos
- Disponibilidade futura reduzindo conforme modelos mais antigos saem de circulação (mitigado: mercado de reposição robusto por décadas)
- Variação de condição em unidades de segunda mão (mitigado: especificação mínima de inspeção antes da compra)

---

## Relacionamentos

- Gerado por: [REQ-0002](../requirements/REQ-0002.md)
- Gerado por: [REQ-0003](../requirements/REQ-0003.md)
- Relacionado: [Arquitetura Powertrain](../products/utv/powertrain/architecture.md)
- Relacionado: [Fornecedores](../suppliers/README.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-21 | CACV | Criação inicial |
| 2.0 | 2026-07-22 | CACV | Motor pré-definido como VW AP 1.6/1.8 |
| 3.0 | 2026-07-22 | Copilot | Status aceito; ADR atualizado com decisão e justificativa completas |
