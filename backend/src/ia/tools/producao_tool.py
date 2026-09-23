# Funções para estimativa de produção.
# Função para TOOLS do DSPY relacionadas a produção.
import math
import sys
from pathlib import Path

import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ia.procedures import procedures
from ia.tools.utils import classificar_dia


def media_vendas_produtos(vendas, setor=None):
    """
    Calcula a média de vendas de cada produto e arredonda o resultado
    para cima.

    Args:
        vendas (list): Lista de vendas no formato de registros
            de um DataFrame do pandas.
        setor (str, opcional): Setor utilizado para filtrar os produtos.
            Se não for informado, calcula a média de todos os produtos.

    Returns:
        list: Lista contendo o nome de cada produto e sua média
            de vendas arredondada para cima.

            Exemplo:
            ['Brigadeiro: 4', 'Temaki: 7', 'Pão Francês: 4']
    """

    dados = pd.DataFrame(vendas)

    if setor is not None:
        produtos_setor = procedures.produtos.buscar_por_setor(setor)

        nomes_produtos = [
            produto["Produto"]
            for produto in produtos_setor
        ]

        dados = dados[
            dados["Produto"].isin(nomes_produtos)
        ]

    medias = dados.groupby("Produto")["Qtd"].mean()

    resultado = []

    for produto, media in medias.items():
        media_arredondada = math.ceil(media)

        resultado.append(
            f"{produto}: {media_arredondada}"
        )

    return resultado

def dataframe_vendas_similares(data: str, filtro_dia: int) -> pd.DataFrame:
    vendas = procedures.vendas.todas_as_vendas()
    if classificar_dia(data) != filtro_dia:
        return pd.DataFrame(columns=vendas.columns)
    filtro = vendas["Data"].apply(classificar_dia) == filtro_dia
    return vendas[filtro]