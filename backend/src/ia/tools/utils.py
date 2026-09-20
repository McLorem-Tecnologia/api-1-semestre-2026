from datetime import datetime
import re
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression

from ia.procedures import csv_procedures as procedures

CAMINHO_PRODUTOS = Path(__file__).resolve().parents[3] / "dados" / "produtos_mercado.csv"
CAMINHO_REGRAS_AGOSTO = Path(__file__).resolve().parents[3] / "dados" / "regras_agosto_2026.csv"
CAMINHO_REGRAS_SETEMBRO = Path(__file__).resolve().parents[3] / "dados" / "regras_setembro_2026.csv"
CAMINHO_VENDAS_AGOSTO = Path(__file__).resolve().parents[3] / "dados" / "vendas_supermercado_agosto_2026.csv"
CAMINHO_VENDAS_SETEMBRO = Path(__file__).resolve().parents[3] / "dados" / "vendas_supermercado_setembro_2026.csv"


def _normalizar_setor(setor: str | None) -> str | None:
    if setor is None:
        return None
    valor = str(setor).strip().lower()
    if not valor:
        return None
    mapa = {
        "acougue": "Açougue",
        "padaria": "Padaria",
        "peixaria": "Peixaria",
        "cozinha": "Cozinha/Rotisseria",
        "rotisseria": "Cozinha/Rotisseria",
        "cozinha/rotisseria": "Cozinha/Rotisseria",
        "cozinha rotisseria": "Cozinha/Rotisseria",
        "confeitaria": "Confeitaria",
    }
    return mapa.get(valor, valor.title())


def _extrair_setor(texto_usuario: str) -> str | None:
    if not texto_usuario:
        return None
    texto = texto_usuario.lower()
    produtos_df = pd.read_csv(CAMINHO_PRODUTOS, sep=";")
    setores = sorted(set(produtos_df["Setor"].dropna().astype(str).tolist()), key=len, reverse=True)
    for setor in setores:
        nome = setor.lower()
        if nome in texto or re.sub(r"[^a-z]", "", nome) in re.sub(r"[^a-z]", "", texto):
            return _normalizar_setor(setor)
    for padrao in ["peixaria", "padaria", "acougue", "cozinha", "rotisseria", "confeitaria"]:
        if padrao in texto:
            return _normalizar_setor(padrao)
    return None


def _carregar_base_historica():
    vendas = pd.concat(
        [
            pd.read_csv(CAMINHO_VENDAS_AGOSTO, sep=";"),
            pd.read_csv(CAMINHO_VENDAS_SETEMBRO, sep=";"),
        ],
        ignore_index=True,
    )
    vendas["Data"] = pd.to_datetime(vendas["Data"], format="%d/%m/%Y")
    produtos_df = pd.read_csv(CAMINHO_PRODUTOS, sep=";")
    return vendas.merge(produtos_df[["Produto", "Setor"]], on="Produto", how="left"), produtos_df


def historico_producao_por_setor(setor: str = None, data_inicio: str = None, data_fim: str = None) -> str:
    """Retorna o histórico real já produzido por setor, baseado nas vendas registradas."""
    vendas, _ = _carregar_base_historica()
    setor_alvo = _normalizar_setor(setor)
    if setor_alvo:
        vendas = vendas[vendas["Setor"].astype(str).str.lower() == setor_alvo.lower()]

    if data_inicio:
        inicio = pd.to_datetime(data_inicio, format="%d/%m/%Y")
        vendas = vendas[vendas["Data"] >= inicio]
    if data_fim:
        fim = pd.to_datetime(data_fim, format="%d/%m/%Y")
        vendas = vendas[vendas["Data"] <= fim]

    if vendas.empty:
        setor_label = setor_alvo or "geral"
        return f"Não encontrei produção registrada para o setor {setor_label}."

    totais = vendas.groupby("Produto", as_index=False)["Qtd"].sum().sort_values("Qtd", ascending=False)
    linhas = [
        "Histórico de produção" + (f" - Setor: {setor_alvo}" if setor_alvo else "") + ", ordenado por quantidade total:",
        "-----------------------------------------",
    ]
    for _, linha in totais.iterrows():
        linhas.append(f"- {linha['Produto']}: {int(linha['Qtd'])} unidades produzidas")

    linhas.append(f"Total histórico: {int(totais['Qtd'].sum())} unidades")
    return "\n".join(linhas)


def historico_producao_geral(data_inicio: str = None, data_fim: str = None) -> str:
    return historico_producao_por_setor(setor=None, data_inicio=data_inicio, data_fim=data_fim)


def somar(a: float, b: float) -> str:
    """[TEST] Função para somar dois valores. Retorna apenas o número final. Não faz arredondamentos."""
    print("[DEBUG] Entrou na função 'somar'")
    return f"a soma de {a} + {b} é {a + b * 100}"


