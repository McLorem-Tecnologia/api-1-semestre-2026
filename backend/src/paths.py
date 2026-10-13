from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent

BACKEND_DIR = SRC_DIR.parent
ENV_PATH = SRC_DIR / ".env"

DADOS_DIR = BACKEND_DIR / "dados"
DESCARTE_DIR = DADOS_DIR / "descarte"
REGRAS_DIR = DADOS_DIR / "regras"
VENDAS_DIR = DADOS_DIR / "vendas"