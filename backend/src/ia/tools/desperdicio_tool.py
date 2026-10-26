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
    
    data_inicio, setor, texto_data = _tratar_parametros_iniciais(data_inicio, setor)
    if data_fim and str(data_fim).strip().lower() not in ['none', 'null']:
        data_fim, _, _ = _tratar_parametros_iniciais(data_fim, setor)
    else:
        data_fim = data_inicio 

    if data_inicio != data_fim:
        texto_data = f"no período de {data_inicio} a {data_fim}"

    resultado = procedures.descarte.buscar_por_intervalo(
        data_inicio,
        data_fim
    #Pega os descartes do intervalo
    )
    if setor:
        produtos = pd.read_csv(
            DADOS_DIR / "produtos.csv",
            sep=";",
            encoding="utf-8-sig"
        )

        resultado = resultado.merge(
            produtos[["SKU", "Setor"]],
            on="SKU",
            how="left"
        )
        #Seleciona só SKU e Setor

        resultado = resultado[
            resultado["Setor"].str.lower() == setor.lower()
        ]
    #Filtra pelo setor, se inserido
    historico = pd.read_csv(
        DADOS_DIR / "historico_ingredientes.csv",
        sep=";",
        encoding="utf-8-sig"
    )
    historico["Data"] = pd.to_datetime(
        historico["Data"], format="%d/%m/%Y"
    )

    # Pega as tabelas dos descartes
    produtos_agrupados = (
        resultado.groupby(["Data", "SKU"])["Descarte"]
        .sum()
        .reset_index()
    )

    # Agrupa os repetidos
    custo_total_descarte = 0

    for _, linha in produtos_agrupados.iterrows():
        sku = linha["SKU"]
        quantidade_descartada = linha["Descarte"]
        data_descarte = linha["Data"]
        #Percorres os produtos descartados
        ingredientes = procedures.ingredientes.buscar_ingredientes(sku)
        #Busca os ingredientes
        precos = (
            historico[historico["Data"] <= data_descarte]
            .sort_values("Data")
            .drop_duplicates("Ingrediente", keep="last")
        )
        #Encontra os preços históricos

        ingredientes = ingredientes.merge(
            precos[["Ingrediente", "Preço Custo"]],
            on="Ingrediente",
            how="left",
            suffixes=("", "_hist")
        )
        #Junta os ingredientes aos preços
        if ingredientes["Preço Custo_hist"].isna().any():
            return "Erro: faltam preços históricos para alguns ingredientes."

        custo_ingredientes = (
            ingredientes["Qtd"] * ingredientes["Preço Custo_hist"]
        ).sum()
        #Verifica caso houver preços faltantes
        custo_descarte = custo_ingredientes * quantidade_descartada
        custo_total_descarte += custo_descarte


    aviso_setor = f" (Setor: {setor})" if setor else ""

    return f"Custo total do desperdício {texto_data}{aviso_setor}: R$ {custo_total_descarte:.2f}"
