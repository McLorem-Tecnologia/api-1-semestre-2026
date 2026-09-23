# Guia de instalação do projeto

## Descrição

Este repositório contém a aplicação desenvolvida para o 1º semestre do curso de Análise e Desenvolvimento de Sistemas da FATEC São José dos Campos. O projeto consiste em um Assistente de Análise de Dados integrado ao Telegram, utilizando Inteligência Artificial executada localmente para garantir autonomia e privacidade.

## Pré-requisitos

Git instalado na máquina - [Download](https://git-scm.com/downloads)

Python 3.9+ instalado - [Download](https://www.python.org/downloads/)

Ollama instalado - [Download](https://ollama.com/download)

Bot do Telegram configurado via [BotFather](https://t.me/BotFather)

## Clonando o Repositório

Para clonar o repositório principal, execute o seguinte comando no seu terminal:
```bash
git clone https://github.com/McLorem-Tecnologia/api-1-semestre-2026.git
```

## Inicializando a Aplicação

#### - Inicialize o Serviço da IA no localhost: 
Certifique-se de que o aplicativo do Ollama está aberto. Em seguida, baixe os modelos necessários no terminal:
```bash
ollama pull gemma4:e2b && ollama pull gemma3:1b
```

#### Instale as dependências

Após clonar o repositório, siga os passos abaixo para configurar o ambiente e iniciar a aplicação:

Entre no diretório do backend e isole o ambiente:
```bash
# Entre no repositório do backend
cd ./api-1-semestre-2026/backend

# Crie o ambiente virtual python (caso já tenha, pule esse comando)
python -m venv venv

# Inicie o ambiente virtual (Windows)
.\venv\Scripts\activate
# (Para Linux ou macOS use: source venv/bin/activate)

# Instale as dependências
pip install -r requirements.txt
```

Configure as **variáveis de ambiente** conforme necessário. O repositório já fornece um arquivo modelo chamado `.env.example` no diretório `./backend/src`.

Faça uma cópia deste arquivo, renomeie-a para `.env` e adicione as suas chaves. As chaves da API não devem ser subidas para o repositório.

Conteúdo base do arquivo `.env.example`:
```env
TELEGRAM_BOT_KEY=seu_token_gerado_no_botfather_aqui
```

#### Inicie os serviços.

Servidor Backend e Integração Telegram:

```bash
# Entre no diretório do código-fonte (caso ainda não esteja)
cd ./src

# Certifique-se de que o ambiente virtual (venv) está ativo
# Inicie a Aplicação Principal
python main.py
```