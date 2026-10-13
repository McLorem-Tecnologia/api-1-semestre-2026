from paths import DADOS_DIR
import re
import pandas as pd

path = DADOS_DIR / "produtos.csv"
prod_tb = pd.read_csv(path, sep=';', encoding='utf-8-sig')

def obter_dicionario_sku_nome() -> dict:
    """{2001: 'Frango assado (Un)', 1001: 'Pão Francês (Kg)', ...}"""
    return dict(zip(prod_tb['SKU'], prod_tb['Produto']))

def nome_do_sku(sku: int) -> str:
    """Nome do produto para um SKU (se o SKU não existir, devolve 'SKU 9999' em vez de dar erro)."""
    return obter_dicionario_sku_nome().get(sku, f"SKU {sku}")

def skus_por_nome(nome_produto: str) -> list:
    """Lista de SKUs cujo nome contém o texto (ex.: 'frango' -> [2001, 4003])."""
    return [p['SKU'] for p in buscar_por_nome(nome_produto)]

def skus_por_setor(setor: str) -> list:
    """Lista de SKUs de um setor (ex.: 'Cozinha' -> [2001, 2002, ...])."""
    return [p['SKU'] for p in buscar_por_setor(setor)]

def listar():
    produtos = prod_tb['Produto'].unique().tolist()
    return produtos

def listar_detalhado() -> str:
    return prod_tb.to_string(index=False)

def buscar_por_nome(nome_produto: str):
    resultado = prod_tb[prod_tb['Produto'].str.contains(nome_produto, case=False, na=False)]
    return resultado.to_dict(orient='records')

def buscar_por_setor(setor: str):
    resultado = prod_tb[prod_tb['Setor'].str.contains(setor, case=False, na=False, regex=False)]
    if resultado.empty:
        for parte in [p.strip() for p in re.split(r"[/()]", setor) if p.strip()]:
            resultado = prod_tb[prod_tb['Setor'].str.contains(parte, case=False, na=False, regex=False)]
            if not resultado.empty:
                break
    return resultado.to_dict(orient='records')

def buscar_por_tempo(tempo: str):
    resultado = prod_tb[prod_tb['Tempo de preparo'].str.contains(tempo, case=False, na=False)]
    return resultado.to_dict(orient='records')