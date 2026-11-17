import pandas as pd
from paths import DESCARTE_DIR, DADOS_DIR

def carregar_dados():
    """
    Carrega os arquivos CSV de descarte, valida os registros,
    relaciona os descartes com os nomes dos produtos pelo SKU
    e remove dados inválidos.

    A função procura todos os arquivos com o padrão
    'descarte_*.csv' dentro do diretório de descartes.

    Valida:
        - Existência dos arquivos e das colunas obrigatórias.
        - Datas inválidas ou ausentes.
        - SKUs ausentes.
        - Produtos sem SKU ou nome.
        - SKUs sem correspondência na tabela de produtos.
        - Valores de descarte inválidos ou ausentes.

    Returns:
        pd.DataFrame: tabela com as colunas Data, SKU,
        Descarte e Produto, contendo somente registros válidos.
        Retorna um DataFrame vazio caso não existam dados válidos
        ou ocorra algum erro na leitura da tabela de produtos.
    """

    # Procura todos os arquivos CSV de descarte.
    arquivos = sorted(DESCARTE_DIR.glob("descarte_*.csv"))

    if not arquivos:
        print("Nenhum arquivo de descarte encontrado.")
        return pd.DataFrame()

    tabelas = []

    # Define as colunas obrigatórias dos arquivos de descarte.
    colunas_descarte = ["Data", "SKU", "Descarte"]

    # Percorre cada arquivo encontrado.
    for arquivo in arquivos:
        try:
            tabela = pd.read_csv(
                arquivo,
                sep=";",
                encoding="utf-8-sig"
            )

            if tabela.empty:
                print(f"Aviso: {arquivo.name} não possui dados. Pulando arquivo.")
                continue

            # Verifica se faltam colunas obrigatórias.
            colunas_faltando = [
                coluna for coluna in colunas_descarte
                if coluna not in tabela.columns
            ]

            if colunas_faltando:
                print(
                    f"Aviso: {arquivo.name} não possui "
                    f"as colunas {colunas_faltando}."
                )
                continue

            # Adiciona somente arquivos válidos à lista.
            tabelas.append(tabela)

        except pd.errors.EmptyDataError:
            print(f"Aviso: {arquivo.name} está vazio. Pulando arquivo.")
            continue

        except FileNotFoundError:
            print(f"Aviso: arquivo {arquivo.name} não encontrado.")
            continue

    if not tabelas:
        print("Nenhum arquivo de descarte válido encontrado.")
        return pd.DataFrame()

    # Junta todos os arquivos em uma única tabela.
    descartes = pd.concat(tabelas, ignore_index=True)

    # Valida as datas dos registros.
    datas_validas = pd.to_datetime(
        descartes["Data"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    invalidos = datas_validas.isna()

    if invalidos.any():
        print(
            f"Aviso: {invalidos.sum()} registros "
            "com datas inválidas foram ignorados."
        )

    descartes = descartes.loc[~invalidos].copy()

    # Identifica e remove registros sem SKU.
    invalidos = descartes["SKU"].isna()

    if invalidos.any():
        print(
            f"Aviso: {invalidos.sum()} registros "
            "sem SKU foram ignorados."
        )

    descartes = descartes.dropna(subset=["SKU"])

    if descartes.empty:
        print("Nenhum registro de descarte válido encontrado.")
        return pd.DataFrame()

    try:
        # Carrega a tabela de produtos.
        produtos = pd.read_csv(
            DADOS_DIR / "produtos.csv",
            sep=";",
            encoding="utf-8-sig"
        )

        if produtos.empty:
            print("Erro: produtos.csv não possui dados.")
            return pd.DataFrame()

        # Verifica as colunas obrigatórias dos produtos.
        colunas_produtos = ["SKU", "Produto"]

        colunas_faltando = [
            coluna for coluna in colunas_produtos
            if coluna not in produtos.columns
        ]

        if colunas_faltando:
            print(
                f"Erro: produtos.csv não possui "
                f"as colunas {colunas_faltando}."
            )
            return pd.DataFrame()

        # Remove produtos sem SKU ou nome.
        invalidos = (
            produtos["SKU"].isna() |
            produtos["Produto"].isna()
        )

        if invalidos.any():
            print(
                f"Aviso: {invalidos.sum()} produtos "
                "com SKU ou nome ausente foram ignorados."
            )

        produtos = produtos.dropna(subset=["SKU", "Produto"])

        # Relaciona os descartes aos produtos pelo SKU.
        dados = pd.merge(
            descartes,
            produtos[["SKU", "Produto"]],
            on="SKU",
            how="left"
        )

        # Remove registros sem produto correspondente.
        invalidos = dados["Produto"].isna()

        if invalidos.any():
            print(
                f"Aviso: {invalidos.sum()} registros "
                "sem produto correspondente foram ignorados."
            )

        dados = dados.dropna(subset=["Produto"])

    except FileNotFoundError:
        print("Erro: arquivo produtos.csv não encontrado.")
        return pd.DataFrame()

    except pd.errors.EmptyDataError:
        print("Erro: arquivo produtos.csv está vazio.")
        return pd.DataFrame()

    # Converte os valores de descarte para números.
    dados["Descarte"] = pd.to_numeric(
        dados["Descarte"],
        errors="coerce"
    )

    invalidos = dados["Descarte"].isna()

    if invalidos.any():
        print(
            f"Aviso: {invalidos.sum()} registros "
            "com descarte inválido foram ignorados."
        )

    dados = dados.dropna(subset=["Descarte"])

    # Retorna a tabela final tratada.
    return dados


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
#soma todo o disperdicio da planilha


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
