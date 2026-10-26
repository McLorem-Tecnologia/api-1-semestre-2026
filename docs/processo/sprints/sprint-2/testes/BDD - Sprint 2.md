# Cenários BDD — Sprint 2

**BDD (Behavior-Driven Development)** é uma técnica para escrever critérios de aceitação em linguagem natural, estruturados em três partes: **Dado** (o contexto antes da ação), **Quando** (a ação realizada pelo usuário) e **Então** (o resultado esperado). O objetivo é descrever o comportamento do sistema de forma clara tanto para quem desenvolve quanto para quem não é da área técnica.

Este documento mapeia, no formato **Dado / Quando / Então**, os cenários de teste de cada User Story da Sprint 2 (que reúne as histórias das antigas Sprints 2 e 3), conforme exigido pela [DoR](../README.md#dor) ("Critérios de Aceitação"). As variações de pergunta a testar estão no [Guia de Testes](./Guia%20de%20Testes%20-%20Sprint%202.md).

---

## Rank 5 — O que produzir em cada período do dia (líder)

> US-05: Eu, como líder, quero saber quais produtos devo produzir em cada período do dia, a fim de otimizar o tempo dos colaboradores.

**Cenário principal**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que eu devo produzir de manhã na padaria?"<br>
**Então** a MIA responde com os produtos do setor **Padaria** a produzir no período da **manhã**, com a quantidade de cada um

**Cenário: todos os períodos**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que produzir em cada período do dia na padaria?"<br>
**Então** a MIA responde com os produtos e quantidades separados por período (manhã, tarde e noite), e os valores de cada período são coerentes com a previsão do dia

**Cenário: mais de um período**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que devo produzir à tarde e à noite na padaria?"<br>
**Então** a MIA responde com cada produto da **Padaria** e as quantidades de tarde e de noite, sem incluir a manhã

**Cenário: período sem histórico**<br>
**Dado** que não há vendas registradas para o período pedido (ex.: madrugada)<br>
**Quando** o líder pergunta o que produzir nesse período<br>
**Então** a MIA informa o período usado no cálculo (ex.: a noite, que é o mais próximo) ou avisa que não encontrou histórico, sem inventar produtos

---

## Rank 6 — Reais descartados em cada setor (gerente)

> US-06: Eu, como gerente, quero saber quantos reais foram descartados em cada setor, a fim de monitorar o impacto financeiro das perdas dos setores.

**Cenário principal**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantos reais foram descartados no dia 01/10/2026 em cada setor?"<br>
**Então** a MIA responde com o valor em R$ descartado em cada setor na data informada (custo dos ingredientes × quantidade descartada) e, se apresentar um total geral, ele é igual à soma dos setores

**Cenário: um setor específico**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantos reais foram descartados no dia 01/10/2026 na padaria?"<br>
**Então** a MIA responde com o valor total em R$ do setor **Padaria** na data informada

**Cenário: pergunta em unidades**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantas unidades foram descartadas ontem?"<br>
**Então** a MIA responde em **unidades**, sem converter para R$

---

## Rank 7 — Reais descartados na empresa (gerente)

> US-07: Eu, como gerente, quero saber quantos reais foram descartados, a fim de avaliar o custo global de desperdício da empresa.

**Cenário principal**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantos reais foram descartados em 07/04/2026 na empresa toda?"<br>
**Então** a MIA responde com o valor total em R$ descartado por **todos os setores** na data informada, igual à soma dos valores obtidos setor a setor

**Cenário: separado por setores**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantos reais foram descartados no dia 01/10/2026? Separe por setores"<br>
**Então** a MIA responde com o total geral e o valor de cada setor, agrupados

---

## Rank 8 — Produtos mais lucrativos na empresa (gerente)

> US-08: Eu, como gerente, quero saber quais produtos me trazem mais lucro, a fim de orientar estrategicamente os setores.

**Cenário principal**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quais produtos da empresa trazem mais lucro?"<br>
**Então** a MIA responde com o ranking dos produtos de **todos os setores**, do mais para o menos lucrativo, indicando o setor e o lucro em R$ de cada item

**Cenário: ranking limitado**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Me mostra os 5 produtos mais lucrativos do mercado"<br>
**Então** a MIA responde com o ranking limitado aos **5** produtos mais lucrativos, em ordem decrescente de lucro

---

## Rank 9 — Perguntas por áudio (gestor)

> US-09: Eu, como gestor, quero interagir com o assistente de análise de dados enviando perguntas por áudio, a fim de obter insights das planilhas de forma fluida e sem contato manual (semelhante a uma Alexa).

**Cenário principal**<br>
**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia uma mensagem de voz dizendo "O que devo produzir hoje?"<br>
**Então** a MIA transcreve o áudio e responde com o mesmo conteúdo que daria à pergunta digitada, sem exigir nenhum contato manual com o teclado

**Cenário: áudio inválido**<br>
**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia um áudio vazio, com ruído ou acima da duração máxima<br>
**Então** a MIA responde com uma mensagem amigável pedindo para tentar de novo, sem travar o bot

---

## Rank 10 — Matéria-prima para o dia seguinte (líder)

> US-10: Eu, como líder, quero saber quanta matéria-prima eu preciso deixar preparada para o dia seguinte, a fim de otimizar o tempo e reduzir o desperdício de matéria-prima.

**Cenário principal**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quanta matéria-prima preciso deixar preparada para amanhã na padaria?"<br>
**Então** a MIA responde com a lista de matérias-primas do setor **Padaria**, com a quantidade e a unidade de cada uma, calculada a partir da previsão de produção de amanhã e do consumo de cada produto

**Cenário: produto sem receita**<br>
**Dado** que um produto da previsão não tem consumo de matéria-prima cadastrado<br>
**Quando** o líder faz a pergunta acima<br>
**Então** a MIA informa quais produtos ficaram sem receita, sem inventar o consumo

---

## Rank 11 — Matérias-primas disponíveis para transferir (líder)

> US-11: Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias.

> **Não entregue na Sprint 2:** história da previsão (sem compromisso de entrega) que passa para a Sprint 3.

**Cenário principal**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quais matérias-primas estão disponíveis para transferir para outros setores?"<br>
**Então** a MIA responde com as matérias-primas que têm sobra, informando a quantidade e o setor que as possui, sem incluir o que o próprio setor precisa no dia seguinte

**Cenário: sem sobra**<br>
**Dado** que todo o estoque do setor é necessário para o dia seguinte<br>
**Quando** o líder faz a pergunta acima<br>
**Então** a MIA informa que não há matéria-prima disponível para transferir

---

## Rank 12 — Motivo da transferência de um produto (gerente)

> US-12: Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção.

> **Não entregue na Sprint 2:** história da previsão (sem compromisso de entrega) que passa para a Sprint 3.

**Cenário principal**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Por que a coxinha está sendo transferida de setor?"<br>
**Então** a MIA responde com o motivo registrado da transferência, informando o setor de origem, o setor de destino e a data

**Cenário: sem registro**<br>
**Dado** que o produto não existe ou não tem transferência registrada<br>
**Quando** o gerente faz a pergunta acima<br>
**Então** a MIA informa que não encontrou registro, sem inventar um motivo

---
