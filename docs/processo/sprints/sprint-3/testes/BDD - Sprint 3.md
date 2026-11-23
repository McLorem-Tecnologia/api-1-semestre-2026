# Cenários BDD — Sprint 3 (regressão completa)

Este documento reúne os cenários de aceitação das User Stories 01 a 10 das Sprints 1 e 2 e os cenários das US-11 e US-12 revisados para as mudanças de matéria-prima desta Sprint. Os cenários descrevem o comportamento esperado e não representam resultados executados.

---

## Menu de ajuda do TeleBot

**Cenário: abrir o menu**
**Dado** que a pessoa está conversando com a MIA no Telegram
**Quando** envia `/ajuda` ou `/help`
**Então** a MIA apresenta opções de Produção, Matéria-prima, Descarte, Produtos, Vendas e perguntas por áudio

**Cenário: executar uma pergunta do menu**
**Dado** que o menu de ajuda está aberto
**Quando** a pessoa escolhe um assunto e toca em uma pergunta de exemplo
**Então** a MIA processa a pergunta pelo mesmo fluxo das mensagens de texto e mostra uma resposta com opção de voltar ao menu

**Cenário: usar as mesmas perguntas por voz**
**Dado** que a pessoa escolhe uma pergunta de exemplo
**Quando** grava essa pergunta como mensagem de voz
**Então** a MIA transcreve e consulta a mesma funcionalidade; previsões de produção sempre incluem quantidades

---

## Rank 1 — Quais produtos devem ser produzidos

> US-01: Eu, como líder, quero saber quais produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.

**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que devo produzir hoje?"<br>
**Então** a MIA responde com a lista dos produtos recomendados para produção hoje e as quantidades, calculadas com base na média histórica do perfil do dia

---

## Rank 2 — Quantos produtos produzir

> US-02: Eu, como líder, quero saber quantos produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.

**Dado** que o gestor está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantas unidades devo produzir hoje?"<br>
**Então** a MIA responde com a lista dos produtos e suas quantidades recomendadas; o resultado segue o mesmo comportamento da pergunta "O que devo produzir hoje?"

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

---

## Rank 11 — Matérias-primas disponíveis para transferir (líder)

> US-11: Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias.

**Cenário principal**
**Dado** que há matéria-prima em estoque acima da necessidade prevista de um setor
**Quando** o líder pergunta "Quais matérias-primas estão disponíveis para transferir para outros setores?"
**Então** a MIA informa ingrediente, unidade, quantidade disponível e setor de origem, sem contar a quantidade necessária para a produção prevista daquele setor

**Cenário: setor de origem informado**
**Dado** que há sobras em mais de um setor
**Quando** o líder pede para considerar as sobras da Padaria
**Então** a MIA lista somente as sobras da Padaria como fontes para transferência

**Cenário: sem sobra disponível**
**Dado** que todo o estoque é necessário para atender à produção prevista
**Quando** o líder pergunta quais matérias-primas estão disponíveis para transferir
**Então** a MIA informa que nenhuma transferência pode ser recomendada

**Cenário: histórico ou receita ausente**
**Dado** que não há histórico compatível ou receita cadastrada para um produto previsto
**Quando** o líder consulta as sobras
**Então** a MIA informa que não foi possível calcular ou identifica os produtos sem receita, sem inventar necessidade

---

## Rank 12 — Recomendação de transferência de matéria-prima (gerente)

> US-12: Eu, como gerente, quero identificar transferências de matéria-prima recomendadas entre setores, a fim de cobrir déficits sem comprometer a necessidade do setor de origem.

**Cenário principal**
**Dado** que um setor tem sobra de um ingrediente após sua necessidade prevista e outro setor tem déficit do mesmo ingrediente
**Quando** o gerente pergunta quais transferências são recomendadas
**Então** a MIA informa ingrediente, unidade, quantidade, setor de origem, setor de destino e a justificativa baseada na sobra e no déficit

**Cenário: transferência parcial**
**Dado** que a sobra da origem não cobre todo o déficit do destino
**Quando** a MIA calcula a recomendação
**Então** recomenda somente a quantidade disponível e informa o déficit que permanece

**Cenário: nenhuma transferência necessária**
**Dado** que não há setor com déficit ou não há sobra compatível
**Quando** o gerente consulta as transferências recomendadas
**Então** a MIA informa que nenhuma transferência foi recomendada

**Cenário: estoque preservado**
**Dado** que a MIA apresenta uma recomendação de transferência
**Quando** a consulta termina
**Então** os estoques registrados permanecem inalterados

---
