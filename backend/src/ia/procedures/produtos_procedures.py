# procedures.vendas.buscar_por_nome_produto()
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[3] / "dados" / "produtos_mercado.csv"

def buscar_por_nome_produto(nome_produto: str):
    """Busca um produto pelo nome."""
    df = pd.read_csv(path, sep=";")

    resultado = df[df['Produto'].str.contains(nome_produto, case=False, na=False)]

    return resultado.to_dict(orient='records')
    