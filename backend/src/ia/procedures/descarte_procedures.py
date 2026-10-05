from pathlib import Path
import pandas as pd


CAMINHO_ARQUIVO = (
    Path(__file__).resolve().parents[3]
    / "dados"
    / "descarte_supermercado_setembro_2026.csv"
)


def carregar_dados():
    return pd.read_csv(CAMINHO_ARQUIVO, sep=";")
#lê a planilha do csv


def buscar_por_produto(produto):
    dados = carregar_dados()

    resultado = dados[
        dados["Produto"].str.lower() == produto.lower()
    ]

    return resultado
#mostra os registros de um produto especifico


def somar_desperdicio_por_produto():
    dados = carregar_dados()

    resultado = (
        dados.groupby("Produto")["Descarte"]
        .sum()
        .reset_index()
    )

    return resultado
#soma o desperdicio de cada produto

def somar_desperdicio_por_produto_dia():
    dados = carregar_dados()

    resultado = (
        dados.groupby(["Data", "Produto"])["Descarte"]
        .sum()
        .reset_index()
    )

    return resultado
#soma desperdicio de cada produto em cada dia


def somar_desperdicio_por_data():
    dados = carregar_dados()

    resultado = (
        dados.groupby("Data")["Descarte"]
        .sum()
        .reset_index()
    )

    return resultado
#soma o desperdicio total de cada data


def listar_produtos():
    dados = carregar_dados()

    return dados["Produto"].unique().tolist()
#lista os produtos sem repetir


def calcular_desperdicio_total():
    dados = carregar_dados()

    return dados["Descarte"].sum()
#soma todo o desperdício da planilha


def produto_com_maior_desperdicio():
    dados = carregar_dados()

    resultado = (
        dados.groupby("Produto")["Descarte"]
        .sum()
        .sort_values(ascending=False)
    )

    return resultado.head(1)
#produto com maior desperdicio

def data_com_maior_desperdicio():
    dados = carregar_dados()

    resultado = (
        dados.groupby("Data")["Descarte"]
        .sum()
        .sort_values(ascending=False)
    )

    return resultado.head(1)
#descobrir o dia com maior desperdicio

def data_com_menor_desperdicio():
    dados = carregar_dados()

    resultado = (
        dados.groupby("Data")["Descarte"]
        .sum()
        .sort_values()
    )

    return resultado.head(1)
#descobrir o dia com menor desperdicio

def top_5_produtos_desperdicio():
    dados = carregar_dados()

    resultado = (
        dados.groupby("Produto")["Descarte"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    return resultado
#5 produtos com mais desperdicio

def media_desperdicio_por_dia():
    dados = carregar_dados()

    desperdicio_por_data = (
        dados.groupby("Data")["Descarte"]
        .sum()
    )

    return desperdicio_por_data.mean()
#média de desperdicio por dia

def buscar_por_data(data):
    dados = carregar_dados()

    resultado = dados[dados["Data"] == data]

    return resultado
#consultar desperdicio em uma data especifica

def buscar_desperdicio_por_produto_data(produto, data):
    dados = carregar_dados()

    resultado = dados[
        (dados["Produto"].str.lower() == produto.lower())
        & (dados["Data"] == data)
    ]

    return resultado
#consultar o desperdicio de um produto em uma data

def produtos_acima_do_limite(limite):
    dados = carregar_dados()

    resultado = (
        dados.groupby("Produto")["Descarte"]
        .sum()
    )

    resultado = resultado[resultado > limite]

    return resultado.sort_values(ascending=False)
#verificar se a quantidade limite de desperdicio foi ultrapassada pelos produtos, por mes

def buscar_por_intervalo(data_inicio, data_fim):
    dados = carregar_dados()
    dados["Data"] = pd.to_datetime(
    dados["Data"],
    format="%d/%m/%Y"
    )
    inicio = pd.to_datetime(data_inicio, format="%d/%m/%Y")
    fim = pd.to_datetime(data_fim, format="%d/%m/%Y")

    resultado = dados[
        (dados["Data"] >= inicio) &
        (dados["Data"] <= fim)
    ]
    return resultado
#busca em um intervalo de datas os dados
