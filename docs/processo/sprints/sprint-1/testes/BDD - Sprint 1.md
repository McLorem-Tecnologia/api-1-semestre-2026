# Cenários BDD — Sprint 1

**BDD (Behavior-Driven Development)** é uma técnica para escrever critérios de aceitação em linguagem natural, estruturados em três partes: **Dado** (o contexto antes da ação), **Quando** (a ação realizada pelo usuário) e **Então** (o resultado esperado). O objetivo é descrever o comportamento do sistema de forma clara tanto para quem desenvolve quanto para quem não é da área técnica.

Este documento mapeia, no formato **Dado / Quando / Então**, o cenário de teste básico de cada User Story da Sprint 1, conforme exigido pela [DoR](./../../../../../README.md) ("Critérios de Aceitação"). Para todas as variações de pergunta testadas e os resultados obtidos na execução, ver o [Relatório de Testes](./Relatório%20de%20Testes%20-%20Sprint%201.md).

---

## Rank 1 — Quais produtos devem ser produzidos

> US-01: Eu, como líder, quero saber quais produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.

**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que devo produzir hoje?"<br>
**Então** a MIA responde com a lista de **nomes** dos produtos recomendados para produção hoje, sem quantidades, calculada com base na média de vendas de dias com o mesmo perfil (bom/ruim) do dia atual

---

## Rank 2 — Quantos produtos produzir

> US-02: Eu, como líder, quero saber quantos produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.

**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantas unidades devo produzir hoje?"<br>
**Então** a MIA responde com a lista de produtos **e** a quantidade recomendada para cada um, calculada pela média histórica arredondada para cima

---

## Rank 3 — O que foi produzido

> US-03: Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y.

**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que foi produzido ontem na padaria?"<br>
**Então** a MIA responde com a lista de produtos do setor Padaria, mostrando o Total Produzido, as Vendas e o Descarte de cada item

---

## Rank 4 — O que deveria ter sido produzido

> US-04: Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de consultar a meta ideal de produção estipulada para a data.

**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que deveria ter sido produzido ontem na padaria?"<br>
**Então** a MIA responde com a meta de produção por produto da Padaria, em tom de relatório/cobrança
