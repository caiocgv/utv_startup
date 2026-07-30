---
title: Ferramentas de Análise de Suspensão e Software CAD 3D
id: ADR-0009
status: accepted
revision: "1.0"
owner: fundador
created: "2026-07-30"
updated: "2026-07-30"
related:
  - /decisions/README.md
  - /decisions/ADR-0004-suspensao.md
  - /requirements/REQ-0004.md
tags: [adr, suspensao, cad, ferramentas, analise-geometrica, fusion360]
---

# ADR-0009 — Ferramentas de Análise de Suspensão e Software CAD 3D

## Status

✅ **Aceito**

---

## Contexto

O desenvolvimento do sistema de suspensão do UTV exige tanto análise geométrica precisa quanto modelagem 3D completa. São necessárias ferramentas acessíveis para:

1. **Análise de geometria de suspensão**: calcular parâmetros como camber, caster, toe, variação de bitola e centro de rolagem ao longo do curso da suspensão.
2. **Modelagem 3D**: criar e validar componentes estruturais e de suspensão antes da fabricação.

A escolha de ferramentas define a qualidade do projeto, a curva de aprendizado da equipe e o custo de desenvolvimento.

---

## Alternativas Consideradas

### Análise de Geometria de Suspensão

| Ferramenta | Custo | Facilidade de Uso | Profundidade de Análise | Acesso |
|------------|-------|-------------------|------------------------|--------|
| **Racing Aspirations MacPherson Calculator** | **Gratuito** | **Alta** | **Adequada para suspensão McPherson** | **Web (online)** |
| OptimumKinematics | Pago | Média | Muito Alta | Desktop |
| Lotus Suspension Analysis | Pago | Baixa | Alta | Desktop |
| Análise manual (planilhas) | Gratuito | Baixa | Limitada | Local |

### Software CAD 3D

| Software | Custo | Curva de Aprendizado | Recursos | Integração |
|----------|-------|---------------------|----------|------------|
| **Autodesk Fusion 360** | **Gratuito (startup/personal)** | **Média** | **CAD + CAM + Simulação** | **Excelente** |
| FreeCAD | Gratuito | Alta | CAD básico | Limitada |
| SolidWorks | Muito Alto | Média | Completo | Excelente |
| Onshape | Freemium | Média | CAD + colaboração | Boa |

---

## Decisão

1. **Análise de geometria de suspensão**: utilizar a calculadora online **Racing Aspirations MacPherson Geometry Calculator** (https://www.racingaspirations.com/apps/macpherson-geometry-calculator/) como ferramenta principal para análise e validação da geometria de suspensão McPherson.

2. **Modelagem CAD 3D**: adotar o **Autodesk Fusion 360** como software principal de modelagem 3D, CAM e simulação para todos os componentes do UTV.

---

## Justificativa

### Racing Aspirations MacPherson Calculator

1. **Gratuito e acessível** — ferramenta web sem necessidade de instalação ou licença
2. **Específico para McPherson** — projetado para a geometria exata utilizada na suspensão traseira do projeto (ADR-0004)
3. **Análise rápida** — permite iteração ágil de parâmetros geométricos (camber, caster, kingpin, scrub radius)
4. **Visualização clara** — fornece representação gráfica da geometria para validação visual
5. **Integração com o projeto** — compatível com a decisão de usar suspensão McPherson traseira derivada do VW Gol

### Autodesk Fusion 360

1. **Gratuito para startups e uso pessoal** — licença sem custo para empresas com faturamento abaixo do limite da Autodesk
2. **Plataforma integrada** — combina CAD, CAM, simulação FEA e colaboração em um único ambiente
3. **Amplamente adotado** — grande comunidade, tutoriais e suporte disponíveis
4. **Nativo em nuvem** — backup automático e acesso multiplataforma
5. **Exportação flexível** — suporte a múltiplos formatos (STEP, IGES, STL, DXF) para comunicação com fornecedores e manufatura
6. **Simulação estrutural integrada** — permite validação de componentes críticos (braços de suspensão, hubs) sem software adicional

---

## Consequências

### Positivas
- Custo zero de licenciamento para ambas as ferramentas na fase inicial
- Análise geométrica de suspensão com ferramenta especializada e validada pela comunidade automotiva
- Modelo 3D completo do UTV em Fusion 360 como base para fabricação (CAM), documentação e comunicação com fornecedores
- Redução de retrabalho por validação geométrica antes da fabricação
- Capacidade de simular e validar componentes estruturalmente críticos

### Negativas
- Dependência de conexão à internet para uso da calculadora MacPherson (ferramenta web)
- Fusion 360 pode ter custos de licença no futuro conforme a empresa cresce além do limite de faturamento
- Curva de aprendizado do Fusion 360 para usuários sem experiência prévia em CAD

### Riscos
- Mudança nos termos de uso do Fusion 360 pode impactar custos futuros (mitigado: exportação para formatos abertos STEP/IGES preserva acesso ao modelo)
- A calculadora MacPherson cobre apenas suspensão do tipo McPherson; análises da suspensão dianteira duplo A podem requerer ferramenta adicional

---

## Relacionamentos

- Gerado por: [Issue #15 — document calculator as possible solution for suspension analysis](https://github.com/caiocgv/utv_startup/issues/15)
- Relacionado: [ADR-0004 — Sistema de Suspensão Independente](./ADR-0004-suspensao.md)
- Relacionado: [ADR-0001 — Repositório GitHub como PLM Simplificado](./ADR-0001-repositorio-plm.md)

---

## Referências

- Racing Aspirations MacPherson Geometry Calculator: https://www.racingaspirations.com/apps/macpherson-geometry-calculator/
- Autodesk Fusion 360: https://www.autodesk.com/products/fusion-360/

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-30 | Copilot | Criação inicial — documenta calculadora MacPherson e Fusion 360 |
