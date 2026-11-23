import calendar
from datetime import datetime, date, timedelta
from functools import lru_cache
from ia import procedures
from ia import utils

FERIADOS_FIXOS = {
    '01-01', '21-04', '01-05', '09-07', '07-09', '12-10',
    '02-11', '15-11', '20-11', '25-12', '19-03', '27-07'
}
FERIADOS_MOVEIS = {
    '04-03-2025', '18-04-2025', '19-06-2025',
    '17-02-2026', '03-04-2026', '04-06-2026',
    '09-02-2027', '26-03-2027', '27-05-2027',
}

def eh_feriado_sjc(dt: datetime | date) -> bool:
    return dt.strftime('%d-%m') in FERIADOS_FIXOS or dt.strftime('%d-%m-%Y') in FERIADOS_MOVEIS

@lru_cache(maxsize=None)
def datas_pagamento_clt(ano: int, mes: int) -> tuple[int, int]:
    dias_no_mes = calendar.monthrange(ano, mes)[1]
    dia_salario = 5
    dias_uteis = 0
    for d in range(1, dias_no_mes + 1):
        atual = date(ano, mes, d)
        if atual.weekday() != 6 and not eh_feriado_sjc(atual):
            dias_uteis += 1
        if dias_uteis == 5:
            dia_salario = d
            break

    dia_vale = 20
    while dia_vale > 1:
        atual = date(ano, mes, dia_vale)
        if atual.weekday() != 6 and not eh_feriado_sjc(atual):
            break
        dia_vale -= 1

    return dia_salario, dia_vale

def obter_fase_financeira(dt: datetime | date) -> str:
    dia_salario, dia_vale = datas_pagamento_clt(dt.year, dt.month)
    dia = dt.day
    if dia_salario <= dia <= (dia_salario + 4):
        return "Pagamento"
    elif dia_vale <= dia <= (dia_vale + 3):
        return "Vale"
    elif dia >= 26:
        return "Fim de Mês"
    return "Normal"

@lru_cache(maxsize=64)
def perfil_do_dia(data_str: str, clima_previsto: str | None = None) -> dict:
    """
    Retorna o contexto completo de um dia (passado via regras_*.csv ou hoje/futuro via Open-Meteo).
    """
    dt = datetime.strptime(data_str, "%d/%m/%Y")
    regra_csv = procedures.regras.obter_dia(data_str)

    if regra_csv is not None:
        feriado = bool(regra_csv["feriado"])
        vespera = bool(regra_csv["vespera_de_feriado"])
        clima = str(regra_csv["clima"]).capitalize()
    else:
        feriado = eh_feriado_sjc(dt)
        vespera = eh_feriado_sjc(dt + timedelta(days=1))
        clima = (
            clima_previsto.capitalize()
            if clima_previsto
            else utils.obter_clima_para_previsao(data_str)
        )

    dia_semana = dt.weekday()
    if feriado:
        dow_efetivo = 6
    elif vespera and dia_semana < 5:
        dow_efetivo = 5
    else:
        dow_efetivo = dia_semana

    clima_grupo = clima if clima in {"Chuvoso", "Frio", "Calor"} else "Neutro"
    fase_fin = obter_fase_financeira(dt)

    return {
        "data": data_str,
        "dia_semana_real": dia_semana,
        "dow_efetivo": dow_efetivo,
        "eh_feriado": feriado,
        "eh_vespera": vespera,
        "eh_chuva": clima == "Chuvoso",
        "clima": clima,
        "clima_grupo": clima_grupo,
        "fase_financeira": fase_fin,
    }