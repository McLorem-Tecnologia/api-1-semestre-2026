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

def nome_para_skus(nome: str) -> str:
    """Retorna o SKU para um nome de produto (se o nome não existir, devolve o próprio SKU = 0000)."""
    sku = next((k for k, v in obter_dicionario_sku_nome().items() if v == nome), None)
    return sku if sku is not None else '0000'

def setor_do_sku(sku: int) -> str:
    """Setor do produto para um SKU (se o SKU não existir, devolve 'SKU 9999' em vez de dar erro)."""
    resultado = prod_tb[prod_tb['SKU'] == sku]
    if not resultado.empty:
        return resultado.iloc[0]['Setor']
    else:
        return f"SKU {sku}"

def produtos_por_setor(setor: str = None) -> list:
    """
    1º Recebe o setor Y e retorna todos os produtos ligados a esse setor.
    O parâmetro setor é opcional (0º): se não for informado, retorna todos os produtos.
    Retorna uma lista de dicionários com os dados de cada produto
    (SKU, Produto, Setor, Preço, Tempo de preparo).
    """
    if not setor or str(setor).strip().lower() in ['none', 'null', 'vazio', '']:
        return prod_tb.to_dict(orient='records')
    return buscar_por_setor(setor)

def valores_por_produtos(produtos: list) -> list:
    """
    2º Recebe a lista de produtos do Setor Y e retorna uma lista com o valor (Preço) de cada produto.
    Cada item retornado é um dicionário: {'Produto': nome, 'Preço': valor}.
    """
    valores = []
    for p in produtos:
        nome = p.get('Produto') if isinstance(p, dict) else str(p)
        preco = p.get('Preço') if isinstance(p, dict) else None
        # Se o preço não veio no dicionário, busca na tabela pelo nome do produto
        if preco is None and nome:
            achado = prod_tb[prod_tb['Produto'] == nome]
            if not achado.empty:
                preco = achado.iloc[0]['Preço']
        valores.append({'Produto': nome, 'Preço': preco})
    return valores