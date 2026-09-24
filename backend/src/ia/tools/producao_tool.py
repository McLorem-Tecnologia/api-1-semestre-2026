# Funções para estimativa de produção.
# Função para TOOLS do DSPY relacionadas a produção.
import math
import sys
from pathlib import Path
import pandas as pd
from ia.procedures import procedures
from ia.tools.utils import dspy_tool
import traceback

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ia.procedures import procedures


def media_vendas_produtos(vendas, setor=None):
    """
    Calcula a média de vendas de cada produto e arredonda o resultado
    para cima.

    Args:
        vendas (list): Lista de vendas no formato de registros
            de um DataFrame do pandas.
        setor (str, opcional): Setor utilizado para filtrar os produtos.
            Se não for informado, calcula a média de todos os produtos.

    Returns:
        list: Lista contendo o nome de cada produto e sua média
            de vendas arredondada para cima.

            Exemplo:
            ['Brigadeiro: 4', 'Temaki: 7', 'Pão Francês: 4']
    """

    dados = pd.DataFrame(vendas)

    if setor is not None:
        produtos_setor = procedures.produtos.buscar_por_setor(setor)

        nomes_produtos = [
            produto["Produto"]
            for produto in produtos_setor
        ]

        dados = dados[
            dados["Produto"].isin(nomes_produtos)
        ]

    medias = dados.groupby("Produto")["Qtd"].mean()

    resultado = []

    for produto, media in medias.items():
        media_arredondada = math.ceil(media)

        resultado.append(
            f"{produto}: {media_arredondada}"
        )

    return resultado


@dspy_tool
def producao_dia_pelo_setor(data: str, setor: str) -> str:
    """Calcula a produção total de um setor em uma data específica.
    A produção é a soma das vendas com o descarte.
    REGRA ABSOLUTA: Retorne a lista EXATAMENTE no formato que esta ferramenta gerar. Se ocorrer um erro, mostre o erro técnico exato ao usuário.
    """
    try:
        print(f"[DEBUG] Iniciando producao_dia -> Data: {data} | Setor: {setor}")
        
        # 1. Buscar produtos do setor
        produtos_setor = procedures.produtos.buscar_por_setor(setor)
        if not produtos_setor:
            return f"Nenhum produto encontrado para o setor '{setor}'."
        
        nomes_produtos = [p["Produto"] for p in produtos_setor]
        
        # 2. Busca os dados brutos das procedures
        dados_vendas = procedures.vendas.buscar_por_data(data)
        dados_descarte = procedures.descarte.buscar_por_data(data)
        
        # PROTEÇÃO 1: Se o retorno for um DataFrame do Pandas, converte para lista de dicionários
        if isinstance(dados_vendas, pd.DataFrame):
            dados_vendas = dados_vendas.to_dict('records')
        if isinstance(dados_descarte, pd.DataFrame):
            dados_descarte = dados_descarte.to_dict('records')
            
        resumo = {nome: {"vendas": 0, "descarte": 0} for nome in nomes_produtos}
        
        # Função interna para garantir que os valores lidos da planilha não quebram a soma
        def limpar_numero(valor):
            try:
                # Converte textos, trata possíveis vírgulas, e garante que sai como número inteiro
                return int(float(str(valor).replace(',', '.').strip()))
            except (ValueError, TypeError):
                return 0

        # 3. Soma as vendas de forma segura
        for item in dados_vendas:
            if isinstance(item, dict) and item.get("Produto") in nomes_produtos:
                qtd = item.get("Qtd", item.get("Quantidade", 0))
                resumo[item["Produto"]]["vendas"] += limpar_numero(qtd)
                
        # 4. Soma os descartes de forma segura
        for item in dados_descarte:
            if isinstance(item, dict) and item.get("Produto") in nomes_produtos:
                qtd = item.get("Qtd", item.get("Quantidade", item.get("Descarte", 0)))
                resumo[item["Produto"]]["descarte"] += limpar_numero(qtd)

        # 5. Monta o resultado final no formato exigido
        resultado = ""
        teve_movimento = False
        
        for produto in sorted(resumo.keys()):
            vendas = resumo[produto]["vendas"]
            descarte = resumo[produto]["descarte"]
            producao = vendas + descarte
            
            if producao > 0:
                teve_movimento = True
                resultado += f"{produto}, produção: {producao}, vendas: {vendas}, descarte: {descarte}\n"
                
        if not teve_movimento:
            return f"Não houve registros de produção para '{setor}' na data {data}."
            
        print("[DEBUG] Sucesso! Ferramenta gerou os dados corretamente.")
        return resultado

    except Exception as e:
        # Imprime o rasto completo do erro no terminal do VS Code
        print("\n--- DETALHE TÉCNICO DO ERRO ---")
        print(traceback.format_exc())
        print("-------------------------------\n")
        
        # Força o bot a apresentar a causa raiz diretamente no chat
        return f"POR FAVOR, AVISE O DESENVOLVEDOR EXATAMENTE ISTO: Erro técnico no Python -> {type(e).__name__}: {str(e)}"