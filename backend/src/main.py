import os
from pathlib import Path
from dotenv import load_dotenv
from ia.config import iniciar_configuracoes_ia
from bot.telegram_bot import iniciar_bot

# 1. Define o caminho dinâmico para o arquivo .env
# ATENÇÃO Criar .env dentro da pasta src 
current_dir = Path(__file__).resolve()
env_path = current_dir.parent / '.env'

load_dotenv(dotenv_path=env_path)

TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")

if not TELEGRAM_BOT_KEY:
    raise ValueError("A variável TELEGRAM_BOT_KEY não foi encontrada no arquivo .env!")

# Inicializar Ollama e Telegram Bot
if __name__ == "__main__":
    iniciar_configuracoes_ia()
    iniciar_bot(TELEGRAM_BOT_KEY)