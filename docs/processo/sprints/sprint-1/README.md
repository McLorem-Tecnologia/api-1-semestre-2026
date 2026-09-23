
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
| **Clareza e Usuário** | O objetivo das User Stories está claramente definido e o usuário da funcionalidade (Líder) está identificado. |
| **Fontes de Dados** | Os produtos estão bem definidos no arquivo `produtos_mercado.csv`. Serão utilizados os arquivos: Regras, Vendas e Descartes do supermercado por mês e ano. |
| **Regras de Negócio** | O método de cálculo está definido, baseando-se nas vendas anteriores, na temperatura do dia e no dia do mês. |
| **Apresentação Visual** | Está definido como a quantidade recomendada e a lista de produtos serão apresentadas ao líder. |
| **Critérios e Dependências** | Todos os critérios de aceite estão definidos e as dependências necessárias para o desenvolvimento foram identificadas. |

## 🏅 DoD - Definition of Done <a id="dod"></a>

| Critério | Descrição |
| :--- | :--- |
| **Identificação e Cálculo** | O sistema identifica corretamente quais produtos precisam ser produzidos e calcula a quantidade recomendada para cada um deles. |
| **Fatores de Demanda** | O cálculo utiliza ativamente os dados do histórico de vendas e considera os fatores de demanda definidos (temperatura, feriados e finais de semana). |
| **Apresentação de Dados** | O sistema apresenta de forma clara, ao líder, o nome do produto e a quantidade recomendada para produção. |
| **Precisão e Regras** | Os cálculos foram validados com dados de referência e produtos sem necessidade de produção não são indevidamente recomendados. |
| **Qualidade (Testes)** | A funcionalidade foi testada com diferentes cenários de demanda e não apresenta erros que impeçam o seu funcionamento. |
| **Aprovação Final** | Todos os critérios de aceite foram atendidos e o líder ou responsável pelo projeto validou o resultado final da Sprint. |

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