def subtrair(a: float, b: float) -> str:
    """[TEST] Função para subtrair dois valores. Retorna apenas o número final. Não faz arredondamentos."""
    print("[DEBUG] Entrou na função 'subtrair'")
    return f"a subtração de {a} - {b} é {a - b}"


def clima(cidade: str) -> str:
    """[TEST] Função para informar o clima de uma cidade. Retorna apenas a descrição do clima."""
    print("[DEBUG] Entrou na função 'clima'")
    return f"O clima em {cidade} é ensolarado com temperatura de 25°C."


def produtos() -> str:
    """[TEST] Função para listar produtos disponíveis. Retorna uma lista de produtos. Quero que o agente retorne em forma de lista para o telegram de forma recuada usando o caractere '•' no início de cada item."""
    tabela_produtos = pd.read_csv(CAMINHO_PRODUTOS, sep=";")
    produtos_disponiveis = tabela_produtos["Produto"].tolist()
    print("[DEBUG] Entrou na função 'produtos'")
    return f"Produtos disponíveis: \n{'\n'.join([f'    • {produto}' for produto in produtos_disponiveis])}."


def produto_por_nome(nome: str) -> str:
    """[TEST] Função para listar as informações de um produto pelo seu nome. Retorna uma lista de informações do produto. Quero que o agente retorne em forma de lista para o telegram de forma recuada usando o caractere '•' no início de cada item."""
    produto = procedures.produtos.buscar_por_nome_produto(nome)
    print("[DEBUG] Entrou na função 'produto_por_nome'")
    return produto


def _normalizar_valor_booleano(valor):
    if isinstance(valor, str):
        texto = valor.strip().lower()
        if texto in {"sim", "s", "1", "true", "yes"}:
            return 1
        return 0
    return int(bool(valor))


def _normalizar_data(data: str):
    if data is None:
        return datetime.now().strftime("%d/%m/%Y")
    texto = str(data).strip().lower()
    if texto in {"hoje", "today", "dia de hoje"}:
        return datetime.now().strftime("%d/%m/%Y")
    return texto


def _carregar_base_previsao():
    produtos_df = pd.read_csv(CAMINHO_PRODUTOS, sep=";")
    regras = pd.concat(
        [
            pd.read_csv(CAMINHO_REGRAS_AGOSTO, sep=";"),
            pd.read_csv(CAMINHO_REGRAS_SETEMBRO, sep=";"),
        ],
        ignore_index=True,
    )
    vendas = pd.concat(
        [
            pd.read_csv(CAMINHO_VENDAS_AGOSTO, sep=";"),
            pd.read_csv(CAMINHO_VENDAS_SETEMBRO, sep=";"),
        ],
        ignore_index=True,
    )
    vendas["Data"] = pd.to_datetime(vendas["Data"], format="%d/%m/%Y")
    regras["Dia"] = pd.to_datetime(regras["Dia"], format="%d/%m/%Y")
    return vendas, regras, produtos_df


def _montar_modelo_previsao():
    vendas, regras, produtos_df = _carregar_base_previsao()

    historico = (
        vendas.groupby(["Data", "Período", "Produto"], as_index=False)["Qtd"].sum()
        .merge(produtos_df, on="Produto", how="left")
        .merge(regras.rename(columns={"Dia": "Data"}), on="Data", how="left")
    )
    historico["Qtd_mediana_produto"] = historico.groupby("Produto")["Qtd"].transform("median")
    historico["demanda_alta"] = (historico["Qtd"] >= historico["Qtd_mediana_produto"]).astype(int)

    colunas_categoria = [
        "Setor",
        "Período",
        "Clima",
        "Véspera de Feriado",
        "Feriado",
        "Véspera de Fim de Semana",
        "Fim de Semana",
    ]
    dados_modelo = historico[colunas_categoria + ["demanda_alta"]].copy()
    dados_modelo = pd.get_dummies(dados_modelo, columns=colunas_categoria)

    modelo = LogisticRegression(max_iter=1000, class_weight="balanced", solver="liblinear")
    modelo.fit(dados_modelo.drop(columns=["demanda_alta"]), dados_modelo["demanda_alta"])

    return modelo, historico, produtos_df, regras


def _produtos_do_setor(setor: str = None):
    produtos_df = pd.read_csv(CAMINHO_PRODUTOS, sep=";")
    if setor is None:
        return produtos_df["Produto"].tolist()
    setor = setor.strip().lower()
    return produtos_df.loc[produtos_df["Setor"].str.lower() == setor, "Produto"].tolist()


