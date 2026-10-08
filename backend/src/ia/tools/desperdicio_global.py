from ia.tools.utils import dspy_tool
from ia.procedures import procedures
@dspy_tool


def tool_buscar_por_intervalo(data_inicio: str, data_fim: str) -> str:
    resultado = procedures.descarte.buscar_por_intervalo(
        data_inicio,
        data_fim
    )
    #Pega as tabelas dos descartes
    produtos_agrupados = (
        resultado.groupby("Produto")["Descarte"]
        .sum()
        .reset_index()
    )
    # Agrupa os repetidos
    for _, linha in produtos_agrupados.iterrows():
        produto = linha["Produto"]
        quantidade_descartada = linha["Descarte"]
        ingredientes = procedures.ingredientes.buscar_ingredientes(produto)
        print(produto)
        print(ingredientes)
        print(quantidade_descartada)
    # Mostra o nome do produto atual
    # Mostra os ingredientes
    # Mostra o total de descartes
    return str(produtos_agrupados)
