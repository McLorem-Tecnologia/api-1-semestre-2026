import re
from datetime import datetime, timedelta
import unicodedata

def converter_data_relativa(data_alvo: str = None) -> str:
    """
    Intercepta palavras relativas, dias da semana (passados/futuros), datas ISO
    e datas por extenso em português, convertendo tudo para DD/MM/AAAA.
    Se não especificado, assume a data de hoje.
    """
    hoje = datetime.now()

    # Se não especificado ou vazio, assume 'hoje' automaticamente
    if not data_alvo or str(data_alvo).strip().lower() in ['', 'none', 'null', 'nil', 'não especificado', 'nao especificado']:
        return hoje.strftime("%d/%m/%Y")
        
    texto = str(data_alvo).strip().lower()
    
    # 1. Termos fixos (Ordenados dos mais compostos para os mais simples)
    # Usa regex com \b para funcionar mesmo se vier "para amanhã" ou "foi antes de ontem"
    termos_fixos = [
        (r'\bdepois\s+de\s+amanh[ãa]\b', 2),
        (r'\bantes\s+de\s+ontem\b', -2),
        (r'\banteontem\b', -2),
        (r'\bamanh[ãa]\b', 1),
        (r'\bontem\b', -1),
        (r'\b(?:hoje|hj)\b', 0),
        (r'\bsemana\s+passada\b', -7),
        (r'\b(?:pr[óo]xima\s+semana|semana\s+que\s+vem)\b', 7),
    ]
    for padrao, delta_dias in termos_fixos:
        if re.search(padrao, texto):
            return (hoje + timedelta(days=delta_dias)).strftime("%d/%m/%Y")
        
    # 2. Busca por padrões matemáticos de dias (Ex: "3 dias atrás", "há 1 dia", "daqui a 5 dias")
    nums_extenso = {
        'um': 1, 'uma': 1, 'dois': 2, 'duas': 2, 'três': 3, 'tres': 3,
        'quatro': 4, 'cinco': 5, 'seis': 6, 'sete': 7, 'oito': 8,
        'nove': 9, 'dez': 10, 'quinze': 15, 'trinta': 30
    }
    # Substitui números escritos por extenso (muito comum vindo do Whisper) por dígitos
    for palavra, digito in nums_extenso.items():
        texto = re.sub(rf'\b{palavra}\b', str(digito), texto)

    match_passado_atras = re.search(r'(\d+)\s*dias?\s*atr[áa]s', texto)
    match_passado_ha = re.search(r'h[áa]\s*(\d+)\s*dias?', texto)
    match_futuro = re.search(r'(?:daqui\s+a|daqui|em)\s*(\d+)\s*dias?', texto)
    
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
    except ValueError:
        pass

    # 3. Dias da semana relativos (ex: "segunda feira passada", "próxima sexta", "terça retrasada")
    dias_semana = {
        'segunda': 0, 'terça': 1, 'terca': 1, 'quarta': 2,
        'quinta': 3, 'sexta': 4, 'sábado': 5, 'sabado': 5, 'domingo': 6
    }
    
    padrao_semana = (
        r'\b(?:(?:na|no)\s+)?'
        r'(?:(pr[óo]xim[ao]|últim[ao]|ultim[ao]|ness[ae]|nest[ae]|ess[ae]|est[ae])\s+)?'
        r'(segunda|ter[çc]a|quarta|quinta|sexta|s[áa]bado|domingo)(?:[-\s]*feira)?'
        r'(?:\s+(passad[ao]|anterior|retrasad[ao]|que\s+vem|pr[óo]xim[ao]))?\b'
    )
    match_semana = re.search(padrao_semana, texto)
    if match_semana:
        prefixo, dia_str, sufixo = match_semana.groups()
        dia_alvo = dias_semana[dia_str]
        dia_atual = hoje.weekday()
        
        eh_futuro = (
            (prefixo and re.match(r'pr[óo]xim[ao]', prefixo)) or
            (sufixo and re.match(r'que\s+vem|pr[óo]xim[ao]', sufixo))
        )
        eh_retrasado = sufixo and re.match(r'retrasad[ao]', sufixo)
        
        if eh_futuro:
            dias_diff = (dia_alvo - dia_atual) % 7
            if dias_diff == 0:
                dias_diff = 7
            return (hoje + timedelta(days=dias_diff)).strftime("%d/%m/%Y")
        else:
            dias_diff = (dia_atual - dia_alvo) % 7
            if dias_diff == 0:
                dias_diff = 7
            if eh_retrasado:
                dias_diff += 7
            return (hoje - timedelta(days=dias_diff)).strftime("%d/%m/%Y")

    # 4. Formato ISO (AAAA-MM-DD ou AAAA/MM/DD)
    match_iso = re.search(r'\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b', texto)
    if match_iso:
        ano, mes, dia = map(int, match_iso.groups())
        try:
            return datetime(ano, mes, dia).strftime("%d/%m/%Y")
        except ValueError:
            pass

    # 5. Formato BR despadronizado (ex: "2/11/2026" ou "02-11-26" -> "02/11/2026")
    match_br = re.search(r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b', texto)
    if match_br:
        dia, mes, ano = map(int, match_br.groups())
        if ano < 100:
            ano += 2000
        try:
            return datetime(ano, mes, dia).strftime("%d/%m/%Y")
        except ValueError:
            pass

    # 6. Datas por extenso em português (ex: "2 de novembro de 2026", "02 de nov")
    meses_map = {
        'janeiro': 1, 'jan': 1, 'fevereiro': 2, 'fev': 2,
        'março': 3, 'marco': 3, 'mar': 3, 'abril': 4, 'abr': 4,
        'maio': 5, 'mai': 5, 'junho': 6, 'jun': 6,
        'julho': 7, 'jul': 7, 'agosto': 8, 'ago': 8,
        'setembro': 9, 'set': 9, 'outubro': 10, 'out': 10,
        'novembro': 11, 'nov': 11, 'dezembro': 12, 'dez': 12
    }
    
    match_extenso = re.search(
        r'\b(\d{1,2})\s*(?:de\s+|/|-)?([a-zç]+)(?:\s*(?:de\s+|/|-)?(\d{2,4}))?\b',
        texto
    )
    if match_extenso:
        dia_str, mes_str, ano_str = match_extenso.groups()
        if mes_str in meses_map:
            dia = int(dia_str)
            mes = meses_map[mes_str]
            ano = int(ano_str) if ano_str else hoje.year
            if ano < 100:
                ano += 2000
            try:
                return datetime(ano, mes, dia).strftime("%d/%m/%Y")
            except ValueError:
                pass

    return data_alvo

def converter_periodo(periodo: str = None) -> list:
    """
    Converte o período dito pelo usuário em uma lista de períodos oficiais:
    "Manhã", "Tarde" e/ou "Noite".

    - Aceita variações com ou sem acento e frases soltas: "de manha", "a tarde",
      "à noite", "pela manhã", "manhã e tarde".
    - Se não for especificado, ou se for "dia todo", "todos os períodos" etc.,
      retorna os três períodos.
    """
    todos = ["Manhã", "Tarde", "Noite"]

    if not periodo or str(periodo).strip().lower() in ['', 'none', 'null', 'nil']:
        return todos

    texto = unicodedata.normalize("NFD", str(periodo).lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")

    if re.search(r'\b(todos|todo|inteiro|completo|geral|o\s+dia|dia\s+todo)\b', texto):
        return todos

    padroes = [
        ("Manhã", r'\b(manha|cedo|matutino)\b'),
        ("Tarde", r'\b(tarde|vespertino)\b'),
        ("Noite", r'\b(noite|noturno|madrugada)\b'),
    ]
    encontrados = [nome for nome, padrao in padroes if re.search(padrao, texto)]

    # Se não reconheceu nada, é mais seguro devolver o dia dividido por período
    return encontrados or todos