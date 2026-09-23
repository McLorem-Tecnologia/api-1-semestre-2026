
# API 1º Semestre ADS

# Documentação - Sprint 1

<div align="center">
  <!-- Imagem que aparece apenas no Modo Escuro -->
  <img src="../../../img/logo-mclorem-dark.png#gh-dark-mode-only" alt="logo da McLorem Tecnologia" width="200">
  
  <!-- Imagem que aparece apenas no Modo Claro -->
  <img src="../../../img/logo-mclorem-light.png#gh-light-mode-only" alt="logo da McLorem Tecnologia" width="200">
  
  <h2>McLorem Tecnologia</h2>
</div>

<p align="center">
  | <a href ="#desafio"> Desafio</a>  |
  <a href ="#us"> User Stories</a>  |   
  <a href ="#dor">DoR</a>  |
  <a href ="#dod">DoD</a>  |
  <a href ="#equipe"> Equipe</a> |
</p>

> Status da Sprint: Em Desenvolvimento

## 🏅 Desafio <a id="desafio"></a>

Desenvolver a base do Assistente de Análise de Dados integrado ao Telegram, permitindo que gestores extraiam insights de negócios através de linguagem natural. O desafio central consistiu em processar dados diretamente de planilhas CSV locais (sem persistência de dados) utilizando lógica algorítmica em Python para estruturar o Planejamento de Produção. Foi necessário criar algoritmos capazes de cruzar o histórico de vendas com variáveis externas (como temperatura e dias da semana) para prever com exatidão quais e quantos produtos devem ser produzidos, visando a redução de desperdícios de tempo e insumos. Toda a inteligência e processamento foram projetados para operar de forma autônoma, atendendo à restrição rigorosa de não utilizar APIs externas de terceiros.

## 📋 User Stories <a id="us"></a>

<table>
  <tbody>
    <tr>
      <td><b>Capacidade estimada da Equipe por Sprint:</b></td>
      <td>55 Story Points</td>
    </tr>
    <tr>
      <td><b><span style="color: #2e8b57;">Meta da Sprint:</span></b></td>
      <td>User Stories de rank 1 e rank 2 (total de <i>21 Story Points</i>)</td>
    </tr>
    <tr>
      <td><b>Previsão da Sprint</b> (<i>extras, sem compromisso de entrega</i>):</td>
      <td>User Story de rank 3 e rank 4 (<i>34 Story Points</i>)</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th style="text-align: center;">Rank</th>
      <th style="text-align: center;">Prioridade</th>
      <th style="text-align: left;">User Story</th>
      <th style="text-align: center;">Story Points</th>
      <th style="text-align: center;">Sprint</th>
      <th style="text-align: center;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">1</span></b></td>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">Alta</span></b></td>
      <td style="text-align: left;"><b><span style="color: #2e8b57;">Eu, como líder, quero saber quais produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.</span></b></td>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">13</span></b></td>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">1</span></b></td>
      <td style="text-align: center;">❌</td>
    </tr>
    <tr>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">2</span></b></td>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">Alta</span></b></td>
      <td style="text-align: left;"><b><span style="color: #2e8b57;">Eu, como líder, quero saber quantos produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.</span></b></td>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">8</span></b></td>
      <td style="text-align: center;"><b><span style="color: #2e8b57;">1</span></b></td>
      <td style="text-align: center;">❌</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td style="text-align: center;">Média</td>
      <td style="text-align: left;">Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y.</td>
      <td style="text-align: center;">13</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">❌</td>
    </tr>
    <tr>
      <td style="text-align: center;">4</td>
      <td style="text-align: center;">Média</td>
      <td style="text-align: left;">Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de comparar a meta com a produção real e identificar gargalos.</td>
      <td style="text-align: center;">21</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">❌</td>
    </tr>
  </tbody>
</table>

---

## 🏅 DoR - Definition of Ready <a id="dor"></a>

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

