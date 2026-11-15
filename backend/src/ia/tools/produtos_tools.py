from ia import procedures
from ia.tools import dspy_tool
import pandas as pd
from paths import DADOS_DIR

@dspy_tool('PRODUTOS')
def listar_todos_produtos() -> str:
    """Retorna o catálogo completo com todos os produtos disponíveis no supermercado.
    Use esta ferramenta APENAS quando o usuário fizer uma solicitação genérica para ver 'tudo o que tem', 'lista de produtos' ou 'quais são os produtos disponíveis'.
    Não use esta ferramenta se o usuário perguntar sobre um produto específico.
    """
    print('[DEBUG] Entrou na função listar_todos_produtos')
    return procedures.produtos.listar()

@dspy_tool('PRODUTOS')
def listar_detalhes_todos_produtos() -> str:
    """Retorna o catálogo completo de produtos incluindo TODOS os detalhes: Nome, Setor e Tempo de preparo de cada item.
    Use esta ferramenta quando o usuário pedir 'a tabela completa', 'todos os dados dos produtos' ou quiser ver os detalhes de todos os itens do supermercado de uma só vez.
    """
    print('[DEBUG] Entrou na função listar_detalhes_todos_produtos')
    return procedures.produtos.listar_detalhado()

@dspy_tool('PRODUTOS')
def informacoes_produto(nome: str) -> str:
    """Busca detalhes e informações de UM produto específico pelo seu nome.
    Use esta ferramenta quando o usuário perguntar sobre um item específico (exemplo: 'informações da coxinha', 'tem pão francês?').
    Você DEVE extrair o nome do produto da mensagem do usuário e passar como parâmetro.
    """
    print(f'[DEBUG] Entrou na função informacoes_produto buscando: {nome}')
    return procedures.produtos.buscar_por_nome(nome)

@dspy_tool('PRODUTOS')
def informacoes_produto_setor(setor: str) -> str:
    """Busca detalhes e informações de produtos de UM setor específico pelo seu nome.
    Use esta ferramenta quando o usuário perguntar sobre um setor específico (exemplo: 'informações do setor da confeitaria', 'tem produtos no setor de padaria?').
    Você DEVE extrair o nome do setor da mensagem do usuário e passar como parâmetro.
    """
    print(f'[DEBUG] Entrou na função informacoes_produto_setor buscando: {setor}')
    return procedures.produtos.buscar_por_setor(setor)

@dspy_tool('PRODUTOS')
def produto_por_tempo_preparo(tempo: str) -> str:
    """Busca a lista de produtos que levam um tempo específico para serem preparados.
    Use esta ferramenta quando o usuário perguntar por opções baseadas no tempo (exemplo: 'quais produtos ficam prontos em 5 min?', 'o que tem com tempo de 10 min?').
    Você DEVE extrair o tempo exato da mensagem do usuário (ex: 'X min', 'X minutos' ou 'Xmin') e passar como parâmetro.
    """
    print(f'[DEBUG] Entrou na função produto_por_tempo_preparo buscando: {tempo}')
    return procedures.produtos.buscar_por_tempo(tempo)

@dspy_tool('VENDAS')
def produtos_do_setor(setor: str = "") -> str:
    """Retorna todos os produtos ligados a um setor específico.
    Use esta ferramenta quando o usuário perguntar quais produtos pertencem a um setor
    (exemplo: 'quais produtos tem no setor da padaria?', 'lista os produtos do açougue').
    
    Parâmetros:
    - setor (opcional): nome do setor (ex: 'Padaria', 'Cozinha', 'Peixaria').
      Deixe vazio se o usuário quiser ver todos os produtos sem filtrar por setor.
    """
    print(f'[DEBUG] Entrou na função produtos_do_setor buscando: {setor}')
    setor_limpo = setor if setor and str(setor).strip().lower() not in ['none', 'null', 'vazio', ''] else None
    resultado = procedures.produtos.produtos_por_setor(setor_limpo)
    
    if not resultado:
        return f"Não encontrei produtos para o setor '{setor}'." if setor else "Não há produtos cadastrados."
    
    linhas = [f"- {p['Produto']} (R$ {p['Preço']:.2f})" for p in resultado]
    if setor:
        return f"Produtos do setor '{setor}':\n" + "\n".join(linhas)
    return "\n".join(linhas)

