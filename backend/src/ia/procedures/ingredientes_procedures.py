from pathlib import Path
import pandas as pd


CAMINHO_ARQUIVO = (
    Path(__file__).resolve().parents[3]
    / "dados"
    / "ingredientes_produtos.csv"
)

def carregar_dados():
    return pd.read_csv(CAMINHO_ARQUIVO, sep=";")
#lê a planilha do csv

def buscar_ingredientes(produto):
    dados = carregar_dados()
    resultado = dados[
        dados["Produto"].str.lower() == produto.lower()
    ]
    return resultado
