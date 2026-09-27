# Documentação - Sprint 1

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

Desenvolver a base do Assistente de Análise de Dados integrado ao Telegram, permitindo que gestores extraiam insights de negócios através de linguagem natural. O desafio central consistiu em processar dados diretamente de planilhas CSV locais (sem persistência de dados) utilizando lógica algorítmica em Python para estruturar o Planejamento de Produção. Foi necessário criar algoritmos capazes de cruzar o histórico de vendas com variáveis externas (como dias da semana e feriados) para prever com exatidão quais e quantos produtos devem ser produzidos, visando a redução de desperdícios de tempo e insumos. Toda a inteligência e processamento foram projetados para operar de forma autônoma, atendendo à restrição rigorosa de não utilizar APIs externas de terceiros.

## 📋 User Stories <a id="us"></a>

| $\textsf{\textbf{Capacidade estimada da Equipe por Sprint:}}$ | $\textsf{55 Story Points}$ |
|---|---|
| $\color{#2e8b57}{\textsf{\textbf{Meta da Sprint:}}}$ | $\textsf{User Story de rank 1 e rank 2 (\textit{21 Story Points})}$ |
| $\textsf{\textbf{Previsão da Sprint} (\textit{extras, sem compromisso de entrega}):}$ | $\textsf{User Story de rank 3 e rank 4 (\textit{34 Story Points})}$ |

| Rank | Prioridade | User Story | Story Points | Sprint | Status |
| :--: | :--------: | :--- | :----------: | :----: | :----: |
| $\color{#2e8b57}{\textsf{\textbf{1}}}$ | $\color{#2e8b57}{\textsf{\textbf{Alta}}}$ | $\color{#2e8b57}{\textsf{\textbf{Eu, como líder, quero saber quais produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.}}}$ | $\color{#2e8b57}{\textsf{\textbf{13}}}$ | $\color{#2e8b57}{\textsf{\textbf{1}}}$ | ✅ |
| $\color{#2e8b57}{\textsf{\textbf{2}}}$ | $\color{#2e8b57}{\textsf{\textbf{Alta}}}$ | $\color{#2e8b57}{\textsf{\textbf{Eu, como líder, quero saber quantos produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.}}}$ | $\color{#2e8b57}{\textsf{\textbf{8}}}$ | $\color{#2e8b57}{\textsf{\textbf{1}}}$ | ✅ |
| $\textsf{3}$ | $\textsf{Média}$ | $\textsf{Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y.}$ | $\textsf{13}$ | $\textsf{1}$ | ✅ |
| $\textsf{4}$ | $\textsf{Média}$ | $\textsf{Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de consultar a meta ideal de produção estipulada para a data.}$ | $\textsf{21}$ | $\textsf{1}$ | ✅ |

---

## 🏅 DoR - Definition of Ready <a id="dor"></a>

A avaliação detalhada de DoR e DoD, User Story por User Story, está em [`Checklist - Sprint 1`](./Checklist%20-%20Sprint%201.md).

| Critério | Descrição |
| :--- | :--- |
| **Clareza na Descrição** | A User Story está escrita no formato: "Eu, como [papel], quero [ação], a fim de [objetivo/valor]". |
| **Critérios de Aceitação** | A história possui critérios claros e pelo menos um cenário de teste básico (BDD) mapeado (Dado que... Quando... Então...). |
| **Independente** | A história pode ser desenvolvida sem depender de tarefas bloqueantes dentro da mesma Sprint. |
| **Compreensão Compartilhada** | A equipe entende o propósito e estimou o esforço da tarefa (Story Points definidos). |
| **Mapeamento de Intenções** | Estão documentados exemplos reais de frases em linguagem natural que o usuário pode enviar (ex: "o que eu devo fazer hoje?", "tem produto pra agora?"). |
| **Critérios Técnicos** | Está definido o que o modelo via **DSPy** precisará extrair da frase (parâmetros) e qual arquivo/coluna estática o **Pandas** deverá ler. |

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério | Descrição |
| :--- | :--- |
| **Critérios Atendidos** | Todos os critérios de aceitação e cenários de teste da User Story foram cumpridos e validados com sucesso. |
| **Interpretação Validada (NLP)** | A IA interpretou corretamente diferentes variações da mesma pergunta em texto livre, acionando a filtragem correta no Pandas. |
| **Código Revisado** | O código passou por Code Review (Pull Request revisado e aprovado por pelo menos um outro membro da equipe). |
| **Documentação Atualizada** | As novas capacidades de interpretação do bot, a estrutura dos módulos DSPy e os mapeamentos dos CSVs estáticos foram atualizados no README.md. |
| **Integração Validada** | A nova capacidade de resposta não confunde a IA em relação a outras perguntas já suportadas e o bot lida bem com frases fora de contexto. |
| **Validação do PO** | O Product Owner conversou de forma natural com o bot no Telegram e confirmou que o retorno atende à regra de negócio. |
| **Pronto para Deploy** | O código está limpo, mergeado na branch principal e pronto para ser executado. |

## 🏅 Sprint Burndown <a id="burndown"></a>

<div align="center">
  <img src="../../../img/burndown-s1.png" alt="Gráfico de Burndown da Sprint 1" width="60%">
</div>

<br>

> [!IMPORTANT]
> **Retrospectiva:** O nosso Burndown Chart reflete um salto nos primeiros dias e um padrão de entregas concentradas no fim (efeito penhasco). O pico inicial ocorreu devido a um erro operacional: a Sprint foi iniciada no Jira antes que os *Story Points* fossem declarados nas *User Stories*. Já a queda brusca no final aconteceu porque os pontos foram atribuídos de forma concentrada na história principal (a "casca"). Como o sistema só "queima" os pontos quando a história inteira é movida para concluída, o esforço contínuo da equipe não foi refletido gradativamente, registrando a entrega total de uma só vez no fechamento da Sprint.
> 
> **Ações para a Sprint 2:** 
> 1. Garantir que o *planning* seja finalizado e todas as estimativas sejam declaradas nos cards **antes** de dar o *start* oficial na Sprint.
> 2. Fracionar as *User Stories* em subtarefas menores e realizar pontuações mais granulares. Isso garantirá que a conclusão de pequenas etapas movimente o fluxo com constância, refletindo o andamento diário da equipe com precisão.

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
          <img src="https://github.com/mvlsouza.png" width="100px;" alt="Foto de Marcus Vinicius"/>
        </a><br>
        <sub><b>Marcus Vinicius</b></sub><br>
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