@dspy_tool('VENDAS')
def valores_dos_produtos(produtos: str) -> str:
    """Recebe uma lista de produtos e retorna o valor (Preço) de cada um.
    Use esta ferramenta quando o usuário quiser saber o preço de uma lista de produtos.
    
    Parâmetros:
    - produtos (texto): lista de produtos, um por linha ou separados por vírgula
      (exemplo: 'Pão Francês (Kg), Frango assado (Un), Marmita (Un)').
    """
    print(f'[DEBUG] Entrou na função valores_dos_produtos buscando: {produtos}')
    lista = [p.strip() for p in produtos.replace(',', '\n').splitlines() if p.strip()]
    
    if not lista:
        return "Informe ao menos um produto para consultar o valor."
    
    produtos_dict = [{'Produto': nome} for nome in lista]
    valores = procedures.produtos.valores_por_produtos(produtos_dict)
    
    linhas = []
    for v in valores:
        if v['Preço'] is not None:
            linhas.append(f"- {v['Produto']}: R$ {v['Preço']:.2f}")
        else:
            linhas.append(f"- {v['Produto']}: preço não encontrado")
    
    return "Valor de cada produto:\n" + "\n".join(linhas)

def _ler_csv_lucro(nome, colunas, numeros=(), tem_data=False):
    """Lê e valida um CSV; devolve a tabela ou informa o dado inválido."""
    tabela = pd.read_csv(DADOS_DIR / nome, sep=";", encoding="utf-8-sig", dtype=str)
    tabela = tabela[list(colunas)].copy()
    if tabela.empty or tabela.isna().any().any():
        raise ValueError(f"{nome}: arquivo sem dados ou com células obrigatórias vazias.")
    for coluna in numeros:
        tabela[coluna] = pd.to_numeric(tabela[coluna], errors="raise")
        if (tabela[coluna] < 0).any() or tabela[coluna].isin([float("inf"), -float("inf")]).any():
            raise ValueError(f"{nome}: {coluna} deve conter números finitos e não negativos.")
    if tem_data:
        tabela["Data"] = pd.to_datetime(tabela["Data"], format="%d/%m/%Y", errors="raise")
    return tabela


