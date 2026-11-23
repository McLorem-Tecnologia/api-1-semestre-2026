import math
import pandas as pd
from ia import procedures
from ia import utils


def dataframe_vendas_similares(
    data: str,
    clima_previsto: str | None = None,
    min_dias: int = 3
) -> pd.DataFrame:
    """
    Busca dias históricos equivalentes considerando:
    1. Dia da semana efetivo (Feriado = Domingo, Véspera = Sábado)
    2. Ciclo financeiro (Pagamento, Vale, Normal, Fim de Mês)
    3. Condição climática (Chuvoso, Frio, Calor, Neutro)
    """
    vendas = procedures.vendas.todas_as_vendas()
    alvo = utils.perfil_do_dia(data, clima_previsto)

    datas_unicas = vendas["Data"].unique()
    perfis = {str(d): utils.perfil_do_dia(str(d)) for d in datas_unicas}

    # Nível 1: Mesmo Dia Efetivo + Mesma Fase Financeira + Mesmo Clima
    datas_match = [
        d for d, p in perfis.items()
        if p["dow_efetivo"] == alvo["dow_efetivo"]
        and p["fase_financeira"] == alvo["fase_financeira"]
        and p["clima_grupo"] == alvo["clima_grupo"]
        and d != data
    ]

    # Nível 2 (Fallback de Clima): Mesmo Dia Efetivo + Mesma Fase Financeira
    if len(datas_match) < min_dias:
        datas_match = [
            d for d, p in perfis.items()
            if p["dow_efetivo"] == alvo["dow_efetivo"]
            and p["fase_financeira"] == alvo["fase_financeira"]
            and d != data
        ]

    # Nível 3 (Fallback Geral): Apenas Mesmo Dia Efetivo (ex: todos os Domingos/Feriados)
    if len(datas_match) < min_dias:
        datas_match = [
            d for d, p in perfis.items()
            if p["dow_efetivo"] == alvo["dow_efetivo"]
            and d != data
        ]

    return vendas[vendas["Data"].isin(datas_match)].copy()


def dataframe_vendas_por_periodo(data: str, periodo: str) -> pd.DataFrame:
    """Vendas históricas de dias com o mesmo perfil da data alvo, filtradas por UM período."""
    vendas = dataframe_vendas_similares(data)
    if not isinstance(vendas, pd.DataFrame) or vendas.empty:
        return pd.DataFrame()
    return vendas[vendas["Período"].str.lower() == periodo.lower()].copy()


def media_vendas_produtos(vendas_similares: pd.DataFrame, setor: str = None) -> list:
    """
    Calcula a média de saída e aplica a MARGEM DE PRODUÇÃO (+5%).
    Retorna uma lista de strings pronta para a IA exibir.
    """
    dados = pd.DataFrame(vendas_similares)
    if dados.empty:
        return []

    if setor is not None:
        skus_setor = [p["SKU"] for p in procedures.produtos.buscar_por_setor(setor)]
        dados = dados[dados["SKU"].isin(skus_setor)]

    total_dia = dados.groupby(["Data", "SKU"])["Qtd"].sum()
    medias = total_dia.groupby("SKU").mean()

    nomes = procedures.produtos.obter_dicionario_sku_nome()

    return [f"{nomes.get(sku, sku)}: {math.ceil(media * 1.05)}" for sku, media in medias.items()]


def calcular_producao_data(data: str, setor: str = "") -> dict | None:
    """Soma vendas e descartes registrados na data, por produto."""
    produtos = procedures.produtos.produtos_por_setor(setor)
    if setor and not produtos:
        return None

    skus_permitidos = {int(produto["SKU"]) for produto in produtos}
    vendas = procedures.vendas.buscar_por_data(data)
    if not vendas.empty:
        vendas = vendas[vendas["SKU"].isin(skus_permitidos)].copy()
        vendas["Qtd"] = pd.to_numeric(vendas["Qtd"], errors="coerce").fillna(0)
        vendas_por_sku = vendas.groupby("SKU")["Qtd"].sum().to_dict()
    else:
        vendas_por_sku = {}

    descartes = procedures.descarte.carregar_dados()
    if not descartes.empty:
        datas_descarte = pd.to_datetime(descartes["Data"], errors="coerce")
        descartes = descartes[
            (datas_descarte.dt.strftime("%d/%m/%Y") == data)
            & descartes["SKU"].isin(skus_permitidos)
        ].copy()
        descartes["Descarte"] = pd.to_numeric(descartes["Descarte"], errors="coerce").fillna(0)
        descarte_por_sku = descartes.groupby("SKU")["Descarte"].sum().to_dict()
    else:
        descarte_por_sku = {}

    resultados = {}
    for produto in produtos:
        sku = int(produto["SKU"])
        vendas_sku = float(vendas_por_sku.get(sku, 0))
        descarte_sku = float(descarte_por_sku.get(sku, 0))
        if vendas_sku or descarte_sku:
            resultados[produto["Produto"]] = {
                "producao": vendas_sku + descarte_sku,
                "vendas": vendas_sku,
                "descarte": descarte_sku,
            }
    return resultados
