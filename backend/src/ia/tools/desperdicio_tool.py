from ia.tools import dspy_tool
from ia.tools.producao_tool import _tratar_parametros_iniciais
from ia import procedures
import pandas as pd
from paths import DADOS_DIR

@dspy_tool("DESPERDICIO")
def tool_buscar_por_intervalo(data_inicio: str = "hoje", data_fim: str = "", setor: str = "") -> str:
    """
    Consulta o custo total do desperdício de produtos em um período.

    Use esta ferramenta quando o usuário perguntar sobre custo,
    valor ou prejuízo do desperdício/descarte em uma data ou entre duas datas.

    Parâmetros:
    - data_inicio (opcional): data ou referência de tempo exatamente como o usuário disse, sem
      calcular a data. Aceita datas numéricas ('20/09/2026'), por extenso ('2 de novembro de 2026'),
      termos relativos ('hoje', 'ontem', 'amanhã', 'depois de amanhã'), contagem de dias
      ('há 2 dias', 'daqui a 5 dias') e dias da semana ('segunda passada', 'próxima sexta').
      Se não especificado, assume 'hoje'.
    - data_fim (opcional): mesmo formato de data_inicio. Informe somente quando o usuário
      pedir um período (ex.: 'de 1 a 15 de setembro'). Se não especificado, a consulta
      vale apenas para a data_inicio.
    - setor (opcional): nome do setor (ex: 'Padaria'). Deixe vazio se não for especificado.

    Se o usuário especificar um setor, informe-o no parâmetro setor.
    Caso contrário, deixe setor vazio.

    Retorna o custo calculado a partir dos registros de descarte
    e dos custos dos ingredientes. Nunca estime o valor por conta própria.
    """

    try:
        if not data_inicio:
            return "Erro: data inicial não informada."

        data_inicio, setor, texto_data = _tratar_parametros_iniciais(data_inicio, setor)

        if data_fim and str(data_fim).strip().lower() not in ["none", "null"]:
            data_fim, _, _ = _tratar_parametros_iniciais(data_fim, setor)
        else:
            data_fim = data_inicio

    except (ValueError, TypeError) as erro:
        return f"Erro: parâmetro de data inválido. {erro}"

    try:
        inicio = pd.to_datetime(data_inicio, format="%d/%m/%Y")
        fim = pd.to_datetime(data_fim, format="%d/%m/%Y")

        if inicio > fim:
            return "Erro: a data inicial não pode ser posterior à data final."

    except (ValueError, TypeError):
        return "Erro: formato de data inválido."

    if data_inicio != data_fim:
        texto_data = f"no período de {data_inicio} a {data_fim}"

    resultado = procedures.descarte.buscar_por_intervalo(
        data_inicio,
        data_fim
    )

    if resultado is None or resultado.empty:
        return "Não foram encontrados registros de desperdício no período informado."

    if not {"SKU", "Data", "Descarte"}.issubset(resultado.columns):
        return "Erro: faltam colunas obrigatórias nos registros de descarte."
    #Filtra os descartes pelo setor informado
    if setor:
        try:
            produtos = pd.read_csv(
                DADOS_DIR / "produtos.csv",
                sep=";",
                encoding="utf-8-sig"
            )

            if produtos.empty:
                return "Erro: produtos.csv está vazio."
            if not {"SKU", "Setor"}.issubset(produtos.columns):
                return "Erro: faltam colunas obrigatórias em produtos.csv."

        except FileNotFoundError:
            return "Erro: arquivo produtos.csv não encontrado."
        except pd.errors.EmptyDataError:
            return "Erro: produtos.csv está vazio."
        except pd.errors.ParserError:
            return "Erro: não foi possível ler produtos.csv."

        resultado = resultado.merge(
            produtos[["SKU", "Setor"]],
            on="SKU",
            how="left"
        )

        resultado = resultado[
            resultado["Setor"].fillna("").str.lower() == setor.lower()
        ]
    #Carrega e valida o histórico de ingredientes
    try:
        historico = pd.read_csv(
            DADOS_DIR / "historico_ingredientes.csv",
            sep=";",
            encoding="utf-8-sig"
        )

        if historico.empty:
            return "Erro: historico_ingredientes.csv está vazio."

        if not {"Data", "Ingrediente", "Preço Custo"}.issubset(historico.columns):
            return "Erro: faltam colunas obrigatórias em historico_ingredientes.csv."

        historico["Data"] = pd.to_datetime(
            historico["Data"],
            format="%d/%m/%Y",
            errors="coerce"
        )
        historico = historico.dropna(subset=["Data"])

        if historico.empty:
            return "Erro: não existem datas válidas no histórico de ingredientes."

        historico["Preço Custo"] = pd.to_numeric(
            historico["Preço Custo"],
            errors="coerce"
        )

        historico = historico.dropna(subset=["Preço Custo"])

        if historico.empty:
            return "Erro: não existem preços válidos no histórico de ingredientes."
    except FileNotFoundError:
        return "Erro: arquivo historico_ingredientes.csv não encontrado."
    except pd.errors.EmptyDataError:
        return "Erro: historico_ingredientes.csv está vazio."
    except pd.errors.ParserError:
        return "Erro: não foi possível ler historico_ingredientes.csv."

    # Converte os valores de descarte para números
    resultado["Descarte"] = pd.to_numeric(
        resultado["Descarte"],
        errors="coerce"
    )

    resultado = resultado.dropna(subset=["Descarte"])
    if resultado.empty:
        return "Não foram encontrados registros válidos de desperdício no período informado."
    #Agrupa os descartes repetidos por produto e data
    produtos_agrupados = resultado.groupby(
        ["SKU", "Data"],
        as_index=False
    )["Descarte"].sum()
    custo_total_descarte = 0
    #Calcula o custo dos ingredientes de cada produto descartado
    for _, linha in produtos_agrupados.iterrows():
        sku = linha["SKU"]
        quantidade_descartada = linha["Descarte"]
        data_descarte = linha["Data"]
        # Busca os ingredientes associados ao produto
        ingredientes = procedures.ingredientes.buscar_ingredientes(sku)

        if ingredientes is None or ingredientes.empty:
            continue

        if not {"Ingrediente", "Qtd"}.issubset(ingredientes.columns):
            return "Erro: faltam colunas obrigatórias nos ingredientes."

        ingredientes["Qtd"] = pd.to_numeric(
            ingredientes["Qtd"],
            errors="coerce"
        )

        ingredientes = ingredientes.dropna(subset=["Qtd"])
        #Seleciona o preço histórico mais recente até a data do descarte
        precos = (
            historico[historico["Data"] <= data_descarte]
            .sort_values("Data")
            .drop_duplicates("Ingrediente", keep="last")
        )
        #Associa os ingredientes aos respectivos preços históricos
        ingredientes = ingredientes.merge(
            precos[["Ingrediente", "Preço Custo"]],
            on="Ingrediente",
            how="left",
            suffixes=("", "_hist")
        )
        if ingredientes["Preço Custo_hist"].isna().any():
            return "Erro: faltam preços históricos para alguns ingredientes."
        #Calcula o custo total dos ingredientes
        custo_ingredientes = (
            ingredientes["Qtd"] * ingredientes["Preço Custo_hist"]
        ).sum()
        #Calcula e acumula o custo de desperdício
        custo_descarte = custo_ingredientes * quantidade_descartada
        custo_total_descarte += custo_descarte


    aviso_setor = f" (Setor: {setor})" if setor else ""

    return f"Custo total do desperdício {texto_data}{aviso_setor}: R$ {custo_total_descarte:.2f}"
