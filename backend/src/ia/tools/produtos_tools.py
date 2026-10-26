from ia import procedures
from ia.tools import dspy_tool

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

@dspy_tool('PRODUTOS')
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

@dspy_tool('PRODUTOS')
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