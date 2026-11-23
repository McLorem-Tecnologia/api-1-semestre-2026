# Documentação — Sprint 3

<div align="center">
  <img src="../../../img/logo-mclorem-dark.png#gh-dark-mode-only" alt="logo da McLorem Tecnologia" width="200">
  <img src="../../../img/logo-mclorem-light.png#gh-light-mode-only" alt="logo da McLorem Tecnologia" width="200">
  <h3>MIA - Assistente de Análise de Dados</h3>
</div>

<br>

<p align="center">
  <a href="#desafio">Desafio</a> &nbsp;&bull;&nbsp;
  <a href="#us">User Stories</a> &nbsp;&bull;&nbsp;
  <a href="#dor">DoR</a> &nbsp;&bull;&nbsp;
  <a href="#dod">DoD</a> &nbsp;&bull;&nbsp;
  <a href="#equipe">Equipe</a>
</p>

---

> [!IMPORTANT]
> **Status da Sprint:**  Concluído ✅<br>
> **Relatório de Testes da Sprint:** [Link](./testes/Relatório%20de%20Testes%20-%20Sprint%203.md)<br>
> **Vídeo da Sprint:** [Youtube](https://youtu.be/QUKi3barLLY)

## 🏅 Desafio <a id="desafio"></a>

Transformar os dados de estoque, receitas e previsão de produção em recomendações seguras para a operação. A MIA calcula a necessidade de matéria-prima por setor, identifica apenas o excedente que sobra depois de reservar essa necessidade e compara ingredientes disponíveis com déficits de outros setores. Quando a sobra não cobre todo o déficit, informa o limite da transferência e quanto ainda faltaria. A recomendação é consultiva: não altera os estoques nem registra uma movimentação.

A sprint também tornou esse conhecimento mais acessível pelo TeleBot: `/ajuda` e `/help` abrem um menu com exemplos de perguntas para produção, matéria-prima, descarte, produtos e vendas. As perguntas escolhidas usam o mesmo fluxo da conversa. Nas previsões de produção, “o que produzir” e “quanto produzir” levam a respostas com quantidades; os mesmos assuntos podem ser perguntados por voz.

## 📋 User Stories <a id="us"></a>

| Indicador | Planejamento e resultado |
| :--- | :--- |
| **Capacidade estimada da equipe por Sprint** | 85 Story Points |
| **Meta da Sprint** | US-11 e US-12 — 21 Story Points; 21 entregues (100%) |
| **Escopo transversal** | Menu de ajuda e navegação no TeleBot; sem estimativa própria de pontos |

| Rank | Prioridade | User Story | Story Points | Sprint | Status |
| :---: | :--------: | ---------- | :----------: | :----: | :----: |
| 11 | Baixa | Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos e evitar compras desnecessárias. | 13 | 3 | ✅ Concluída |
| 12 | Baixa | Eu, como gerente, quero identificar transferências de matéria-prima recomendadas entre setores, a fim de cobrir déficits sem comprometer a necessidade do setor de origem. | 8 | 3 | ✅ Concluída |

**Validação da Sprint:** [BDD](./testes/BDD%20-%20Sprint%203.md) · [Checklist DoR/DoD](./Checklist%20-%20Sprint%203.md) · [Relatório de testes US-11/US-12](./testes/Relatório%20de%20Testes%20-%20Sprint%203.md) · [Regressão completa](../../teste/Relatorio%20de%20Teste.md)

---

## 🏅 DoR — Definition of Ready <a id="dor"></a>

| Critério | Definição atendida nesta Sprint |
| :--- | :--- |
| **Objetivo e usuário** | US-11 atende ao líder que precisa localizar sobras; US-12 atende ao gerente que precisa avaliar transferências para cobrir déficits. |
| **Regra de negócio** | Sobra é estoque atual menos necessidade prevista. A quantidade sugerida não ultrapassa a sobra após reservar a necessidade do setor de origem. |
| **Dados e unidades** | A previsão usa vendas históricas, produtos, receitas e estoques cadastrados. A unidade da receita é a unidade de referência da necessidade e da recomendação. |
| **Filtros e cenários** | O setor de origem é opcional. O BDD cobre transferência total e parcial, ausência de sobra, falta de histórico e produto sem receita. |
| **Limites da ação** | A tool apenas recomenda: não altera o CSV, não baixa estoque e não confirma uma movimentação real. |
| **Critérios de aceitação** | Os critérios estão registrados no BDD e no Checklist da Sprint 3, com evidências ligadas ao Relatório de Testes. |
| **Dependências** | A previsão de necessidade reutiliza o cálculo de matéria-prima da US-10 e a previsão de produção existente. |
| **Intenções e acesso** | Exemplos de perguntas estão mapeados por categoria; `/ajuda` e `/help` levam às perguntas de exemplo pelo fluxo da MIA. |

## 🏅 DoD — Definition of Done <a id="dod"></a>

| Critério | Resultado da Sprint |
| :--- | :--- |
| **US-11 — sobras disponíveis** | A tool lista ingredientes com saldo positivo por setor após reservar a necessidade prevista e aceita filtro de setor de origem. |
| **US-12 — recomendação** | A tool recomenda transferências para déficits compatíveis, limita a quantidade à sobra disponível e informa o déficit residual nas transferências parciais. |
| **Estoque preservado** | As consultas são somente leitura e não modificam os estoques. O teste verificou o hash do CSV antes e depois. |
| **Tratamento de dados ausentes** | Histórico inexistente e produtos sem receita recebem mensagens de ausência/ressalva, sem consumo inventado. |
| **Menu do TeleBot** | `/ajuda` e `/help`, categorias, perguntas de exemplo e retorno ao menu foram implementados e verificados com testes automatizados. |
| **Testes registrados** | Os 13 testes automatizados passaram. A resposta integrada local preservou os 69 itens da tool; os resultados e respostas completas estão no relatório. |
| **Documentação** | Arquitetura, BDD, checklist, manual do usuário e relatórios foram atualizados para a organização das tools e o menu. |
| **Limites da validação** | A execução foi local. Telegram ao vivo e áudio físico não foram testados; isso está registrado no relatório, sem ser apresentado como integração validada. |

---

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
