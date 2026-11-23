import requests
from datetime import datetime
from functools import lru_cache
from ia import procedures

# Cacheia por (data_str, hora_atual) para não fazer várias requisições na mesma hora
@lru_cache(maxsize=32)
def _consultar_open_meteo(data_iso: str, hora_cache: int) -> str:
    """
    Consulta a previsão do tempo para São José dos Campos usando a Open-Meteo.
    Usa os mesmos critérios exatos do gerador_erp.py:
      - precipitação > 5.0 mm -> 'Chuvoso'
      - temp_max > 30.0 °C    -> 'Calor'
      - temp_max <= 20.0 °C   -> 'Frio'
      - caso contrário        -> 'Neutro' (Ensolarado/Nublado têm fator 1.0)
    """
    lat, lon = -23.1791, -45.8872
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,precipitation_sum"
        f"&timezone=America%2FSao_Paulo"
        f"&start_date={data_iso}&end_date={data_iso}"
    )
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            daily = resp.json().get("daily", {})
            t_max = daily.get("temperature_2m_max", [None])[0]
            precip = daily.get("precipitation_sum", [None])[0]

            if t_max is not None and precip is not None:
                if precip > 5.0:
                    return "Chuvoso"
                if t_max > 30.0:
                    return "Calor"
                if t_max <= 20.0:
                    return "Frio"
                return "Neutro"
    except requests.RequestException:
        pass

    return "Neutro"


def obter_clima_para_previsao(data_str: str) -> str:
    """
    Recebe data no formato 'DD/MM/AAAA'.
    1. Se a data já existe nos CSVs (regras_*.csv), lê direto do disco (0ms).
    2. Se for hoje ou futuro próximo (até 14 dias), consulta a Open-Meteo.
    3. Se estiver fora do alcance ou sem internet, retorna 'Neutro'.
    """
    # Tenta primeiro no histórico local (CSV)
    regra_csv = procedures.regras.obter_dia(data_str)
    if regra_csv is not None:
        return str(regra_csv["clima"]).capitalize()

    # Se não está no CSV, verifica se está na janela de previsão (hoje até +14 dias)
    dt_alvo = datetime.strptime(data_str, "%d/%m/%Y").date()
    hoje = datetime.now().date()
    dias_a_frente = (dt_alvo - hoje).days

    if 0 <= dias_a_frente <= 14:
        hora_atual = datetime.now().hour
        return _consultar_open_meteo(dt_alvo.strftime("%Y-%m-%d"), hora_atual)

    return "Neutro"