def _fazer_previsao_para_produto(modelo, historico, produtos_df, regras, produto: str, data_alvo: str):
    produto = produto.strip()
    dados_produto = historico[historico["Produto"] == produto].copy()
    media_historica = dados_produto["Qtd"].mean() if not dados_produto.empty else 3.0
    mediana_historica = dados_produto["Qtd"].median() if not dados_produto.empty else 2.0

    regra_do_dia = regras[regras["Dia"].astype(str) == data_alvo].copy()
    if regra_do_dia.empty:
        regra_do_dia = pd.DataFrame([{
            "Dia": pd.to_datetime(data_alvo, format="%d/%m/%Y"),
            "Clima": "Calor",
            "Véspera de Feriado": "Não",
            "Feriado": "Não",
            "Véspera de Fim de Semana": "Não",
            "Fim de Semana": "Não",
        }])

    setor_do_produto = produtos_df.loc[produtos_df["Produto"] == produto, "Setor"].iloc[0] if produto in produtos_df["Produto"].values else "Geral"
    linha = pd.DataFrame([{
        "Setor": setor_do_produto,
        "Período": "Manhã",
        "Clima": regra_do_dia.iloc[0]["Clima"],
        "Véspera de Feriado": regra_do_dia.iloc[0]["Véspera de Feriado"],
        "Feriado": regra_do_dia.iloc[0]["Feriado"],
        "Véspera de Fim de Semana": regra_do_dia.iloc[0]["Véspera de Fim de Semana"],
        "Fim de Semana": regra_do_dia.iloc[0]["Fim de Semana"],
    }])
    linha = pd.get_dummies(linha, columns=["Setor", "Período", "Clima", "Véspera de Feriado", "Feriado", "Véspera de Fim de Semana", "Fim de Semana"])

    colunas_esperadas = modelo.feature_names_in_
    for coluna in colunas_esperadas:
        if coluna not in linha.columns:
            linha[coluna] = 0
    linha = linha.reindex(columns=colunas_esperadas, fill_value=0)

    probabilidade = float(modelo.predict_proba(linha)[0][1])
    margem = 0.75 + probabilidade * 0.75
    quantidade = max(1, int(round(max(mediana_historica, media_historica) * margem)))
    return {
        "produto": produto,
        "setor": setor_do_produto,
        "quantidade": quantidade,
        "probabilidade": probabilidade,
        "media_historica": float(media_historica),
    }


def previsao_producao_por_produto(produto: str, data: str = "hoje") -> str:
    """Estima a quantidade saudável a produzir de um produto em uma data específica usando regressão logística."""
    data_alvo = _normalizar_data(data)
    modelo, historico, produtos_df, regras = _montar_modelo_previsao()
    estimativa = _fazer_previsao_para_produto(modelo, historico, produtos_df, regras, produto, data_alvo)
    return (
        f"Produto: {estimativa['produto']}\n"
        f"Setor: {estimativa['setor']}\n"
        f"Quantidade estimada: {estimativa['quantidade']} unidades\n"
        f"Probabilidade de pico de demanda: {estimativa['probabilidade']:.0%}\n"
        f"Média histórica: {estimativa['media_historica']:.1f} unidades"
    )


def previsao_producao_por_setor(setor: str = None, data: str = "hoje") -> str:
    """Faz a estimativa saudável de produção por setor para um dia, considerando clima, feriado e dados históricos."""
    if setor is not None and str(setor).strip().lower() in {"geral", "todos", "todos os setores"}:
        setor = None

    if setor and setor.strip() and "/" in setor and len(setor.strip()) >= 6:
        data = setor.strip()
        setor = None

    data_alvo = _normalizar_data(data)
    modelo, historico, produtos_df, regras = _montar_modelo_previsao()

    setor_alvo = setor.strip() if setor else None
    lista_produtos = _produtos_do_setor(setor_alvo)
    if not lista_produtos:
        if setor_alvo is None:
            lista_produtos = _produtos_do_setor(None)
        else:
            return "Não encontrei produtos para esse setor. Verifique o nome do setor e tente novamente."

    estimativas = []
    total_geral = 0
    for nome_produto in lista_produtos:
        estimativa = _fazer_previsao_para_produto(modelo, historico, produtos_df, regras, nome_produto, data_alvo)
        estimativas.append(estimativa)
        total_geral += estimativa["quantidade"]

    linhas = [
        "Setor: " + (setor_alvo or "Todos") + " | Data: " + data_alvo,
        "-----------------------------------------",
    ]
    for item in estimativas:
        linhas.append(f"- {item['produto']}: {item['quantidade']} unidades (confiança {item['probabilidade']:.0%})")
    linhas.append(f"Total estimado: {total_geral} unidades")
    linhas.append("Margem: saudável, com resguardo para evitar quebra e desperdício excessivo.")
    return "\n".join(linhas)


def previsao_producao_geral(data: str = "hoje") -> str:
    return previsao_producao_por_setor(setor=None, data=data)