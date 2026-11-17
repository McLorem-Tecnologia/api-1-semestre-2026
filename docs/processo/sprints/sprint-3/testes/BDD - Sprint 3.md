# Cenários BDD — Sprint 3

**BDD (Behavior-Driven Development)** é uma técnica para escrever critérios de aceitação em linguagem natural, estruturados em três partes: **Dado** (o contexto antes da ação), **Quando** (a ação realizada pelo usuário) e **Então** (o resultado esperado). O objetivo é descrever o comportamento do sistema de forma clara tanto para quem desenvolve quanto para quem não é da área técnica.

Este documento mapeia, no formato **Dado / Quando / Então**, os cenários de teste de cada User Story da Sprint 3 (ranks 11 e 12) e das melhorias técnicas M1 a M4, conforme exigido pela [DoR](../README.md#dor) ("Critérios de Aceitação"). As variações de pergunta a testar estão no [Guia de Testes](./Guia%20de%20Testes%20-%20Sprint%203.md).

---

## Rank 11 — Matérias-primas disponíveis para transferir (líder)

> US-11: Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias.

**Cenário principal**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quais matérias-primas estão disponíveis para transferir para outros setores?"<br>
**Então** a MIA responde com as matérias-primas que têm sobra, separadas por setor, informando a quantidade disponível e a unidade de medida de cada uma, sem incluir o que o próprio setor precisa no dia seguinte

**Cenário: um setor específico**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que tenho sobrando de ingredientes na padaria para transferir?"<br>
**Então** a MIA responde com as matérias-primas com sobra do setor **Padaria**, sob o título do setor, com a quantidade e a unidade de cada uma

**Cenário: uma matéria-prima específica**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quanto de farinha de trigo está disponível para transferir?"<br>
**Então** a MIA responde com a quantidade disponível de farinha de trigo em cada setor que a possui, já descontada a necessidade do dia seguinte

**Cenário: sem sobra**<br>
**Dado** que todo o estoque do setor é necessário para o dia seguinte<br>
**Quando** o líder faz a pergunta acima<br>
**Então** a MIA informa que não há matéria-prima disponível para transferir

---

## Rank 12 — Motivo da transferência de um produto (gerente)

> US-12: Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção.

**Cenário principal**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Por que a coxinha está sendo transferida de setor?"<br>
**Então** a MIA responde com o motivo registrado da transferência, informando o setor de origem, o setor de destino e a data

**Cenário: mais de uma transferência**<br>
**Dado** que o produto tem mais de uma transferência registrada<br>
**Quando** o gerente pergunta o motivo da transferência desse produto<br>
**Então** a MIA apresenta todas as transferências, da mais recente para a mais antiga, cada uma com data, origem, destino e motivo

**Cenário: nome com maiúsculas e minúsculas**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Por que o PÃO FRANCÊS foi transferido?"<br>
**Então** a MIA reconhece o produto e responde como se o nome tivesse sido escrito em minúsculas

**Cenário: sem registro**<br>
**Dado** que o produto não existe ou não tem transferência registrada<br>
**Quando** o gerente faz a pergunta acima<br>
**Então** a MIA informa que não encontrou registro, sem inventar um motivo

---

## M1 — Resposta padronizada por setor

> Toda resposta que lista produtos ou informa valores descartados traz a quantidade (ou o valor) e os setores separados, mesmo quando a pergunta cita um único setor.

**Cenário principal: "quais" e "quantos" têm a mesma resposta**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia as mensagens "Quais produtos devo produzir hoje?" e "Quantos produtos devo produzir hoje?"<br>
**Então** a MIA responde às duas com o mesmo conteúdo: os produtos de todos os setores, separados por setor, cada um com a quantidade e a unidade de medida

**Cenário: um único setor**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quais produtos devo produzir hoje na padaria?"<br>
**Então** a MIA responde com o título do setor **Padaria** e, logo abaixo, os produtos do setor com a quantidade e a unidade de medida de cada um, e não apenas os nomes

**Cenário: um único produto**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quanto de coxinha devo fazer amanhã?"<br>
**Então** a MIA responde somente com a coxinha, com a quantidade e a unidade de medida, sob o título do setor ao qual ela pertence

**Cenário: previsão por período**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que produzir em cada período do dia na padaria?"<br>
**Então** a MIA responde com a manhã, a tarde e a noite no mesmo formato, em ordem cronológica, sob o título do setor **Padaria**

**Cenário: valor descartado por setor**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantos reais foram descartados no dia 01/10/2026?"<br>
**Então** a MIA responde com o valor em R$ de cada setor e com o total geral, que é igual à soma dos setores

**Cenário: áudio**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia uma mensagem de voz dizendo "O que devo produzir hoje na padaria?"<br>
**Então** a MIA responde com o mesmo conteúdo e o mesmo formato que daria à pergunta digitada

---

## M2 — Tratamento de erros

> O bot não fica preso quando algo falha e avisa de forma clara quando não consegue atender a pergunta.

**Cenário: falha da IA**<br>
**Dado** que o modelo de IA está indisponível<br>
**Quando** o usuário envia a mensagem "O que devo produzir hoje?"<br>
**Então** a mensagem "Processando sua solicitação..." é substituída por um aviso amigável de falha, e o bot volta a responder normalmente quando a IA volta

**Cenário: resposta maior que o limite do Telegram**<br>
**Dado** que a resposta tem mais de 4096 caracteres<br>
**Quando** o líder envia a mensagem "Quanta matéria-prima preciso para amanhã?"<br>
**Então** a MIA envia a resposta em mais de uma mensagem, sem cortar um item no meio e sem erro no Telegram

**Cenário: queda de conexão**<br>
**Dado** que a conexão do bot com o Telegram é interrompida por alguns segundos<br>
**Quando** a conexão volta<br>
**Então** o bot volta a responder sem ser reiniciado, e nenhuma mensagem é respondida duas vezes

**Cenário: data inválida**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quanto devo produzir em 31/02/2026?"<br>
**Então** a MIA avisa que não entendeu a data e pede para informá-la de novo, sem mostrar mensagem técnica

**Cenário: período sem histórico**<br>
**Dado** que não há vendas registradas para o período pedido (ex.: madrugada)<br>
**Quando** o líder pergunta o que produzir nesse período<br>
**Então** a MIA informa qual período foi usado no cálculo (ex.: a noite, que é o mais próximo), sem inventar produtos

**Cenário: setor inexistente**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "O que devo produzir hoje na floricultura?"<br>
**Então** a MIA informa que não encontrou o setor, sem inventar produtos

**Cenário: data sem registros de descarte**<br>
**Dado** que o gerente está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quantos reais foram descartados em 01/01/2020?"<br>
**Então** a MIA informa que não há registros de descarte nessa data

**Cenário: arquivo de dados ausente**<br>
**Dado** que um arquivo da pasta `dados/` não existe<br>
**Quando** o bot é iniciado<br>
**Então** o terminal informa qual arquivo não foi encontrado, em vez de um erro técnico sem contexto

---

## M3 — Limpeza do código

> Remoção do que deixou de ser necessário, sem mudar o comportamento das funcionalidades já entregues.

**Cenário principal: sem tratamento separado de "quais" e "quantos"**<br>
**Dado** que o código do projeto foi revisado<br>
**Quando** se procura pelo parâmetro `tipo_pergunta` nas tools<br>
**Então** nenhuma ocorrência é encontrada, e a pergunta "quais produtos devo produzir?" é respondida como a pergunta "quantos?"

**Cenário: terminal sem logs de depuração**<br>
**Dado** que o bot está em execução<br>
**Quando** o líder envia qualquer pergunta<br>
**Então** o terminal não mostra logs de depuração, apenas os erros e o tempo de processamento

**Cenário: valores do descarte preservados**<br>
**Dado** que o cálculo do custo do descarte foi movido para `services.desperdicio`<br>
**Quando** o gerente envia a mensagem "Quantos reais foram descartados em 07/04/2026 na empresa toda?"<br>
**Então** a MIA responde com o mesmo total registrado no Relatório de Testes da Sprint 2 (R$ 543,59)

**Cenário: previsão de produção preservada**<br>
**Dado** que o formatador das respostas foi unificado<br>
**Quando** o líder envia a mensagem "Quantos produtos devo produzir no dia 26/10/2026 na padaria?"<br>
**Então** a MIA responde com as mesmas quantidades registradas no Relatório de Testes da Sprint 2

---

## M4 — Correções da matéria-prima (US10)

> Matéria-prima para o dia seguinte com quantidade e unidade corretas e resposta mais enxuta.

**Cenário principal**<br>
**Dado** que o líder está conversando com a MIA pelo Telegram<br>
**Quando** ele envia a mensagem "Quanta matéria-prima preciso deixar preparada para amanhã na padaria?"<br>
**Então** a MIA responde com cada produto da **Padaria** uma única vez e, logo abaixo, os ingredientes com a quantidade e a unidade de medida correta (kg ou g, L ou mL, un), sem mostrar a sobra em estoque

**Cenário: ingrediente fracionado**<br>
**Dado** que um produto usa um ingrediente em pequena quantidade por unidade (ex.: 0,1 kg)<br>
**Quando** o líder faz a pergunta acima<br>
**Então** a quantidade do ingrediente é a previsão do produto × a quantidade na receita, exibida em g ou mL quando for menor que 1, sem arredondar para zero

**Cenário: estoque insuficiente**<br>
**Dado** que o estoque do setor não cobre a necessidade de um ingrediente<br>
**Quando** o líder faz a pergunta acima<br>
**Então** a MIA sinaliza o ingrediente como insuficiente, informando a quantidade necessária e a disponível, com a unidade de medida

**Cenário: produto sem receita**<br>
**Dado** que um produto da previsão não tem consumo de matéria-prima cadastrado<br>
**Quando** o líder faz a pergunta acima<br>
**Então** a MIA informa quais produtos ficaram sem receita, sem inventar o consumo
