---
title: Repositório GitHub como PLM Simplificado
id: ADR-0001
status: accepted
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - /products/utv/decisions/README.md
  - /README.md
tags: [adr, plm, github, tooling, infrastructure]
---

# ADR-0001 — Repositório GitHub como PLM Simplificado

## Status

✅ **Aceito**

---

## Contexto

Precisamos de um sistema para gerenciar todo o ciclo de vida do produto: requisitos, engenharia, CAD, BOM, testes, qualidade e documentação. As opções comerciais de PLM (Siemens Teamcenter, PTC Windchill, etc.) têm custo muito elevado e são inadequadas para o estágio inicial da empresa. A empresa está em fase inicial, operada por uma única pessoa, com baixo investimento disponível.

---

## Alternativas Consideradas

| Alternativa | Custo | Complexidade | Rastreabilidade | Colaboração |
|-------------|-------|--------------|-----------------|-------------|
| PLM Comercial (Teamcenter) | 💰💰💰 | Alta | Excelente | Excelente |
| PLM Open Source (OpenPLM) | 💰 | Muito Alta | Boa | Boa |
| ERP + Docs internos | 💰💰 | Alta | Média | Média |
| **GitHub + Markdown** | **Grátis** | **Baixa** | **Boa** | **Excelente** |
| Notion/Confluence | 💰 | Baixa | Baixa | Boa |

---

## Decisão

Usar o repositório **GitHub com Markdown, Mermaid e arquivos de engenharia** como PLM simplificado.

---

## Justificativa

1. **Custo zero** — GitHub gratuito para repositório público ou privado de pequeno time
2. **Rastreabilidade nativa** — Git oferece histórico completo de todas as mudanças
3. **Colaboração** — Pull Requests, Issues, Projects, Discussions integrados
4. **Padronização** — Templates em Markdown garantem consistência
5. **Simplicidade** — Qualquer pessoa com conhecimento básico pode contribuir
6. **Escalabilidade** — Funciona para 1 pessoa e escala para uma equipe
7. **Diagramas** — Mermaid permite criar fluxogramas e arquiteturas diretamente no Markdown
8. **Independência de ferramentas** — Sem dependência de software pago

---

## Consequências

### Positivas
- Custo zero de infraestrutura
- Rastreabilidade completa via commits
- Acesso de qualquer dispositivo com internet
- Backup automático pelo Git

### Negativas
- Não substitui CAD (FreeCAD será utilizado separadamente)
- Não tem gestão de configuração nativa de CAD
- Funcionalidades PLM avançadas ausentes (como gestão de ECO automatizada)

### Riscos
- Dependência do GitHub (mitigado: repositório pode ser migrado)
- Escalabilidade limitada para grandes equipes com muito CAD

---

## Relacionamentos

- Habilita: [README.md](../../../README.md)
- Relacionado: [ADR-0002](./ADR-0002-chassis-tubular.md)
- Relacionado: [ADR-0003](./ADR-0003-motor-nacional.md)

---

## Histórico

| Rev | Data | Autor | Descrição |
|-----|------|-------|-----------|
| 1.0 | 2026-07-21 | Fundador | Criação inicial |