def _calcular_lucros_us08(data_inicio="", data_fim="", setor=""):
    """Retorna ranking, cálculos diários, período e SKUs com unidades incompatíveis."""
    if not all(isinstance(valor, str) for valor in (data_inicio, data_fim, setor)):
        raise TypeError("Datas e setor devem ser textos; use vazio para não filtrar.")
    inicio = pd.to_datetime(data_inicio, format="%d/%m/%Y") if data_inicio else None
    fim = pd.to_datetime(data_fim, format="%d/%m/%Y") if data_fim else None
    if inicio is not None and fim is not None and inicio > fim:
        raise ValueError("A data inicial deve ser anterior ou igual à final.")
    produtos = _ler_csv_lucro("produtos.csv", ["SKU", "Produto", "Setor"])
    receitas = _ler_csv_lucro("receitas.csv", ["SKU", "Ingrediente", "Qtd", "Unidade"], ["Qtd"])
    precos = _ler_csv_lucro("historico_produtos.csv", ["SKU", "Data", "Preço Venda"], ["Preço Venda"], True)
    custos = _ler_csv_lucro("historico_ingredientes.csv", ["Ingrediente", "Data", "Preço Custo", "Unidade"], ["Preço Custo"], True)
    if precos.duplicated(["SKU", "Data"]).any() or custos.duplicated(["Ingrediente", "Data"]).any():
        raise ValueError("Há preços históricos duplicados para a mesma data.")
    arquivos = sorted((DADOS_DIR / "vendas").glob("vendas_*.csv"))
    if not arquivos:
        raise FileNotFoundError("Não foram encontrados arquivos de vendas.")
    vendas = pd.concat([
        _ler_csv_lucro(f"vendas/{arquivo.name}", ["Data", "SKU", "Qtd"], ["Qtd"], True)
        for arquivo in arquivos
    ], ignore_index=True)
    vendas = vendas.merge(produtos, on="SKU", how="left", validate="many_to_one")
    if vendas["Produto"].isna().any():
        raise ValueError("Há vendas com SKU sem cadastro.")
    if inicio is not None:
        vendas = vendas[vendas["Data"] >= inicio]
    if fim is not None:
        vendas = vendas[vendas["Data"] <= fim]
    if setor.strip():
        vendas = vendas[vendas["Setor"].str.casefold() == setor.strip().casefold()]
    vendas = vendas[vendas["Qtd"] > 0]
    periodo = f"{vendas['Data'].min():%d/%m/%Y} a {vendas['Data'].max():%d/%m/%Y}" if not vendas.empty else ""
    vendas = vendas.groupby(["Data", "SKU"], as_index=False)["Qtd"].sum()

    dias = []
    excluidos = set()
    for data, vendas_dia in vendas.groupby("Data"):
        # Usa somente o último preço conhecido até a data da venda.
        precos_dia = precos[precos["Data"] <= data].sort_values("Data").drop_duplicates("SKU", keep="last")
        custos_dia = custos[custos["Data"] <= data].sort_values("Data").drop_duplicates("Ingrediente", keep="last")
        ficha = receitas[receitas["SKU"].isin(vendas_dia["SKU"])].merge(
            custos_dia.drop(columns="Data"), on="Ingrediente", how="left", suffixes=("", "_historico")
        )
        if ficha["Preço Custo"].isna().any():
            raise ValueError("Falta preço histórico de um ingrediente.")
        # Sem conversão entre unidades e quilos, o produto é excluído com aviso.
        excluidos.update(ficha.loc[ficha["Unidade"] != ficha["Unidade_historico"], "SKU"])
        ficha["Custo unitário"] = ficha["Qtd"] * ficha["Preço Custo"]
        custo_produtos = ficha.groupby("SKU", as_index=False)["Custo unitário"].sum()
        calculo = vendas_dia.merge(precos_dia[["SKU", "Preço Venda"]], on="SKU", how="left")
        calculo = calculo.merge(custo_produtos, on="SKU", how="left")
        if calculo[["Preço Venda", "Custo unitário"]].isna().any().any():
            raise ValueError("Há produto sem receita ou sem preço histórico de venda.")
        calculo["Receita"] = calculo["Preço Venda"] * calculo["Qtd"]
        calculo["Custo"] = calculo["Custo unitário"] * calculo["Qtd"]
        calculo["Lucro"] = calculo["Receita"] - calculo["Custo"]
        dias.append(calculo)
    if not dias:
        return pd.DataFrame(), pd.DataFrame(), periodo, excluidos
    detalhes = pd.concat(dias, ignore_index=True)
    detalhes = detalhes[~detalhes["SKU"].isin(excluidos)]
    ranking = detalhes.groupby("SKU", as_index=False)[["Qtd", "Receita", "Custo", "Lucro"]].sum()
    ranking = ranking.merge(produtos, on="SKU").sort_values(["Lucro", "Produto"], ascending=[False, True])
    return ranking, detalhes, periodo, excluidos


def _reais_lucro(valor):
    """Formata um valor em reais."""
    return "R$ " + f"{valor:.2f}".replace(".", ",")


