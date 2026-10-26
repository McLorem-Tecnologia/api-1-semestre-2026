# Documentação - Sprint 2

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
  <a href ="#dor">DoR</a> &nbsp;&bull;&nbsp;
  <a href ="#dod">DoD</a> &nbsp;&bull;&nbsp;
  <a href ="#burndown"> Burndown</a> &nbsp;&bull;&nbsp;
  <a href ="#equipe"> Equipe</a>
</p>

---

> [!IMPORTANT]
> **Status do Projeto:**  Concluído ✅

## 🏅 Desafio <a id="desafio"></a>

Evoluir a MIA além do planejamento de produção, levando ao líder e ao gerente uma visão financeira e operacional dos setores, sempre por linguagem natural no Telegram. O desafio central é traduzir as perdas em valor financeiro (cruzando os descartes com o custo unitário dos produtos), recortar a previsão de produção por período do dia, estimar a matéria-prima necessária para o dia seguinte e apoiar as transferências entre setores. Soma-se a isso uma nova forma de interação: o envio de perguntas por áudio, com transcrição feita localmente. Toda a inteligência e o processamento continuam operando de forma autônoma, sem persistência de dados e sem APIs externas de terceiros.

## 📋 User Stories <a id="us"></a>

| $\textsf{\textbf{Capacidade estimada da Equipe por Sprint:}}$                         | $\textsf{85 Story Points (\textbf{64 SP entregues} \color{#808080}{/ 21 SP não entregues})}$ |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| $\color{#2e8b57}{\textsf{\textbf{Meta da Sprint:}}}$                                  | $\textsf{User Stories de rank 5, 6, 7 e 8 (\textit{39 Story Points — 100\% entregue})}$      |
| $\textsf{\textbf{Previsão da Sprint} (\textit{extras, sem compromisso de entrega}):}$ | $\textsf{User Stories de rank 9 e 10 entregues (\textit{25 SP}) \color{#808080}{/ rank 11 e 12 não entregues (\textit{21 SP})}}$ |

|                  Rank                  |                 Prioridade                 | User Story                                                                                                                                                                                                          |              Story Points               |                 Sprint                 |                 Status                 |
| :------------------------------------: | :----------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------: | :------------------------------------: | :------------------------------------: |
| $\color{#2e8b57}{\textsf{\textbf{5}}}$ | $\color{#2e8b57}{\textsf{\textbf{Média}}}$ | $\color{#2e8b57}{\textsf{\textbf{Eu, como líder, quero saber quais produtos devo produzir em cada período do dia, a fim de otimizar o tempo dos colaboradores.}}}$                                                  | $\color{#2e8b57}{\textsf{\textbf{13}}}$ | $\color{#2e8b57}{\textsf{\textbf{2}}}$ | $\color{#2e8b57}{\textsf{\textbf{✅}}}$ |
| $\color{#2e8b57}{\textsf{\textbf{6}}}$ | $\color{#2e8b57}{\textsf{\textbf{Média}}}$ | $\color{#2e8b57}{\textsf{\textbf{Eu, como gerente, quero saber quantos reais foram descartados em cada setor, a fim de monitorar o impacto financeiro das perdas dos setores.}}}$                                   | $\color{#2e8b57}{\textsf{\textbf{8}}}$  | $\color{#2e8b57}{\textsf{\textbf{2}}}$ | $\color{#2e8b57}{\textsf{\textbf{✅}}}$ |
| $\color{#2e8b57}{\textsf{\textbf{7}}}$ | $\color{#2e8b57}{\textsf{\textbf{Média}}}$ | $\color{#2e8b57}{\textsf{\textbf{Eu, como gerente, quero saber quantos reais foram descartados, a fim de avaliar o custo global de desperdício da empresa.}}}$                                                      | $\color{#2e8b57}{\textsf{\textbf{5}}}$  | $\color{#2e8b57}{\textsf{\textbf{2}}}$ | $\color{#2e8b57}{\textsf{\textbf{✅}}}$ |
| $\color{#2e8b57}{\textsf{\textbf{8}}}$ | $\color{#2e8b57}{\textsf{\textbf{Baixa}}}$ | $\color{#2e8b57}{\textsf{\textbf{Eu, como gerente, quero saber quais produtos me trazem mais lucro, a fim de orientar estrategicamente os setores.}}}$                                                              | $\color{#2e8b57}{\textsf{\textbf{13}}}$ | $\color{#2e8b57}{\textsf{\textbf{2}}}$ | $\color{#2e8b57}{\textsf{\textbf{✅}}}$ |
|              $\textsf{9}$              |              $\textsf{Baixa}$              | $\textsf{Eu, como gestor, quero interagir com o assistente de análise de dados enviando perguntas por áudio, a fim de obter insights das planilhas de forma fluida e sem contato manual (semelhante a uma Alexa).}$ |              $\textsf{10}$              |              $\textsf{2}$              |                   ✅                    |
|             $\textsf{10}$              |              $\textsf{Baixa}$              | $\textsf{Eu, como líder, quero saber quanta matéria-prima eu preciso deixar preparada para o dia seguinte, a fim de otimizar o tempo e reduzir o desperdício de matéria-prima.}$                                    |              $\textsf{15}$              |              $\textsf{2}$              |                   ✅                    |
|     $\color{#808080}{\textsf{11}}$     |     $\color{#808080}{\textsf{Baixa}}$      | $\color{#808080}{\textsf{Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias.}}$           |     $\color{#808080}{\textsf{13}}$      |     $\color{#808080}{\textsf{2}}$      |     $\color{#808080}{\textsf{❌}}$      |
|     $\color{#808080}{\textsf{12}}$     |     $\color{#808080}{\textsf{Baixa}}$      | $\color{#808080}{\textsf{Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção.}}$                                    |      $\color{#808080}{\textsf{8}}$      |     $\color{#808080}{\textsf{2}}$      |     $\color{#808080}{\textsf{❌}}$      |

> [!NOTE]
> A Sprint 2 reúne as histórias da Sprint 2 e da Sprint 3. As User Stories de **rank 5 a 8** são a meta da Sprint; as de **rank 9 a 12** são o que vamos tentar entregar, sem compromisso de entrega. Em relação ao backlog anterior, a **US05** passou a tratar do que produzir em cada período do dia (antes era lucro) e a **US06** passou a ser do gerente e a mostrar o valor descartado de cada setor. As **US07** e **US08** não foram alteradas.

---

## 🏅 DoR - Definition of Ready <a id="dor"></a>

A avaliação detalhada de DoR e DoD, User Story por User Story, está em [`Checklist - Sprint 2`](./Checklist%20-%20Sprint%202.md). Os cenários de aceitação estão no [`BDD - Sprint 2`](./testes/BDD%20-%20Sprint%202.md).

| Critério                      | Descrição                                                                                                                                                                                                   |
| :---------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Clareza na Descrição**      | A User Story está escrita no formato: "Eu, como [papel], quero [ação], a fim de [objetivo/valor]".                                                                                                          |
| **Critérios de Aceitação**    | A história possui critérios claros e pelo menos um cenário de teste básico (BDD) mapeado (Dado que... Quando... Então...).                                                                                  |
| **Independente**              | A história pode ser desenvolvida sem depender de tarefas bloqueantes dentro da mesma Sprint. Quando houver dependência (ex.: a US11 depende da US10), ela está identificada.                                |
| **Compreensão Compartilhada** | A equipe entende o propósito e estimou o esforço da tarefa (Story Points definidos).                                                                                                                        |
| **Mapeamento de Intenções**   | Estão documentados exemplos reais de frases em linguagem natural que o usuário pode enviar (ex: "o que produzo de manhã?", "quantos reais perdemos ontem?").                                                |
| **Dados Disponíveis**         | Está definido qual arquivo e coluna dos CSVs estáticos serão lidos, e os dados que ainda não existem na base (ex.: horário das vendas, custo unitário, matéria-prima, transferências) têm origem combinada. |
| **Critérios Técnicos**        | Está definido o que o modelo via **DSPy** precisará extrair da frase (parâmetros) e qual regra o **Pandas** deverá aplicar.                                                                                 |

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério                         | Descrição                                                                                                                                                                       |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Critérios Atendidos**          | Todos os critérios de aceitação e cenários de teste da User Story foram cumpridos e validados com sucesso.                                                                      |
| **Interpretação Validada (NLP)** | A IA interpretou corretamente diferentes variações da mesma pergunta, em texto ou em áudio, acionando a regra correta.                                                          |
| **Código Revisado**              | O código passou por Code Review (Pull Request revisado e aprovado por pelo menos um outro membro da equipe).                                                                    |
| **Testes Registrados**           | Os casos do Guia de Testes foram executados e registrados no Relatório de Testes, sem falhas pendentes.                                                                         |
| **Documentação Atualizada**      | As novas capacidades do bot e os mapeamentos dos CSVs estáticos foram atualizados na documentação.                                                                              |
| **Integração Validada**          | A nova capacidade de resposta não confunde a IA em relação a outras perguntas já suportadas (inclusive as das sprints anteriores) e o bot lida bem com frases fora de contexto. |
| **Validação do PO**              | O Product Owner conversou de forma natural com o bot no Telegram e confirmou que o retorno atende à regra de negócio.                                                           |
| **Pronto para Deploy**           | O código está limpo, mergeado na branch principal e pronto para ser executado.                                                                                                  |

## 🏅 Sprint Burndown <a id="burndown"></a>

<div align="center">
  <img src="../../../img/burndown-s2.png" alt="Gráfico de Burndown da Sprint 2" width="60%">
</div>

<br>

## 🎓 Equipe <a id="equipe"></a>

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/hcastrosilva96">
          <img src="https://github.com/hcastrosilva96.png" width="115px;" alt="Foto de Henrique de Castro"/>
        </a><br>
        <sub><b>Henrique de Castro</b></sub><br>
        <sub>Product Owner</sub><br>
        <a href="https://github.com/hcastrosilva96"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/henrique-castro-silva-6568a012b/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
      <td align="center">
        <a href="https://github.com/FelipeMoraisOC">
          <img src="https://github.com/FelipeMoraisOC.png" width="115px;" alt="Foto de Felipe Morais"/>
        </a><br>
        <sub><b>Felipe Morais</b></sub><br>
        <sub>Scrum Master</sub><br>
        <a href="https://github.com/FelipeMoraisOC"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/felipemoraisoc/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
    </tr>
  </table>
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/mirelacristina">
          <img src="https://github.com/mirelacristina.png" width="100px;" alt="Foto de Mirela Cristina"/>
        </a><br>
        <sub><b>Mirela Cristina</b></sub><br>
        <sub>Dev Team</sub><br>
        <a href="https://github.com/mirelacristina"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/mirela-cristina-4325723a6/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
      <td align="center">
        <a href="https://github.com/eduardogranja">
          <img src="https://github.com/eduardogranja.png" width="100px;" alt="Foto de Eduardo Granja"/>
        </a><br>
        <sub><b>Eduardo Granja</b></sub><br>
        <sub>Dev Team</sub><br>
        <a href="https://github.com/eduardogranja"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/eduardo-granja-95273739a/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
      <td align="center">
        <a href="https://github.com/IanVRV">
          <img src="https://github.com/IanVRV.png" width="100px;" alt="Foto de Ian Victor"/>
        </a><br>
        <sub><b>Ian Victor</b></sub><br>
        <sub>Dev Team</sub><br>
        <a href="https://github.com/IanVRV"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/ian-victor-ribeiro-vieira-3147121ba/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
      <td align="center">
        <a href="https://github.com/mvlsouza">
          <img src="https://github.com/mvlsouza.png" width="100px;" alt="Foto de Marcus Vinícius"/>
        </a><br>
        <sub><b>Marcus Vinícius</b></sub><br>
        <sub>Dev Team</sub><br>
        <a href="https://github.com/mvlsouza"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/mvlsouza/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
    </tr>
  </table>
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/leandrotc013-lab">
          <img src="https://github.com/leandrotc013-lab.png" width="100px;" alt="Foto de Leandro Silva"/>
        </a><br>
        <sub><b>Leandro Silva</b></sub><br>
        <sub>Dev Team</sub><br>
        <a href="https://github.com/leandrotc013-lab"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/leandro-silva-a54ab4a2/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
      <td align="center">
        <a href="https://github.com/ag0ulart-dev">
          <img src="https://github.com/ag0ulart-dev.png" width="100px;" alt="Foto de Adham Goulart"/>
        </a><br>
        <sub><b>Adham Goulart</b></sub><br>
        <sub>Dev Team</sub><br>
        <a href="https://github.com/ag0ulart-dev"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/adham-goulart-4a7320394/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
      <td align="center">
        <a href="https://github.com/MATHEUSORTEGA">
          <img src="https://github.com/MATHEUSORTEGA.png" width="100px;" alt="Foto de Matheus Correia"/>
        </a><br>
        <sub><b>Matheus Correia</b></sub><br>
        <sub>Dev Team</sub><br>
        <a href="https://github.com/MATHEUSORTEGA"><img src="https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub"/></a> <a href="https://www.linkedin.com/in/"><img src="https://img.shields.io/badge/-LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
      </td>
    </tr>
  </table>
</div>

---

# 🎓 Contexto acadêmico

A **MIA**, desenvolvida pela **McLorem Tecnologia**, faz parte da **Aprendizagem por Projetos Integrados (API)** do 1º semestre do curso de **Análise e Desenvolvimento de Sistemas da Fatec São José dos Campos**.

<br>

<div align="center">

### MIA - Assistente de Análise de Dados

**McLorem Tecnologia · Fatec São José dos Campos · 2026**

</div>
