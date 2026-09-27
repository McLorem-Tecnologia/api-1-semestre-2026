import pandas as pd
from ia.procedures import procedures

def calcular_producao_data(data: str, setor: str = None) -> dict:
    """Busca vendas e descartes, limpa os dados e retorna o cálculo matemático puro.
    Pode filtrar por setor ou trazer a produção de todo o supermercado."""
    
    if setor:
        produtos_alvo = procedures.produtos.buscar_por_setor(setor)
        if not produtos_alvo:
            return None
        nomes_produtos = [p["Produto"] for p in produtos_alvo]
    else:
        nomes_produtos = procedures.produtos.listar()

    dados_vendas = procedures.vendas.buscar_por_data(data)
    dados_descarte = procedures.descarte.buscar_por_data(data)
    
    if isinstance(dados_vendas, pd.DataFrame): dados_vendas = dados_vendas.to_dict('records')
    if isinstance(dados_descarte, pd.DataFrame): dados_descarte = dados_descarte.to_dict('records')

    def limpar_numero(valor):
        try: return int(float(str(valor).replace(',', '.').strip()))
        except (ValueError, TypeError): return 0

    resumo = {nome: {"vendas": 0, "descarte": 0} for nome in nomes_produtos}

    for item in dados_vendas:
        if isinstance(item, dict) and item.get("Produto") in nomes_produtos:
            qtd = item.get("Qtd", item.get("Quantidade", 0))
            resumo[item["Produto"]]["vendas"] += limpar_numero(qtd)

    for item in dados_descarte:
        if isinstance(item, dict) and item.get("Produto") in nomes_produtos:
            qtd = item.get("Qtd", item.get("Quantidade", item.get("Descarte", 0)))
            resumo[item["Produto"]]["descarte"] += limpar_numero(qtd)

    resultado_final = {}
    for produto, dados in resumo.items():
        producao = dados["vendas"] + dados["descarte"]
        if producao > 0:
            dados["producao"] = producao
            resultado_final[produto] = dados
            
    return resultado_final