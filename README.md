 # API 1º Semestre ADS

<div align="center">
  <!-- Imagem que aparece apenas no Modo Escuro -->
  <img src="docs/img/logo-mclorem-dark.png#gh-dark-mode-only" alt="logo da McLorem Tecnologia" width="200">
  
  <!-- Imagem que aparece apenas no Modo Claro -->
  <img src="docs/img/logo-mclorem-light.png#gh-light-mode-only" alt="logo da McLorem Tecnologia" width="200">
  
  <h2>McLorem Tecnologia</h2>
</div>


 <p align="center">
  | <a href ="#desafio"> Desafio</a>  |
  <a href ="#solucao"> Solução</a>  |   
  <a href ="#backlog"> Backlog do Produto</a>  |
  <a href ="#dor">DoR</a>  |
  <a href ="#dod">DoD</a>  |
  <a href ="#sprint"> Cronograma de Sprints</a>  |
  <a href ="#tecnologias">Tecnologias</a> |
  <a href ="#manual">Manual de Instalação</a>  | 
  <a href ="#equipe"> Equipe</a> |
</p>

<br>

> Status do Projeto: Em Desenvolvimento 
<!--
>
> Relatório de Testes: [PDF](docs/cliente/relatorio_avaliacoes.pdf)
>
> Pasta de Documentação: [Link](docs/cliente)
> 
> Video do Projeto:  [Youtube](https://youtu.be/)
-->

## 🎯 Desafio <a id="desafio"></a>

Apesar do avanço tecnológico, a gestão diária de setores operacionais em **supermercados** (como padaria, açougue e reposição de gôndolas) ainda se baseia fortemente em planilhas estáticas. Essa realidade cria um distanciamento da era da Inteligência Artificial, pois os dados não estão organizados em pipelines modernos.

Nos corredores, estoques e áreas de preparo, gerentes e líderes enfrentam problemas diretos:

* **Falta de Agilidade:** Precisar sair do salão de vendas, ir até o escritório e aplicar filtros no Excel para saber o que precisa ser produzido ou reposto no dia.
* **Mãos Ocupadas:** O ambiente de varejo exige mobilidade constante (conferência de validade, manuseio de caixas e atendimento), tornando o uso de teclado e mouse pouco prático durante a supervisão.
* **Sistemas Engessados:** Softwares tradicionais ou bots antigos exigem que o usuário decore comandos rígidos (ex: `/producao_padaria`), o que diminui a adoção da ferramenta pela equipe.

<br>

## 💡 Solução <a id="solucao"></a>

Desenvolvemos um **Assistente de Análise de Dados** integrado ao Telegram, projetado para extrair insights diretamente das planilhas do mercado (arquivos CSV) utilizando Python, sem a necessidade de migração para bancos de dados complexos.

O diferencial da solução é a fricção zero com o usuário. A plataforma atua de forma semelhante a uma "Alexa corporativa" para o varejo:

* **Integração com Pandas:** O motor de análise em Python lê, cruza e filtra os dados de estoque, produção e validade dos CSVs instantaneamente.
* **Linguagem Natural (DSPy):** O gestor não precisa usar comandos. Ele interage de forma conversacional (ex: *"O que precisamos assar na padaria hoje?"* ou *"Quero saber quantos produtos precisam ser produzidos hoje?"*), e a IA interpreta a intenção e os parâmetros da busca.
* **Acessibilidade por Voz:** Suporte nativo para recebimento de perguntas via mensagens de áudio no Telegram, permitindo consultas *hands-free* diretamente do estoque ou do salão de vendas.
* **Insights Diretos:** O bot devolve a resposta processada, mastigada e formatada no chat, economizando tempo e apoiando a tomada de decisão rápida sobre reposição, redução de desperdícios (perdas de hortifruti/açougue) e lucros.

---

## 📋 Backlog do Produto <a id="backlog"></a>

| Rank | Prioridade | User Story | Story Points | Sprint | Requisito do Cliente | Status |
| :--: | :--------: | :--- | :----------: | :----: | :------------------: | :----: |
|   **1**  |    **Alta**    | Eu, como líder, quero saber quais produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto. |      -*-*-       |    1   |          ---         |    ❌   |
|   **2**  |    **Alta**    | Eu, como líder, quero saber quantos produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto. |      -*-*-       |    1   |        ---       |    ❌   |
|   **3**  |    **Média**   | Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y. |      -*-*-       |    1   |          ---         |    ❌   |
|   **4**  |    **Média**   | Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de comparar a meta com a produção real e identificar gargalos. |      -*-*-       |    1   |          ---         |    ❌   |
|   **5**  |    **Média**   | Eu, como líder, quero saber quais produtos me trazem mais lucro, a fim de otimizar o tempo dos colaboradores. |      -*-*-       |    2   |          ---         |    ❌   |
|   **6**  |    **Média**   | Eu, como líder, quero saber quantos reais foram descartados, a fim de monitorar o impacto financeiro das perdas do meu setor. |      -*-*-       |    2   |          ---         |    ❌   |
|   **7**  |    **Média**   | Eu, como gerente, quero saber quantos reais foram descartados, a fim de avaliar o custo global de desperdício da empresa. |      -*-*-       |    2  |          ---         |    ❌   |
|   **8**  |    ****Baixa****   | Eu, como gerente, quero saber quais produtos me trazem mais lucro, a fim de orientar estrategicamente os setores. |      -*-*-       |    2   |          ---         |    ❌   |
|  **9**  |    ****Baixa****   | Eu, como gestor, quero interagir com o assistente de análise de dados enviando perguntas por áudio, a fim de obter insights das planilhas de forma fluida e sem contato manual (semelhante a uma Alexa). |      -*-*-       |    3   |          ---         |    ❌   |
|   **10**  |    ****Baixa****   | Eu, como líder, quero saber quanta matéria-prima eu preciso deixar preparada para o dia seguinte, a fim de otimizar o tempo e reduzir o desperdício de matéria-prima. |      -*-*-       |    3   |          ---         |    ❌   |
|  **11**  |    ****Baixa****   | Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias. |      -*-*-       |    3   |          ---         |    ❌   |
|  **12**  |    ****Baixa****   | Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção. |      -*-*-       |    3   |          ---         |    ❌   |

---

<br>

## 🏅 DoR - Definition of Ready <a id="DoR"></a>

| Critério | Descrição |
| :--- | :--- |
| **Clareza na Descrição** | A User Story está escrita no formato: "Eu, como [papel], quero [ação], a fim de [objetivo/valor]". |
| **Critérios de Aceitação** | A história possui critérios claros e pelo menos um cenário de teste básico (BDD) mapeado (Dado que... Quando... Então...). |
| **Independente** | A história pode ser desenvolvida sem depender de tarefas bloqueantes dentro da mesma Sprint. |
| **Compreensão Compartilhada** | A equipe entende o propósito e estimou o esforço da tarefa (Story Points definidos). |
| **Mapeamento de Intenções** | Estão documentados exemplos reais de frases em linguagem natural que o usuário pode enviar (ex: "o que eu devo fazer hoje?", "tem produto pra agora?"). |
| **Critérios Técnicos** | Está definido o que o modelo via **DSPy** precisará extrair da frase (parâmetros) e qual arquivo/coluna estática o **Pandas** deverá ler. |
---
<br>

## 🏅 DoD - Definition of Done <a id="DoD"></a>

| Critério | Descrição |
| :--- | :--- |
| **Critérios Atendidos** | Todos os critérios de aceitação e cenários de teste da User Story foram cumpridos e validados com sucesso. |
| **Interpretação Validada (NLP)** | A IA interpretou corretamente diferentes variações da mesma pergunta em texto livre, acionando a filtragem correta no Pandas. |
| **Código Revisado** | O código passou por Code Review (Pull Request revisado e aprovado por pelo menos um outro membro da equipe). |
| **Documentação Atualizada** | As novas capacidades de interpretação do bot, a estrutura dos módulos DSPy e os mapeamentos dos CSVs estáticos foram atualizados no README.md. |
| **Integração Validada** | A nova capacidade de resposta não confunde a IA em relação a outras perguntas já suportadas e o bot lida bem com frases fora de contexto. |
| **Validação do PO** | O Product Owner conversou de forma natural com o bot no Telegram e confirmou que o retorno atende à regra de negócio. |
| **Pronto para Deploy** | O código está limpo, mergeado na branch principal e pronto para ser executado. |
---
<br>

<!--


## 📅 Cronograma de Sprints <a id="sprint"></a>

<br>
## 💻 Tecnologias <a id="tecnologias"></a>

<br>

## 📖 Manual de Instalação <a id="manual"></a>

<br>

### 🛠 Pré-requisitos

-->
