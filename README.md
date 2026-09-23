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
| Rank | Prioridade | User Story | Story Points | Sprint | Status |
| :--: | :--------: | :--- | :----------: | :----: | :----: |
|   **1**  |    **Alta**    | Eu, como líder, quero saber quais produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto. |      13       |    1   |    ❌   |
|   **2**  |    **Alta**    | Eu, como líder, quero saber quantos produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto. |      8       |    1   |    ❌   |
|   **3**  |    **Média**   | Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y. |      13       |    1   |    ❌   |
|   **4**  |    **Média**   | Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de comparar a meta com a produção real e identificar gargalos. |      21       |    1   |    ❌   |
|   **5**  |    **Média**   | Eu, como líder, quero saber quais produtos me trazem mais lucro, a fim de otimizar o tempo dos colaboradores. |      -*-*-       |    2   |    ❌   |
|   **6**  |    **Média**   | Eu, como líder, quero saber quantos reais foram descartados, a fim de monitorar o impacto financeiro das perdas do meu setor. |      -*-*-       |    2   |    ❌   |
|   **7**  |    **Média**   | Eu, como gerente, quero saber quantos reais foram descartados, a fim de avaliar o custo global de desperdício da empresa. |      -*-*-       |    2  |    ❌   |
|   **8**  |    **Baixa**   | Eu, como gerente, quero saber quais produtos me trazem mais lucro, a fim de orientar estrategicamente os setores. |      -*-*-       |    2   |    ❌   |
|  **9**  |    **Baixa**   | Eu, como gestor, quero interagir com o assistente de análise de dados enviando perguntas por áudio, a fim de obter insights das planilhas de forma fluida e sem contato manual (semelhante a uma Alexa). |      -*-*-       |    3   |    ❌   |
|   **10**  |    **Baixa**   | Eu, como líder, quero saber quanta matéria-prima eu preciso deixar preparada para o dia seguinte, a fim de otimizar o tempo e reduzir o desperdício de matéria-prima. |      -*-*-       |    3   |    ❌   |
|  **11**  |    **Baixa**   | Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias. |      -*-*-       |    3   |    ❌   |
|  **12**  |    **Baixa**   | Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção. |      -*-*-       |    3   |    ❌   |

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
---

## 📅 Cronograma de Sprints <a id="sprint"></a>

| Sprint          |    Período    | Documentação                                     |
| --------------- | :-----------: | ------------------------------------------------ |
| 🔖 **SPRINT 1** | 07/09 - 27/09 | [Sprint 1 Docs](./docs/processo/sprints/sprint-1/README.md) |
| 🔖 **SPRINT 2** | 05/10 - 25/10 | ⏳ A iniciar |
| 🔖 **SPRINT 3** | 02/11 - 27/11 | ⏳ A iniciar |

## 💻 Tecnologias <a id="tecnologias"></a>

<h4 align="center">
  <!-- Desenvolvimento, Dados e Inteligência Artificial -->
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"></a>
  <a href="https://github.com/stanfordnlp/dspy"><img src="https://img.shields.io/badge/DSPy-C24D2C?style=for-the-badge&logoColor=white"></a>
  <a href="https://ollama.com/"><img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white"></a>
  <a href="https://ai.google.dev/gemma"><img src="https://img.shields.io/badge/Gemma-4285F4?style=for-the-badge&logo=google&logoColor=white"></a>
  
  <br>
  
  <a href="https://www.telegram.org/"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
  <a href="https://miro.com/"><img src="https://img.shields.io/badge/Miro-1A1A1A?style=for-the-badge&logo=miro&logoColor=white"/></a>
  <a href="https://www.atlassian.com/software/jira"><img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white"/></a>
  <a href="https://github.com/"><img src="https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
</h4>


## 📖 Manual de Instalação <a id="manual"></a>

### ⚙️ Pré-requisitos

- Git ([Download](https://git-scm.com/downloads))

- Python 3.9+ ([Download](https://www.python.org/downloads/))

- Ollama ([Download](https://ollama.com/download))

- Token de Bot do Telegram (via [BotFather](https://t.me/BotFather))

---

### 1. Clonar o Repositório Principal

```bash
git clone https://github.com/McLorem-Tecnologia/api-1-semestre-2026.git
cd api-1-semestre-2026
```

---

### 2. Configuração do Backend (IA e Bot)

**1° Inicialize os modelos de Inteligência Artificial localmente:**
```bash
ollama pull gemma4:e2b && ollama pull gemma3:1b
```

**2° Crie e Inicie o Ambiente Virtual Python:**
```bash
cd ./backend
python -m venv venv

# Se você usa Linux/Mac:
source venv/bin/activate 
# Se você usa Windows:
.\venv\Scripts\activate 	 
```

**3° Instale as dependências do projeto:**
```bash
pip install -r requirements.txt
```

**4° Configure as variáveis de ambiente:**
Dentro do diretório `backend/src/`, faça uma cópia do arquivo modelo `.env.example` e renomeie-a para `.env`. Em seguida, abra o arquivo `.env` e insira o seu token do Telegram.

**5° Inicie a aplicação:**
```bash
cd ./src
python main.py
```

**Saída Esperada:**
<br>
Mensagem de sucesso no terminal indicando que as configurações de IA foram carregadas e o Bot do Telegram está online.

---

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