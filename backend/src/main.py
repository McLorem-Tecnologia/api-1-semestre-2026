import os
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bot.telegram_bot import iniciar_bot
from config import verificacao_ambiente

# Verifica se os módulos estão baixados corretamente
verificacao_ambiente()

TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_FATEC1_KEY")

if not TELEGRAM_BOT_KEY:
    raise ValueError("A variável TELEGRAM_BOT_FATEC1_KEY não foi encontrada no ambiente do sistema!")

# Inicializar Telegram Bot
iniciar_bot(TELEGRAM_BOT_KEY)