def _responder_lucro(tipo, limite=0, produto="", data_inicio="", data_fim="", setor=""):
    """Prepara a resposta da US08 e transforma erros em mensagens para o usuário."""
    try:
        if isinstance(limite, bool) or not isinstance(limite, int) or limite < 0:
            raise ValueError("O limite deve ser inteiro e não negativo; 0 significa todos.")
        ranking, detalhes, periodo, excluidos = _calcular_lucros_us08(data_inicio, data_fim, setor)
        aviso = "\nAviso: ranking parcial. SKUs excluídos por unidades incompatíveis: " + ", ".join(sorted(excluidos)) if excluidos else ""
        if ranking.empty:
            return "Não há vendas válidas para calcular o lucro." + aviso
        linhas = [f"Lucro bruto estimado de {periodo}; receita por unidade vendida, sem descarte/despesas." + aviso]
        if tipo == "conferencia":
            if not isinstance(produto, str) or not produto.strip():
                raise ValueError("Informe o nome ou SKU do produto.")
            busca = produto.strip().casefold()
            encontrados = ranking[(ranking["SKU"] == busca) | (ranking["Produto"].str.casefold() == busca)]
            if encontrados.empty:
                encontrados = ranking[ranking["Produto"].str.casefold().str.contains(busca, regex=False)]
            if len(encontrados) != 1:
                return "Informe um nome único ou SKU de produto com vendas e custo válido." + aviso
            item = encontrados.iloc[0]
            linhas.append(f"{item['Produto']} | Setor: {item['Setor']}")
            linhas.append("Fontes: vendas/*.csv, receitas.csv, historico_produtos.csv e historico_ingredientes.csv.")
            linhas.append("Custo unitário = soma de quantidade de ingrediente × preço histórico.")
            for _, dia in detalhes[detalhes["SKU"] == item["SKU"]].iterrows():
                linhas.append(f"• {dia['Data']:%d/%m/%Y}: ({dia['Preço Venda']:.6f} − {dia['Custo unitário']:.6f}) × {dia['Qtd']:g} = {_reais_lucro(dia['Lucro'])}")
            linhas.append(f"Total sem arredondamentos intermediários: receita {_reais_lucro(item['Receita'])} − custo {_reais_lucro(item['Custo'])} = lucro {_reais_lucro(item['Lucro'])}.")
        elif tipo == "setores":
            selecionados = ranking.head(limite) if limite else ranking
            linhas.append("Setores dos produtos selecionados; a soma considera apenas esses produtos.")
            for nome, grupo in selecionados.groupby("Setor"):
                linhas.append(f"• {nome}: {_reais_lucro(grupo['Lucro'].sum())} — " + ", ".join(grupo["Produto"]))
        else:
            selecionados = ranking.head(limite) if limite else ranking
            for _, item in selecionados.iterrows():
                linhas.append(f"• {item['Produto']} | Setor: {item['Setor']} | Lucro: {_reais_lucro(item['Lucro'])} | Receita: {_reais_lucro(item['Receita'])} | Custo: {_reais_lucro(item['Custo'])} | Quantidade: {item['Qtd']:g}")
        return "\n".join(linhas)
    except (OSError, UnicodeError, KeyError, ValueError, TypeError, pd.errors.EmptyDataError, pd.errors.ParserError) as erro:
        return f"Erro ao calcular lucro: {erro}"


@dspy_tool('VENDAS')
def produtos_mais_lucrativos(limite: int = 0, data_inicio: str = "", data_fim: str = "", setor: str = "") -> str:
    """Retorna ranking de lucro e setor. Recebe limite (0=todos), datas DD/MM/AAAA e setor opcionais.
    Sem datas, usa todas as vendas disponíveis. Preço isolado não representa lucro.
    """
    return _responder_lucro("produtos", limite, data_inicio=data_inicio, data_fim=data_fim, setor=setor)


@dspy_tool('VENDAS')
def setores_dos_produtos_mais_lucrativos(limite: int = 5, data_inicio: str = "", data_fim: str = "") -> str:
    """Retorna os setores presentes no top N produtos e a soma do lucro desses produtos.
    Recebe limite (padrão 5; 0=todos) e datas DD/MM/AAAA opcionais.
    """
    return _responder_lucro("setores", limite, data_inicio=data_inicio, data_fim=data_fim)


@dspy_tool('VENDAS')
def cinco_produtos_mais_lucrativos(data_inicio: str = "", data_fim: str = "") -> str:
    """Retorna até cinco produtos mais lucrativos. Recebe datas DD/MM/AAAA opcionais."""
    return _responder_lucro("produtos", 5, data_inicio=data_inicio, data_fim=data_fim)


@dspy_tool('VENDAS')
def conferir_lucro_produto(produto: str, data_inicio: str = "", data_fim: str = "") -> str:
    """Retorna cálculo diário e total para conferência. Recebe nome/SKU e datas opcionais."""
    return _responder_lucro("conferencia", produto=produto, data_inicio=data_inicio, data_fim=data_fim)