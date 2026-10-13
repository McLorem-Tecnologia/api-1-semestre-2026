from datetime import date, timedelta, datetime
from functools import lru_cache

# Feriados Nacionais + Estaduais de SP + Municipais
FERIADOS_FIXOS = {
    '01-01', '21-04', '01-05', '09-07', '07-09', '12-10', '02-11', '15-11',
    '20-11', '25-12', '19-03', '27-07'   # 20-11: nacional desde 2024
}

@lru_cache(maxsize=None)
def pascoa(ano: int) -> date:
    """Domingo de Páscoa (Meeus/Jones/Butcher) - vale para qualquer ano."""
    a, b, c = ano % 19, ano // 100, ano % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(ano, mes, dia)

@lru_cache(maxsize=None)
def feriados_moveis(ano: int) -> frozenset:
    """Carnaval (terça), Sexta-Feira Santa e Corpus Christi, calculados a partir da Páscoa."""
    p = pascoa(ano)
    return frozenset({p - timedelta(days=47), p - timedelta(days=2), p + timedelta(days=60)})

def eh_feriado(data) -> bool:
    """Verifica se a data fornecida é um feriado fixo ou móvel."""
    d = data.date() if isinstance(data, datetime) else data
    
    if d.strftime('%d-%m') in FERIADOS_FIXOS:
        return not (d.strftime('%d-%m') == '20-11' and d.year < 2024)
        
    return d in feriados_moveis(d.year)