from ia import procedures 
from paths import DADOS_DIR
import pandas as pd
estoque = DADOS_DIR / "ingredientes.csv"
receita = DADOS_DIR / "receitas.csv"


estoque_tb = pd.read_csv(estoque, sep=';', encoding='utf-8-sig')
receita_tb = pd.read_csv(receita, sep=';', encoding='utf-8-sig')

def buscar_receita_por_sku(sku: int):
    """Retorna a receita de um produto (SKU) como uma lista de dicionários."""
    resultado = receita_tb[receita_tb['SKU'] == sku]
    return resultado.to_dict(orient='records')

def consultar_estoque_por_ingrediente(ingrediente: str, setor: str = None):
    """Retorna a quantidade em estoque de um ingrediente específico, em determinado setor."""
    if setor:
        resultado = estoque_tb[(estoque_tb['Ingrediente'].str.contains(f'^{ingrediente}$', case=False, na=False)) & (estoque_tb['Setor'] == setor)]
    else:
        resultado = estoque_tb[estoque_tb['Ingrediente'].str.contains(f'^{ingrediente}$', case=False, na=False)]
    return resultado.to_dict(orient='records')

def formatacao_pre_calculo (sku : list = [] ):
    """Ela unifica os dados da receita e do estoque, e retorna uma lista de dicionários com os ingredientes, suas quantidades na receita e no estoque.
    ira devolver, para cada sku, uma lista de dicionarios com os ingredientes, suas quantidades na receita e no estoque."""
    resultado = []
    for s in sku:
        receita_sku = buscar_receita_por_sku(s)
        for item in receita_sku:
            ingrediente = item['Ingrediente']
            quantidade_receita = item['Qtd']
            estoque_ingrediente = consultar_estoque_por_ingrediente(ingrediente, procedures.produtos.setor_do_sku(s))
            quantidade_estoque = estoque_ingrediente[0]['Estoque Atual'] if estoque_ingrediente else 0
            resultado.append({
                'SKU': s,
                'Ingrediente': ingrediente,
                'Quantidade na Receita': quantidade_receita,
                'Quantidade em Estoque': quantidade_estoque
            })
    return resultado