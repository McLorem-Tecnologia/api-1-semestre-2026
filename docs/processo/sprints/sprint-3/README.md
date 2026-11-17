# Documentação - Sprint 3

<div align="center">
  <!-- Imagem que aparece apenas no Modo Escuro -->
  <img src="../../../img/logo-mclorem-dark.png#gh-dark-mode-only" alt="logo da McLorem Tecnologia" width="200">
  
  <!-- Imagem que aparece apenas no Modo Claro -->
  <img src="../../../img/logo-mclorem-light.png#gh-light-mode-only" alt="logo da McLorem Tecnologia" width="200">
  
  <h3>MIA - Assistente de Análise de Dados</h3>
</div>

<br>

<p align="center">
  <a href ="#desafio"> Desafio</a> &nbsp;&bull;&nbsp;
  <a href ="#us"> User Stories</a> &nbsp;&bull;&nbsp;
  <a href ="#melhorias"> Melhorias Técnicas</a> &nbsp;&bull;&nbsp;
  <a href ="#dor">DoR</a> &nbsp;&bull;&nbsp;
  <a href ="#dod">DoD</a>
</p>

---

> [!IMPORTANT]
> **Status da Sprint:**  Não Iniciado 🔜<br>
> **Relatório de Testes da Sprint:** [Link](./testes/Relatório%20de%20Testes%20-%20Sprint%203.md)<br>
> **Vídeo da Sprint:** [Youtube]()

## 🏅 Desafio <a id="desafio"></a>

Fechar o backlog da MIA entregando as duas últimas User Stories, que ficaram de fora da Sprint 2: saber quais matérias-primas sobram em um setor e podem ser transferidas a outros (US11) e saber por que um produto está sendo transferido de setor (US12). Para isso, a MIA passa a cruzar a necessidade prevista de matéria-prima com o estoque de cada setor e a consultar um registro de transferências, com o motivo de cada uma, sempre por linguagem natural no Telegram.

Em paralelo, a Sprint é dedicada a consolidar o que já existe. A resposta é padronizada e passa a trazer sempre a quantidade e os setores separados, mesmo quando a pergunta cita um único setor. O tratamento de erros do bot e da IA é reforçado, o cálculo da matéria-prima é corrigido e o código que deixou de ser necessário é removido, como o tratamento separado das perguntas "quais" e "quantos". Toda a inteligência e o processamento continuam operando de forma autônoma, sem persistência de dados e sem APIs externas de terceiros.

## 📋 User Stories <a id="us"></a>

