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