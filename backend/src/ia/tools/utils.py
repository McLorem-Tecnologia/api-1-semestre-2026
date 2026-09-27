from datetime import datetime, timedelta
import difflib
import holidays

TOOLS_DISPONIVEIS = []

def dspy_tool(func):
    """Decorador: adiciona a função à lista de ferramentas do DSPy."""
    TOOLS_DISPONIVEIS.append(func)
    return func

import re
from datetime import datetime, timedelta

def converter_data_relativa(data_alvo: str) -> str:
    """
    Intercepta palavras relativas e converte para a data real do sistema (DD/MM/AAAA).
    Aceita "hoje", "amanhã", "ontem", "anteontem", "3 dias atrás", "daqui a 5 dias", etc.
    """
    if not data_alvo:
        return ""
        
    texto = data_alvo.strip().lower()
    hoje = datetime.now() 
    
    # 1. Mapeamento direto (Termos fixos)
    if texto in ['hoje', 'hj']:
        return hoje.strftime("%d/%m/%Y")
    elif texto in ['amanhã', 'amanha']:
        return (hoje + timedelta(days=1)).strftime("%d/%m/%Y")
    elif texto in ['ontem']:
        return (hoje - timedelta(days=1)).strftime("%d/%m/%Y")
    elif texto in ['anteontem']:
        return (hoje - timedelta(days=2)).strftime("%d/%m/%Y")
        
    # 2. Busca por padrões matemáticos de dias (Regex)
    # Ex: "3 dias atrás", "ha 2 dias", "há 5 dias" (Passado)
    match_passado_atras = re.search(r'(\d+)\s*dias?\s*atr[áa]s', texto)
    match_passado_ha = re.search(r'h[áa]\s*(\d+)\s*dias?', texto)
    
    # Ex: "daqui a 3 dias", "daqui 2 dias", "em 4 dias" (Futuro)
    match_futuro = re.search(r'(?:daqui a|daqui|em)\s*(\d+)\s*dias?', texto)
    
    try:
        if match_passado_atras:
            dias = int(match_passado_atras.group(1))
            return (hoje - timedelta(days=dias)).strftime("%d/%m/%Y")
            
        if match_passado_ha:
            dias = int(match_passado_ha.group(1))
            return (hoje - timedelta(days=dias)).strftime("%d/%m/%Y")
            
        if match_futuro:
            dias = int(match_futuro.group(1))
            return (hoje + timedelta(days=dias)).strftime("%d/%m/%Y")
            
    except ValueError: pass

    return data_alvo

def normalizar_setor(setor_informado: str) -> str:
    """
    Corrige erros de digitação e mapeia apelidos para o nome oficial do setor no banco de dados.
    """
    if not setor_informado or setor_informado.lower() in ['none', 'null', 'vazio']:
        return None
        
    setores_oficiais = ["Açougue", "Padaria", "Cozinha/Rotisseria", "Peixaria", "Confeitaria"]
    texto_limpo = setor_informado.strip().lower()
    
    alias_map = {
        "cozinha": "Cozinha/Rotisseria",
        "rotisseria": "Cozinha/Rotisseria",
        "roti": "Cozinha/Rotisseria",
        "acougue": "Açougue",
        "carne": "Açougue",
        "peixe": "Peixaria",
        "doce": "Confeitaria"
    }
    
    for apelido, oficial in alias_map.items():
        if apelido in texto_limpo:
            return oficial
            
    matches = difflib.get_close_matches(setor_informado.title(), setores_oficiais, n=1, cutoff=0.6)
    
    if matches:
        return matches[0]
        
    return setor_informado.capitalize()

def dias_ate_pagamento(valor: str) -> int:
    data_alvo = datetime.strptime(valor, "%d/%m/%Y")

    feriados_br = holidays.country_holidays('BR', subdiv='SP', years=[data_alvo.year - 1, data_alvo.year, data_alvo.year + 1])
    
    def sim_pagamento(d):
        # 1. Regra do dia 20 (antecipa se for fim de semana)
        dia_20 = d.replace(day=20)
        if dia_20.weekday() == 5: dia_20 = dia_20.replace(day=19) # Sábado
        if dia_20.weekday() == 6: dia_20 = dia_20.replace(day=18) # Domingo
        if d.date() == dia_20.date(): return True
            
        # 2. Regra do 5º dia útil
        dias_uteis = 0
        for i in range(1, 32):
            try:
                data_teste = d.replace(day=i)
                # Sábado é dia útil (<= 5), mas se for Feriado, não conta!
                if data_teste.weekday() <= 5 and data_teste.date() not in feriados_br:
                    dias_uteis += 1
                if dias_uteis == 5:
                    return d.date() == data_teste.date()
            except ValueError:
                break # Sai do loop se o dia não existir no mês (ex: 31 de fev)
        return False

    # Expande a busca dia a dia a partir da data alvo
    for i in range(20):
        if sim_pagamento(data_alvo + timedelta(days=i)): return -i # Futuro (negativo)
        if sim_pagamento(data_alvo - timedelta(days=i)): return i  # Passado (positivo)
    return -999

def classificar_dia(data: str) -> int:
    """
    Classifica se o dia é bom (1) ou ruim (0).
    Condições para dia bom: dia de pagamento, sexta a domingo, ou feriado.
    """
    # 1. Verifica se é dia de pagamento
    if dias_ate_pagamento(data) == 0:
        return 1
        
    dt = datetime.strptime(data, "%d/%m/%Y")
    
    # 2. Verifica se é sexta (4), sábado (5) ou domingo (6)
    if dt.weekday() in [4, 5, 6]:
        return 1
        
    # 3. Verifica se é feriado no Brasil usando a biblioteca holidays
    # Passamos o ano da data para ele gerar o calendário correto daquele ano
    feriados_br = holidays.country_holidays('BR', subdiv='SP', years=dt.year)
    
    if dt.date() in feriados_br:
        return 1
        
    # Se nenhuma das condições acima for satisfeita, o dia é ruim
    return 0

# --- REGISTRO DE ARQUIVOS DE FERRAMENTAS ---
# O Python precisa ler esses arquivos uma única vez para ativar os decoradores.
# Sempre que criar um arquivo novo (ex: vendas.py), adicione um import genérico aqui:

import ia.tools.produtos_tools
import ia.tools.producao_tool
# import ia.tools.vendas_tools
# import ia.tools.descartes_tools