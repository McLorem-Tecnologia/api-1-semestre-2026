import holidays
from datetime import datetime, timedelta

TOOLS_DISPONIVEIS = []

def dspy_tool(func):
    """Decorador: adiciona a função à lista de ferramentas do DSPy."""
    TOOLS_DISPONIVEIS.append(func)
    return func

def dias_ate_pagamento(valor: str) -> int:
    data_alvo = datetime.strptime(valor, "%d/%m/%Y")

    feriados_br = holidays.country_holidays('BR', subdiv='SP', years=[data_alvo.year - 1, data_alvo.year, data_alvo.year + 1])
    
    def sim_pagamento(d):
        # 1. Regra do dia 20 (antecipa se for fim de semana)
        dia_20 = d.replace(day=20)
        if dia_20.weekday() == 5: dia_20 = dia_20.replace(day=19) # Sábado
        if dia_20.weekday() == 6: dia_20 = dia_20.replace(day=18) # Domingo
        if d.date() == dia_20.date(): 
            return True
            
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
        if sim_pagamento(data_alvo + timedelta(days=i)):
            return -i # Futuro (negativo)
        if sim_pagamento(data_alvo - timedelta(days=i)):
            return i  # Passado (positivo)

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