## 🎓 Equipe <a id="equipe"></a>

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/hcastrosilva96">
          <img src="https://github.com/hcastrosilva96.png" width="115px;" style="border-radius: 50%;" alt="Foto do Henrique de Castro"/><br>
          <sub><b>Henrique de Castro</b></sub>
        </a><br>
        Product Owner<br>
        <a href="https://www.linkedin.com/in/henrique-castro-silva-6568a012b/">LinkedIn</a>
      </td>
      <td align="center">
        <a href="https://github.com/FelipeMoraisOC">
          <img src="https://github.com/FelipeMoraisOC.png" width="115px;" style="border-radius: 50%;" alt="Foto do Felipe Morais"/><br>
          <sub><b>Felipe Morais</b></sub>
        </a><br>
        Scrum Master<br>
        <a href="https://www.linkedin.com/in/felipemoraisoc/">LinkedIn</a>
      </td>
    </tr>
  </table>
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/mirelacristina">
          <img src="https://github.com/mirelacristina.png" width="100px;" style="border-radius: 50%;" alt="Foto da Mirela Cristina"/><br>
          <sub><b>Mirela Cristina</b></sub>
        </a><br>
        Dev Team<br>
        <!-- <a href="https://www.linkedin.com/in/">LinkedIn</a> -->
      </td>
      <td align="center">
        <a href="https://github.com/eduardogranja">
          <img src="https://github.com/eduardogranja.png" width="100px;" style="border-radius: 50%;" alt="Foto do Eduardo Granja"/><br>
          <sub><b>Eduardo Granja</b></sub>
        </a><br>
        Dev Team<br>
        <!-- <a href="https://www.linkedin.com/in/">LinkedIn</a> -->
      </td>
      <td align="center">
        <a href="https://github.com/IanVRV">
          <img src="https://github.com/IanVRV.png" width="100px;" style="border-radius: 50%;" alt="Foto do Ian Victor"/><br>
          <sub><b>Ian Victor</b></sub>
        </a><br>
        Dev Team<br>
        <a href="https://www.linkedin.com/in/ian-victor-ribeiro-vieira-3147121ba/">LinkedIn</a>
      </td>
      <td align="center">
        <a href="https://github.com/mvlsouza">
          <img src="https://github.com/mvlsouza.png" width="100px;" style="border-radius: 50%;" alt="Foto do Marcus Vinicius"/><br>
          <sub><b>Marcus Vinicius</b></sub>
        </a><br>
        Dev Team<br>
        <a href="https://www.linkedin.com/in/mvlsouza">LinkedIn</a>
      </td>
    </tr>
  </table>
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/leandrotc013-lab">
          <img src="https://github.com/leandrotc013-lab.png" width="100px;" style="border-radius: 50%;" alt="Foto do Leandro"/><br>
          <sub><b>Leandro Silva</b></sub>
        </a><br>
        Dev Team<br>
        <!-- <a href="https://www.linkedin.com/in/">LinkedIn</a> -->
      </td>
      <td align="center">
        <a href="https://github.com/ag0ulart-dev">
          <img src="https://github.com/ag0ulart-dev.png" width="100px;" style="border-radius: 50%;" alt="Foto do Adham Goulart"/><br>
          <sub><b>Adham Goulart</b></sub>
        </a><br>
        Dev Team<br>
        <a href="https://www.linkedin.com/in/adham-goulart-4a7320394/">LinkedIn</a>
      </td>
      <td align="center">
        <a href="https://github.com/MATHEUSORTEGA">
          <img src="https://github.com/MATHEUSORTEGA.png" width="100px;" style="border-radius: 50%;" alt="Foto do Matheus Correia"/><br>
          <sub><b>Matheus Correia</b></sub>
        </a><br>
        Dev Team<br>
        <!-- <a href="https://www.linkedin.com/in/">LinkedIn</a> -->
      </td>
    </tr>
  </table>
</div>

---

*Desenvolvido com dedicação por estudantes da Fatec para o projeto de API do 1º Semestre de ADS - 2026-2.*