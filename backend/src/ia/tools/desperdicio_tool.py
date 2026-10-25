from ia.tools import dspy_tool
from ia import procedures
import pandas as pd
from paths import DADOS_DIR

@dspy_tool("DESPERDICIO")
def tool_buscar_por_intervalo(data_inicio: str, data_fim: str, setor: str | None = None) -> str:
    """
    Consulta o custo total do desperdício de produtos em um período.

    Use esta ferramenta quando o usuário perguntar sobre custo,
    valor ou prejuízo do desperdício/descarte entre duas datas.

    Parâmetros:
    - data_inicio: data inicial no formato DD/MM/AAAA.
    - data_fim: data final no formato DD/MM/AAAA.
    - setor: setor opcional, como Padaria, Cozinha, Peixaria,
      Açougue ou Processados.

    Se o usuário especificar um setor, informe-o no parâmetro setor.
    Caso contrário, deixe setor como None.

    Retorna o custo calculado a partir dos registros de descarte
    e dos custos dos ingredientes. Nunca estime o valor por conta própria.
    """
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


    if setor:
        return f"Custo total do desperdício no setor {setor}: R$ {custo_total_descarte:.2f}"

    return f"Custo total do desperdício no período: R$ {custo_total_descarte:.2f}"
