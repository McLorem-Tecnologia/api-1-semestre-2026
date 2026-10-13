import math
import pandas as pd
from ia import procedures
from ia import utils

def dataframe_vendas_similares(data: str) -> pd.DataFrame:
    """Busca dias passados que tenham o mesmo perfil (pico ou comum) da data alvo."""
    vendas = procedures.vendas.todas_as_vendas()
    filtro_dia = utils.classificar_dia(data)
    datas_unicas = vendas["Data"].unique()
    print(f"Datas únicas encontradas: {len(datas_unicas)}")
    mapa_dias = {d: utils.classificar_dia(str(d)) for d in datas_unicas}
    filtro = vendas["Data"].map(mapa_dias) == filtro_dia
    
    return vendas[filtro]

def media_vendas_produtos(vendas_similares: pd.DataFrame, setor: str = None) -> list:
    """
    Calcula a média de saída e aplica a MARGEM DE PRODUÇÃO (+30%).
    Retorna uma lista de strings pronta para a IA exibir.
    """
    dados = pd.DataFrame(vendas_similares)
    
    if setor is not None:
        skus_setor = [p["SKU"] for p in procedures.produtos.buscar_por_setor(setor)]
        dados = dados[dados["SKU"].isin(skus_setor)]

    total_dia = dados.groupby(["Data", "SKU"])["Qtd"].sum()
    medias = total_dia.groupby("SKU").mean()

    nomes = procedures.produtos.obter_dicionario_sku_nome()
    
    return [f"{nomes.get(sku, sku)}: {math.ceil(media * 1.3)}" for sku, media in medias.items()]

def calcular_producao_data(data: str, setor: str = None) -> dict:
    """Cruza Vendas e Descartes usando o SKU para calcular a Produção real."""
    
    dicionario_bruto = procedures.produtos.obter_dicionario_sku_nome()
    nomes_produtos = {str(sku): nome for sku, nome in dicionario_bruto.items()}
    
    if setor:
        produtos_alvo = procedures.produtos.buscar_por_setor(setor)
        if not produtos_alvo:
            return None
        skus_alvo = [str(p.get("SKU")) for p in produtos_alvo]
    else:
        skus_alvo = list(nomes_produtos.keys())

    dados_vendas = procedures.vendas.buscar_por_data(data)
    dados_descarte = procedures.descarte.buscar_por_data(data)
    
    if isinstance(dados_vendas, pd.DataFrame): dados_vendas = dados_vendas.to_dict('records')
    if isinstance(dados_descarte, pd.DataFrame): dados_descarte = dados_descarte.to_dict('records')

    def limpar_numero(valor):
        try: return int(float(str(valor).replace(',', '.').strip()))
        except (ValueError, TypeError): return 0

    resumo = {sku: {"vendas": 0, "descarte": 0} for sku in skus_alvo}

    for item in dados_vendas:
        if isinstance(item, dict):
            sku_item = str(item.get("SKU"))
            if sku_item in skus_alvo:
                qtd = item.get("Qtd", item.get("Quantidade", 0))
                resumo[sku_item]["vendas"] += limpar_numero(qtd)

    for item in dados_descarte:
        if isinstance(item, dict):
            sku_item = str(item.get("SKU"))
            if sku_item in skus_alvo:
                qtd = item.get("Qtd", item.get("Quantidade", item.get("Descarte", 0)))
                resumo[sku_item]["descarte"] += limpar_numero(qtd)

    resultado_final = {}
    for sku, dados in resumo.items():
        producao = dados["vendas"] + dados["descarte"]
        if producao > 0:
            dados["producao"] = producao
            nome_legivel = nomes_produtos.get(sku, f"Produto Desconhecido ({sku})")
            resultado_final[nome_legivel] = dados
            
    return resultado_final