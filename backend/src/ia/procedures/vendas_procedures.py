import pandas as pd
from ia import procedures
from paths import VENDAS_DIR

arquivos = sorted(VENDAS_DIR.glob("vendas_*.csv"))
tabela = pd.concat([pd.read_csv(a, sep=";", encoding="utf-8-sig") for a in arquivos], ignore_index=True)

def buscar_por_nome_produto(nome):
    skus = [p["SKU"] for p in procedures.produtos.buscar_por_nome(nome)]
    return tabela[tabela["SKU"].isin(skus)]

def buscar_por_periodo(periodo):
    return tabela[tabela["Período"].str.contains(periodo, case=False, na=False)]

def buscar_por_data(data):
    print(f"[DEBUG - vendas_procedures] Resultado: {tabela[tabela["Data"] == data]}")
    return tabela[tabela["Data"] == data]

def produtos_mais_vendidos(limite):
    if limite <= 0:
        return None
    top = tabela.groupby("SKU")["Qtd"].sum().sort_values(ascending=False).head(limite)
    top.index = top.index.map(procedures.produtos.obter_dicionario_sku_nome())   # nome só na saída
    top.index.name = "Produto"
    return top

def todas_as_vendas():
    return tabela