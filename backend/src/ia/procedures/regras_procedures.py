from pathlib import Path
import pandas as pd
 
path1 = Path(__file__).resolve().parents[3] / "dados" / "regras_agosto_2026.csv"
path2 = Path(__file__).resolve().parents[3] / "dados" / "regras_setembro_2026.csv"
 
 
def carregar_arquivo(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho, sep=";", encoding="utf-8")
    data = pd.to_datetime(df["Dia"], format="%d/%m/%Y")
 
    return pd.DataFrame(
        {
            "data": data,
            "ano": data.dt.year,
            "mes": data.dt.month,
            "dia": data.dt.day,
            "semana": data.dt.isocalendar().week.astype(int),
            "clima": df["Clima"].str.capitalize(),
            "vespera_de_feriado": df["Véspera de Feriado"].str.casefold().eq("sim"),
            "feriado": df["Feriado"].str.casefold().eq("sim"),
            "vespera_de_fim_de_semana": df["Véspera de Fim de Semana"].str.casefold().eq("sim"),
            "fim_de_semana": df["Fim de Semana"].str.casefold().eq("sim"),
        }
    )
 
 
def carregar_dados(caminhos=(path1, path2)) -> pd.DataFrame:
    df = pd.concat((carregar_arquivo(c) for c in caminhos), ignore_index=True)
    df["dia_util"] = ~df["fim_de_semana"] & ~df["feriado"]
    return df.sort_values("data").reset_index(drop=True)
 
 
def obter_dia(data, dados: pd.DataFrame | None = None) -> pd.Series | None:
    df = dados if dados is not None else carregar_dados()
    alvo = pd.to_datetime(data, format="%d/%m/%Y") if isinstance(data, str) else pd.to_datetime(data)
    linhas = df[df["data"] == alvo]
    return linhas.iloc[0] if not linhas.empty else None
 
 
def obter_ano(ano: int, dados: pd.DataFrame | None = None) -> pd.DataFrame:
    df = dados if dados is not None else carregar_dados()
    return df[df["ano"] == ano]
 
 
def obter_mes(ano: int, mes: int, dados: pd.DataFrame | None = None) -> pd.DataFrame:
    df = dados if dados is not None else carregar_dados()
    return df[(df["ano"] == ano) & (df["mes"] == mes)]
 
 
def obter_semana(ano: int, semana: int, dados: pd.DataFrame | None = None) -> pd.DataFrame:
    df = dados if dados is not None else carregar_dados()
    return df[(df["ano"] == ano) & (df["semana"] == semana)]
 
 
def filtrar(
    dados: pd.DataFrame | None = None,
    *,
    ano: int | None = None,
    mes: int | None = None,
    dia: int | None = None,
    semana: int | None = None,
    clima: str | None = None,
    feriado: bool | None = None,
    vespera_de_feriado: bool | None = None,
    fim_de_semana: bool | None = None,
    vespera_de_fim_de_semana: bool | None = None,
    dia_util: bool | None = None,
) -> pd.DataFrame:
    df = dados if dados is not None else carregar_dados()
    criterios = {
        "ano": ano,
        "mes": mes,
        "dia": dia,
        "semana": semana,
        "feriado": feriado,
        "vespera_de_feriado": vespera_de_feriado,
        "fim_de_semana": fim_de_semana,
        "vespera_de_fim_de_semana": vespera_de_fim_de_semana,
        "dia_util": dia_util,
    }
    for coluna, valor in criterios.items():
        if valor is not None:
            df = df[df[coluna] == valor]
    if clima is not None:
        df = df[df["clima"].str.casefold() == clima.casefold()]
    return df
 
 
if __name__ == "__main__":
    dados = carregar_dados()
    print(dados.head())
    print()
    print(obter_dia("07/09/2026", dados))
    print()
    print(obter_ano(2026, dados).shape)
    print(obter_mes(2026, 9, dados).shape)
    print(obter_semana(2026, obter_dia("07/09/2026", dados)["semana"], dados))