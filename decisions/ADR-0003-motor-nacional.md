---
title: Motor de Combustão Nacional como Propulsão Inicial
id: ADR-0003
status: proposed
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /decisions/README.md
  - /products/utv/powertrain/architecture.md
  - /requirements/REQ-0002.md
tags: [adr, powertrain, motor, propulsion, utv]
---

# ADR-0003 — Motor de Combustão Nacional como Propulsão Inicial

## Status

🟡 **Pré-definido** — Aguardando implementação no projeto

---

## Contexto

A escolha do sistema de propulsão define peso, custo e experiência do usuário. O mercado-alvo (rural/agrícola brasileiro) tem características específicas de combustível disponível, manutenção e preferência do usuário.

---

## Alternativas Consideradas

| Alternativa | Custo | Manutenção | Homologação | Força | Autonomia | Mercado-alvo |
|-------------|-------|------------|-------------|-------|-----------|--------------|
| **Motor gasolina estacionário** | **Baixo** | **Excelente** | **Padrão** | **Baixo** | **Boa** | **Rural** |
| Motor diesel estacionário | Baixo | Excelente | Padrão | Baixo | Excelente | Rural |
| Motor elétrico | Alto | Baixa | Complexa | Boa | Limitada | Urbano |
| Motor automotivo segunda mão | Baixo | Excelente | Padrão | Excelente | Boa | Rural |

---

## Decisão Proposta

Motor de **combustão interna (gasolina ou flex) de fabricante nacional**, disponível com rede de assistência e peças de reposição consolidada no Brasil. Motor VW AP 1.6 ou 1.8 com cambio integrado.

---

## Justificativa

1. **Infraestrutura de manutenção** — postos de gasolina e mecânicos em todo o Brasil
2. **Custo** — motores nacionais amplamente disponíveis e com preço competitivo
3. **Homologação simplificada** — processo já estabelecido para combustão
4. **Demanda do mercado** — usuário rural familiarizado com combustão
5. **Peças de reposição** — cadeia logística nacional consolidada

---

## Consequências

### Positivas
- Facilidade de manutenção pelo usuário final
- Peças de reposição em todo o Brasil
- Custo inicial menor

### Negativas
- Impacto ambiental maior que elétrico
- Dependência de combustível fóssil (risco de longo prazo)
- Ruído e vibrações a serem gerenciados

---

## Relacionamentos

- Gerado por: [REQ-0002](../requirements/REQ-0002.md)
- Relacionado: [Arquitetura Powertrain](../products/utv/powertrain/architecture.md)
- Relacionado: [Fornecedores](../suppliers/README.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-21 | CACV | Criação inicial |
| 2.0 | 2026-07-22 | CACV | Motor pre definido|
