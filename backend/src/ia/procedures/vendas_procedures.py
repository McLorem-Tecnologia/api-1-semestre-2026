import pandas as pd
import math
from ia.tools.utils import classificar_dia
from ia.procedures import procedures
from pathlib import Path

path1 = Path(__file__).resolve().parents[3] / "dados" / "vendas_supermercado_agosto_2026.csv"
path2 = Path(__file__).resolve().parents[3] / "dados" / "vendas_supermercado_setembro_2026.csv"
vsa, vss = pd.read_csv(path1, sep=";"), pd.read_csv(path2, sep=";")
tabela = pd.concat([vsa, vss], ignore_index=True)

def buscar_por_nome_produto(nome):
    return tabela[tabela["Produto"].str.contains(nome, case=False, na=False)]

def buscar_por_periodo(periodo):
    return tabela[tabela["Período"].str.contains(periodo, case=False, na=False)]

def buscar_por_data(data):
    return tabela[tabela["Data"] == data]

def produtos_mais_vendidos(limite):
    if limite <= 0:
        return None
    else:
        return tabela.groupby("Produto")["Qtd"].sum().sort_values(ascending=False).head(limite) 

def todas_as_vendas():
    return tabela
 
def dataframe_vendas_similares(data: str, filtro_dia: int) -> pd.DataFrame:
    vendas = todas_as_vendas()
    if classificar_dia(data) != filtro_dia:
        return pd.DataFrame(columns=vendas.columns)
    filtro = vendas["Data"].apply(classificar_dia) == filtro_dia
    print(vendas[filtro])
    return vendas[filtro]

def media_vendas_produtos(vendas: pd.DataFrame, setor: str = None):
    """
    Calcula a média de vendas de cada produto, incluir a margem de 30% e arredonda o resultado
    para cima.

    Args:
        vendas (pd.DataFrame): Lista de vendas no formato de registros
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
        resultado.append(
            f"{produto}: {math.ceil(media * 1.3)}"
        )

    return resultado  