from ia import utils
from datetime import datetime, timedelta
from functools import lru_cache

def eh_pagamento(d):
        # 1. Regra do dia 20 (antecipa se for fim de semana)
        dia_20 = d.replace(day=20)
        if dia_20.weekday() == 6: dia_20 = dia_20.replace(day=19) 
        if d.date() == dia_20.date(): return True
            
        # 2. Regra do 5º dia útil
        dias_uteis = 0
        for i in range(1, 32):
            try:
                data_teste = d.replace(day=i)
                # Sábado é dia útil (<= 5), mas se for Feriado, não conta!
                if data_teste.weekday() <= 5 and not utils.eh_feriado(data_teste):
                    dias_uteis += 1
                if dias_uteis == 5:
                    return d.date() == data_teste.date()
            except ValueError:
                break # Sai do loop se o dia não existir no mês (ex: 31 de fev)
        return False
    
def dias_ate_pagamento(valor: str) -> int:
    data_alvo = datetime.strptime(valor, "%d/%m/%Y")
    
    for i in range(20):
        if eh_pagamento(data_alvo + timedelta(days=i)): return -i # Futuro (negativo)
        if eh_pagamento(data_alvo - timedelta(days=i)): return i  # Passado (positivo)
    return -999

@lru_cache(maxsize=None)
def classificar_dia(data: str) -> int:
    """
    Classifica se o dia é bom (1) ou ruim (0).
    Condições para dia bom: dia de pagamento, sexta a domingo, ou feriado.
    """
    dt = datetime.strptime(data, "%d/%m/%Y")
    
    # se é dia de pagamento
    if dias_ate_pagamento(data) == 0: return 1
        
    # se é sexta (4), sábado (5) ou domingo (6)
    if dt.weekday() in [4, 5, 6]: return 1
        
    # se é feriado chamando nossa função própria
    if utils.eh_feriado(dt): return 1
        
    # Se nenhuma das condições acima for satisfeita, o dia é ruim
    return 0