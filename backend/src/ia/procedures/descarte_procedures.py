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

def converter_data(data):
    """
    Converte uma data para o formato DD/MM/AAAA.

    Aceita datas no formato DD/MM/AAAA ou por extenso
    em português.

    Args:
        data (str): data que será convertida.

    Returns:
        str: data padronizada no formato DD/MM/AAAA.
        None: caso a data seja inválida ou não informada.
    """

    # Verifica se a data foi informada.
    if data is None:
        print("Erro: a data não foi informada.")
        return None

    # Verifica se a data é um texto.
    if not isinstance(data, str):
        print("Erro: a data deve ser informada como texto.")
        return None

    # Remove espaços extras e transforma o texto em minúsculo.
    data = data.strip().lower()

    # Verifica se a data está vazia.
    if not data:
        print("Erro: a data não pode estar vazia.")
        return None

    # Dicionário que relaciona os meses por extenso aos seus números.
    meses = {
        "janeiro": "01",
        "fevereiro": "02",
        "março": "03",
        "abril": "04",
        "maio": "05",
        "junho": "06",
        "julho": "07",
        "agosto": "08",
        "setembro": "09",
        "outubro": "10",
        "novembro": "11",
        "dezembro": "12"
    }

    try:
        # Verifica se a data já está no formato DD/MM/AAAA.
        if "/" in data:
            data_convertida = pd.to_datetime(
                data,
                format="%d/%m/%Y"
            )

        else:
            # Separa o dia, o mês e o ano.
            partes = data.replace(" de ", " ").split()

            if len(partes) != 3:
                raise ValueError

            dia, mes, ano = partes

            # Verifica se o mês existe no dicionário.
            if mes not in meses:
                raise ValueError

            # Monta a data no formato DD/MM/AAAA.
            data_formatada = f"{dia}/{meses[mes]}/{ano}"

            data_convertida = pd.to_datetime(
                data_formatada,
                format="%d/%m/%Y"
            )

        # Retorna a data padronizada.
        return data_convertida.strftime("%d/%m/%Y")

    except (ValueError, TypeError):
        print("Erro: data inválida.")
        return None

def buscar_por_produto(produto):
    """
    Busca os registros de descarte de um produto específico.

    Args:
        produto (str): nome ou parte do nome do produto que será pesquisado.

    Returns:
        pd.DataFrame: registros encontrados para o produto.
        Retorna um DataFrame vazio se o produto não for informado
        ou não for encontrado.
    """

    # Verifica se o nome do produto foi informado.
    if produto is None:
        print("Erro: o produto não foi informado.")
        return pd.DataFrame()

    # Carrega os dados de descarte.
    dados = carregar_dados()

    # Verifica se existem dados para consultar.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return pd.DataFrame()

    # Busca o produto pelo nome completo ou parcial,
    # ignorando diferenças entre maiúsculas e minúsculas.
    resultado = dados[
        dados["Produto"].str.contains(
            produto,
            case=False,
            na=False
        )
    ]

    # Verifica se algum produto foi encontrado.
    if resultado.empty:
        print("Aviso: produto não encontrado.")
        return pd.DataFrame()

    return resultado

def somar_desperdicio_por_produto():
    """
    Calcula a quantidade total de descarte de cada produto.

    Returns:
        pd.DataFrame: tabela contendo o nome de cada produto
        e a soma de seu descarte.
        Retorna um DataFrame vazio caso não existam dados.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar a soma.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return pd.DataFrame()

    # Agrupa os registros por produto e soma os descartes.
    resultado = (
        dados.groupby("Produto")["Descarte"]
        .sum()
        .reset_index()
    )

    return resultado

def somar_desperdicio_por_produto_dia():
    """
    Calcula a quantidade total de descarte de cada produto em cada dia.

    Returns:
        pd.DataFrame: tabela contendo a data, o produto e a soma
        do descarte correspondente.
        Retorna um DataFrame vazio caso não existam dados.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar a soma.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return pd.DataFrame()

    # Agrupa os registros por data e produto e soma os descartes.
    resultado = (
        dados.groupby(["Data", "Produto"])["Descarte"]
        .sum()
        .reset_index()
    )

    return resultado

def somar_desperdicio_por_data():
    """
    Calcula a quantidade total de descarte em cada data.

    Returns:
        pd.DataFrame: tabela contendo cada data e a soma
        do descarte correspondente.
        Retorna um DataFrame vazio caso não existam dados.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar a soma.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return pd.DataFrame()

    # Agrupa os registros por data e soma os descartes.
    resultado = (
        dados.groupby("Data")["Descarte"]
        .sum()
        .reset_index()
    )

    return resultado

def listar_produtos():
    """
    Retorna uma lista com os nomes dos produtos sem repetições.

    Returns:
        list: lista de produtos encontrados.
        Retorna uma lista vazia caso não existam dados.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para listar.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return []

    # Obtém os nomes dos produtos sem repetições.
    produtos = dados["Produto"].unique().tolist()

    return produtos

def calcular_desperdicio_total():
    """
    Calcula a quantidade total de descarte registrada.

    Returns:
        float ou int: soma de todos os descartes.
        None: caso não existam dados para realizar o cálculo.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar o cálculo.
    if dados.empty:
        print("Aviso: não há dados para calcular o descarte total.")
        return None

    # Soma todos os valores da coluna Descarte.
    total = dados["Descarte"].sum()

    return total

def produto_com_maior_desperdicio():
    """
    Identifica o produto com a maior quantidade total de descarte.

    Returns:
        pd.Series: nome do produto e quantidade descartada.
        None: caso não existam dados para realizar a consulta.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar a consulta.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return None

    # Agrupa por produto e soma os descartes.
    resultado = (
        dados.groupby("Produto")["Descarte"]
        .sum()
        .sort_values(ascending=False)
    )

    # Retorna somente o produto com maior descarte.
    return resultado.head(1)

def data_com_maior_desperdicio():
    """
    Identifica a data com a maior quantidade total de descarte.

    Returns:
        pd.Series: data e quantidade total descartada.
        None: caso não existam dados para realizar a consulta.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar a consulta.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return None

    # Agrupa por data e soma os descartes.
    resultado = (
        dados.groupby("Data")["Descarte"]
        .sum()
        .sort_values(ascending=False)
    )

    # Retorna somente a data com maior descarte.
    return resultado.head(1)

def data_com_menor_desperdicio():
    """
    Identifica a data com a menor quantidade total de descarte.

    Returns:
        pd.Series: data e quantidade total descartada.
        None: caso não existam dados para realizar a consulta.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar a consulta.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return None

    # Agrupa por data, soma os descartes e ordena do menor para o maior.
    resultado = (
        dados.groupby("Data")["Descarte"]
        .sum()
        .sort_values(ascending=True)
    )

    # Retorna somente a data com menor descarte.
    return resultado.head(1)

def top_5_produtos_desperdicio():
    """
    Retorna os cinco produtos com maior quantidade total de descarte.

    Returns:
        pd.DataFrame: tabela com os cinco produtos e suas quantidades
        de descarte.
        Retorna um DataFrame vazio caso não existam dados.
    """

    # Carrega os dados de descarte já tratados.
    dados = carregar_dados()

    # Verifica se existem dados para realizar a consulta.
    if dados.empty:
        print("Aviso: não há dados para consultar.")
        return pd.DataFrame()

    # Agrupa por produto, soma os descartes e ordena do maior para o menor.
    resultado = (
        dados.groupby("Produto")["Descarte"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    return resultado

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
