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
    match_passado_atras = re.search(r'(\d+)\s*dias?\s*atr[áa]s', texto)
    match_passado_ha = re.search(r'h[áa]\s*(\d+)\s*dias?', texto)
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
