---
title: Roadmap Estratégico
id: ROOT-ROADMAP
status: active
revision: "1.0"
owner: fundador
created: "2026-07-21"
updated: "2026-07-21"
related:
  - README.md
  - /roadmap/product/README.md
  - /roadmap/company/README.md
  - /roadmap/technology/README.md
tags: [roadmap, strategy, planning]
---

# Roadmap Estratégico

Este documento apresenta o roadmap de alto nível da empresa e dos produtos.  
Para detalhes, consulte o diretório [/roadmap](./roadmap/README.md).

---

## Visão Geral

```mermaid
gantt
    title Roadmap Estratégico — UTV Startup
    dateFormat  YYYY-MM
    section Fundação
    Estrutura do repositório        :done,    rep,  2026-07, 2026-08
    Definição de requisitos UTV     :active,  req,  2026-08, 2026-10
    Arquitetura do sistema          :         arch, 2026-10, 2026-12
    section Engenharia Conceitual
    CAD conceitual — Chassis        :         cad1, 2027-01, 2027-04
    CAD conceitual — Suspensão      :         cad2, 2027-03, 2027-06
    BOM inicial                     :         bom1, 2027-04, 2027-06
    section Prototipagem
    Protótipo #1 — Chassis          :         prt1, 2027-07, 2027-12
    Testes estruturais iniciais     :         tst1, 2027-10, 2028-02
    section Validação
    Protótipo #2 — Sistema completo :         prt2, 2028-01, 2028-06
    Campanha de testes              :         tst2, 2028-06, 2028-12
    section Homologação
    Processo DENATRAN/INMETRO       :         hom,  2029-01, 2029-12
    section Comercialização
    Lançamento UTV v1.0             :         launch, 2030-01, 2030-06
```

---

## Fases do Produto UTV

### Fase 0 — Fundação (2026)
- [x] Criar repositório PLM
- [x] Definir filosofia de engenharia
- [ ] Documentar missão e visão
- [ ] Iniciar sistema de requisitos

### Fase 1 — Conceitual (2026–2027)
- [ ] REQ: levantar todos os requisitos do UTV
- [ ] ARQ: definir arquitetura do sistema
- [ ] CAD: modelos conceituais dos sistemas principais
- [ ] BOM: lista preliminar de componentes

### Fase 2 — Detalhamento (2027–2028)
- [ ] CAD: projeto detalhado de todos os sistemas
- [ ] SIM: simulações estruturais e dinâmicas
- [ ] BOM: BOM definitiva com fornecedores
- [ ] DES: desenhos técnicos completos

### Fase 3 — Prototipagem (2027–2028)
- [ ] Fabricação do protótipo #1
- [ ] Testes funcionais
- [ ] Iterações e correções
- [ ] Protótipo #2 validado

### Fase 4 — Homologação (2029)
- [ ] Documentação para DENATRAN
- [ ] Ensaios INMETRO
- [ ] Homologação completa

### Fase 5 — Comercialização (2030+)
- [ ] Lançamento comercial
- [ ] Estrutura de pós-venda
- [ ] Expansão da linha de produtos

---

## Produtos Futuros

```mermaid
timeline
    title Linha de Produtos
    2030 : UTV Utilitário v1.0
    2031 : Carreta Homologada v1.0
    2032 : Implementos Agrícolas
    2033 : Plataforma Modular Gen2
    2034 : Novos Veículos Utilitários
```

---

## Links Relacionados

- [Roadmap de Produto](./roadmap/product/README.md)
- [Roadmap da Empresa](./roadmap/company/README.md)
- [Roadmap Tecnológico](./roadmap/technology/README.md)
- [Roadmap de Industrialização](./roadmap/industrialization/README.md)
- [Decisões Estratégicas](./products/utv/decisions/README.md)