| $\textsf{\textbf{Capacidade estimada da Equipe por Sprint:}}$ | $\textsf{21 Story Points}$                                         |
| ------------------------------------------------------------- | ------------------------------------------------------------------ |
| $\color{#2e8b57}{\textsf{\textbf{Meta da Sprint:}}}$          | $\textsf{User Stories de rank 11 e 12 (\textit{21 Story Points})}$ |
| $\textsf{\textbf{Melhorias técnicas da Sprint:}}$             | $\textsf{M1 a M4 (\textit{sem Story Points})}$                     |

|              Rank              |            Prioridade             | User Story                                                                                                                                                                                                | Story Points                   | Sprint                        |            Status             |
| :----------------------------: | :-------------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------: | :---------------------------: | :---------------------------: |
| $\color{#2e8b57}{\textsf{11}}$ | $\color{#2e8b57}{\textsf{Baixa}}$ | $\color{#2e8b57}{\textsf{Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias.}}$ | $\color{#2e8b57}{\textsf{13}}$ | $\color{#2e8b57}{\textsf{3}}$ | $\color{#2e8b57}{\textsf{⌛}}$ |
| $\color{#2e8b57}{\textsf{12}}$ | $\color{#2e8b57}{\textsf{Baixa}}$ | $\color{#2e8b57}{\textsf{Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção.}}$                          | $\color{#2e8b57}{\textsf{8}}$  | $\color{#2e8b57}{\textsf{3}}$ | $\color{#2e8b57}{\textsf{⌛}}$ |

> [!NOTE]
> A Sprint 3 entrega as histórias de **rank 11 e 12**, que já eram desta Sprint no backlog original e não foram entregues na Sprint 2. Além delas, a Sprint reúne as **melhorias técnicas M1 a M4**, que não têm Story Points. Com a **M1**, a resposta à pergunta "quais produtos devo produzir?" (**US01**) passa a ser a mesma da pergunta "quantos?" (**US02**): o que a US01 entrega continua atendido, só que sem um tratamento separado no código.

## 🛠️ Melhorias Técnicas <a id="melhorias"></a>

| ID  | Melhoria                              | Descrição                                                                                                                                                                                                                                                                                                  | Status |
| :-: | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----: |
| M1  | Resposta padronizada por setor        | Toda resposta que lista produtos (previsão do dia, meta, produção real, previsão por período e matéria-prima) e a que informa o valor descartado passam a trazer a quantidade (ou o valor) e os setores separados, mesmo quando a pergunta cita um único setor. As perguntas "quais" e "quantos" têm a mesma resposta. |   ⌛   |
| M2  | Tratamento de erros                   | O bot não fica preso na mensagem "Processando..." quando algo falha, reconecta sozinho quando a conexão cai, divide as respostas maiores que o limite do Telegram e avisa de forma clara quando a data, o setor, o período ou o arquivo de dados não pode ser usado.                                       |   ⌛   |
| M3  | Limpeza do código                     | Remoção do que deixou de ser necessário: o tratamento separado de "quais" e "quantos" (parâmetro `tipo_pergunta`), os logs de depuração e o código sem uso. O cálculo do custo do descarte passa a ficar em um único *service*, fora da tool.                                                               |   ⌛   |
| M4  | Correções da matéria-prima (US10)     | Quantidade correta para ingredientes fracionados, unidade de medida correta de cada ingrediente (kg, g, L, mL ou un), produto exibido uma única vez com seus ingredientes logo abaixo e resposta mais enxuta, sem a sobra em estoque (que passa a ser consultada na US11).                                  |   ⌛   |

---

## 🏅 DoR - Definition of Ready <a id="dor"></a>

A avaliação detalhada de DoR e DoD, User Story por User Story e melhoria por melhoria, está em [`Checklist - Sprint 3`](./Checklist%20-%20Sprint%203.md). Os cenários de aceitação estão no [`BDD - Sprint 3`](./testes/BDD%20-%20Sprint%203.md).

| Critério                      | Descrição                                                                                                                                                                                              |
| :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Clareza na Descrição**      | A User Story está escrita no formato: "Eu, como [papel], quero [ação], a fim de [objetivo/valor]". As melhorias técnicas descrevem o comportamento esperado.                                           |
| **Critérios de Aceitação**    | A história possui critérios claros e pelo menos um cenário de teste básico (BDD) mapeado (Dado que... Quando... Então...).                                                                             |
| **Independente**              | A história pode ser desenvolvida sem depender de tarefas bloqueantes dentro da mesma Sprint. Quando houver dependência (ex.: a US11 depende da US10 e da M4), ela está identificada.                   |
| **Compreensão Compartilhada** | A equipe entende o propósito e estimou o esforço da tarefa (Story Points definidos nas User Stories).                                                                                                  |
| **Mapeamento de Intenções**   | Estão documentados exemplos reais de frases em linguagem natural que o usuário pode enviar (ex: "quais matérias-primas posso transferir?", "por que a coxinha foi transferida?").                       |
| **Dados Disponíveis**         | Está definido qual arquivo e coluna dos CSVs estáticos serão lidos, e os dados que ainda não existem na base (ex.: registro de transferências com o motivo) têm origem combinada.                      |
| **Critérios Técnicos**        | Está definido o que o modelo via **DSPy** precisará extrair da frase (parâmetros) e qual regra o **Pandas** deverá aplicar.                                                                            |
| **Tarefa Registrada**         | A tarefa tem um código no Jira (`MT-XX`), usado para nomear a branch e os commits, conforme a [Estratégia de Branch](../../Estratégia%20de%20Branch.md).                                                |

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério                         | Descrição                                                                                                                                                                       |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Critérios Atendidos**          | Todos os critérios de aceitação e cenários de teste da User Story ou da melhoria foram cumpridos e validados com sucesso.                                                       |
| **Interpretação Validada (NLP)** | A IA interpretou corretamente diferentes variações da mesma pergunta, em texto ou em áudio, acionando a regra correta.                                                          |
| **Resposta Padronizada**         | A resposta traz a quantidade (ou o valor) e os setores separados, mesmo quando a pergunta cita um único setor.                                                                  |
| **Tratamento de Erros**          | Entradas inválidas, falta de dados e falhas de rede, do Telegram ou da IA geram uma mensagem amigável, sem travar o bot nem deixar a mensagem em "Processando...".             |
| **Código Revisado**              | O código passou por Code Review (Pull Request da branch da tarefa, revisado e aprovado por pelo menos um outro membro da equipe).                                               |
| **Testes Registrados**           | Os casos do Guia de Testes foram executados e registrados no Relatório de Testes, sem falhas pendentes.                                                                         |
| **Documentação Atualizada**      | As novas capacidades do bot, os mapeamentos dos CSVs estáticos e a arquitetura foram atualizados na documentação.                                                               |
| **Integração Validada**          | A nova capacidade de resposta não confunde a IA em relação a outras perguntas já suportadas (inclusive as das sprints anteriores) e o bot lida bem com frases fora de contexto. |
| **Validação do PO**              | O Product Owner conversou de forma natural com o bot no Telegram e confirmou que o retorno atende à regra de negócio.                                                           |
| **Pronto para Deploy**           | O código está limpo, mergeado na `main` oficial por Pull Request e pronto para ser executado.                                                                                   |

---

<div align="center">

### MIA - Assistente de Análise de Dados

**McLorem Tecnologia · Fatec São José dos Campos · 2026**

</div>