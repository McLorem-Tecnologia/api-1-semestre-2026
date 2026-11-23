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

def buscar_ingredientes(sku):
    dados = pd.read_csv(receita, sep=";", encoding="utf-8-sig")
    resultado = dados[dados["SKU"] == int(sku)]
    return resultado

def consultar_estoque_por_ingrediente(ingrediente: str, setor: str = None):
    """Retorna a quantidade em estoque de um ingrediente específico, em determinado setor."""
    alvo = str(ingrediente).strip().lower()
    filtro_ingrediente = estoque_tb['Ingrediente'].astype(str).str.strip().str.lower() == alvo

    if setor:
        filtro_setor = estoque_tb['Setor'].astype(str).str.strip() == str(setor).strip()
        resultado = estoque_tb[filtro_ingrediente & filtro_setor]
    else:
        resultado = estoque_tb[filtro_ingrediente]

    return resultado.to_dict(orient='records')


def formatacao_pre_calculo(sku: list = []):
    """Unifica os dados da receita e do estoque, retornando uma lista de dicionários
    com os ingredientes, suas quantidades na receita, unidade e estoque."""
    resultado = []
    for s in sku:
        receita_sku = buscar_receita_por_sku(s)
        for item in receita_sku:
            ingrediente = item['Ingrediente']
            quantidade_receita = item['Qtd']
            unidade = item.get('Unidade', 'un')
            estoque_ingrediente = consultar_estoque_por_ingrediente(
                ingrediente, procedures.produtos.setor_do_sku(s)
            )
            quantidade_estoque = estoque_ingrediente[0]['Estoque Atual'] if estoque_ingrediente else 0
            resultado.append({
                'SKU': s,
                'Ingrediente': ingrediente,
                'Unidade': unidade,
                'Quantidade na Receita': quantidade_receita,
                'Quantidade em Estoque': quantidade_estoque,
            })
    return resultado