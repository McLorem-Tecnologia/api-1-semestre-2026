from ia.tools import dspy_tool
from ia import utils
from ia import services

def _tratar_parametros_iniciais(data: str, setor: str):
    """Trata a data, normaliza o setor e cria aquele texto bonito para a resposta."""
    
    data_limpa = data if data and str(data).strip().lower() not in ['none', 'null'] else "hoje"
    
    data_real = utils.converter_data_relativa(data_limpa)
    setor_limpo = utils.normalizar_setor(setor) if setor else ""
    
    termo = data_limpa.strip().lower()
    if termo in ['hoje', 'hj', 'ontem', 'anteontem', 'amanhã', 'amanha'] or 'dias' in termo:
        texto_data_amigavel = f"{termo} ({data_real})"
    else:
        texto_data_amigavel = f"no dia {data_real}"
        
    return data_real, setor_limpo, texto_data_amigavel

def _formatar_lista_produtos(resultado: list, tipo_pergunta: str) -> str:
    """Monta os bullet points dependendo se o usuário quer 'quais' ou 'quantos'."""
    tipo_pergunta = tipo_pergunta if tipo_pergunta else "quanto"
    texto = ""
    
    for item in resultado:
        if tipo_pergunta.lower() in ['qual', 'quais', 'o que']:
            nome_produto = item.split(":")[0]
            texto += f"- {nome_produto}\n"
        else:
            texto += f"- {item} unidades\n"
            
    return texto

@dspy_tool('PRODUCAO')
def tool_previsao_vendas_por_data(data: str = "hoje", setor: str = "", tipo_pergunta: str = "quanto") -> str:
    # US-01 e US-02
    # US-01: Eu, como líder, quero saber QUAIS produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.
    # US-02: Eu, como líder, quero saber QUANTOS produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto.
    """Use esta ferramenta EXCLUSIVAMENTE para PREVISÃO DE PRODUÇÃO (foco em ação atual ou futura).
    Acione-a para responder perguntas como: "O que precisamos produzir?", "Quanto devemos produzir amanhã?", "O que produzir daqui a 3 dias?".
    
    Lógica interna: A ferramenta analisa se a data solicitada é dia de pico ou comum, cruzando e calculando a média ideal de produção baseada no histórico.
    
    Parâmetros:
    - data (opcional): data exata ('30/09/2026'), palavras relativas ('hoje', 'amanhã') ou tempo relativo ('daqui a 3 dias', 'em 5 dias'). SE NÃO ESPECIFICADO, DEIXE VAZIO (o sistema assumirá 'hoje').
    - setor (opcional): nome do setor (ex: 'Padaria'). Deixe vazio se não for especificado.
    - tipo_pergunta (OBRIGATÓRIO AVALIAR): Você deve classificar a intenção da frase do usuário. Se ele usar palavras como "Qual", "Quais", ou perguntar "O que", preencha com "quais". Se pedir números, preencha com "quanto".
        
    REGRA ABSOLUTA: Entregue os dados com foco em AÇÃO. Repasse EXATAMENTE os números retornados.
    """
    try:
        data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)

        df_historico_limpo = services.producao.dataframe_vendas_similares(data_real)
        
        if df_historico_limpo.empty:
            return f"Não encontrei dados históricos compatíveis para projetar a produção do dia {texto_data}."
            
        resultado = services.producao.media_vendas_produtos(df_historico_limpo, setor)
        
        if not resultado:
            aviso = f" no setor '{setor}'" if setor else ""
            return f"Não há histórico suficiente para projetar a produção{aviso} do dia {texto_data}."
            
        aviso_setor = f" (Setor: {setor})" if setor else ""
        texto_resposta = f"PREVISÃO DE PRODUÇÃO: O que DEVE ser produzido para o dia {texto_data}{aviso_setor}:\n"
        texto_resposta += "(Baseado no perfil de demanda projetado para esta data)\n\n"
        
        texto_resposta += _formatar_lista_produtos(resultado, tipo_pergunta)
        return texto_resposta

    except Exception as e:
        print(f"[ERRO - tool_previsao_vendas_por_data] Falha: {e}")
        return "Ocorreu um erro técnico ao cruzar os dados. Informe ao usuário que não foi possível projetar a produção neste momento."

@dspy_tool('PRODUCAO')
def tool_meta_producao_passada(data: str = "hoje", setor: str = "", tipo_pergunta: str = "quanto") -> str:
    # US-04
    # US-04: Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de consultar a meta ideal.
    """Use esta ferramenta EXCLUSIVAMENTE para AUDITORIA e METAS PASSADAS (foco em cobrança ou verificação).
    Acione-a para responder perguntas como: "O que DEVERIA ter sido produzido ontem?", "Qual era a meta de 3 dias atrás?".
    
    Lógica interna: Ela cruza o perfil histórico do dia para dizer a média ideal que a equipe DEVERIA ter alcançado.
    
    Parâmetros:
    - data (opcional): data exata ('20/09/2026'), palavras relativas ('ontem', 'hoje'). SE NÃO ESPECIFICADO, assumirá 'hoje'.
    - setor (opcional): nome do setor (ex: 'Padaria'). Deixe vazio se não for especificado.
    - tipo_pergunta (OBRIGATÓRIO AVALIAR): Se usar "Qual", "Quais", ou "O que", preencha com "quais". Se pedir números, preencha com "quanto".
    """
    try:
        data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)

        df_historico_limpo = services.producao.dataframe_vendas_similares(data_real)
        
        if df_historico_limpo.empty:
            return f"Não encontrei histórico compatível para auditar a meta do dia {texto_data}."
            
        resultado = services.producao.media_vendas_produtos(df_historico_limpo, setor)
        
        if not resultado:
            aviso = f" no setor '{setor}'" if setor else ""
            return f"Não há dados suficientes para estipular o que deveria ter sido produzido{aviso} no dia {texto_data}."
            
        aviso_setor = f" (Setor: {setor})" if setor else ""
        texto_resposta = f"RELATÓRIO DE META: O que DEVERIA TER SIDO PRODUZIDO no dia {texto_data}{aviso_setor}:\n"
        texto_resposta += "(Cálculo da meta ideal baseada no perfil histórico do dia)\n\n"
        
        texto_resposta += _formatar_lista_produtos(resultado, tipo_pergunta)
        return texto_resposta

    except Exception as e:
        print(f"[ERRO - tool_meta_producao_passada] Falha: {e}")
        return "Ocorreu um erro técnico ao calcular a meta histórica de produção."

@dspy_tool('PRODUCAO')
def tool_producao_por_data(data: str, setor: str = "") -> str:
    # US-03
    # US-03: Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y.
    """Use esta ferramenta EXCLUSIVAMENTE para consultar a PRODUÇÃO REAL (produtividade já executada) em uma data exata.
    Acione-a para responder perguntas como: "O que foi produzido hoje?", "Qual a produtividade da Confeitaria ontem?".
    
    Lógica interna: Soma automaticamente os registros reais de Vendas + Descartes do dia para entregar o total produzido.
    
    Parâmetros:
    - data (obrigatório): data exata ('15/08/2026'), palavras relativas ('ontem', 'hoje') ou tempo relativo.
    - setor (opcional): nome do setor (ex: 'Padaria'). Se o usuário perguntar o geral, deixe vazio.
    
    REGRA ABSOLUTA PARA A RESPOSTA FINAL: 
    NÃO RESUMA. NÃO ABREVIES. O usuário PRECISA ver a lista de todos os produtos.
    Você DEVE transcrever a tabela inteira gerada por esta ferramenta na sua resposta final, linha por linha.
    """
    try:
        if not data or str(data).strip().lower() in ['none', 'null', '']:
            return "Falta a data. Pergunte ao usuário de qual data ele quer saber a produção."
            
        data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)

        dados_calculados = services.producao.calcular_producao_data(data_real, setor)
        
        if dados_calculados is None:
            return f"Nenhum produto encontrado para o setor '{setor}'."
            
        if not dados_calculados:
            aviso = f" no setor '{setor}'" if setor else " no panorama geral"
            return f"Não houve registros de produção{aviso} em {texto_data}."
            
        aviso_setor = f" ({setor})" if setor else ""
        texto_resposta = f"RELATÓRIO DE PRODUÇÃO REAL: O que FOI PRODUZIDO {texto_data}{aviso_setor}:\n"
        texto_resposta += "(Soma real das vendas e descartes registrados)\n\n"

        producao_total = 0
        
        for produto, valores in sorted(dados_calculados.items()):
            producao_total += valores['producao']
            texto_resposta += f"- {produto} | Total Produzido: {valores['producao']} (Vendas: {valores['vendas']}, Descarte: {valores['descarte']})\n"

        texto_resposta += f"\nNo total foram produzidas {producao_total} unidades."
        
        return texto_resposta

    except Exception as e:
        print(f"[ERRO - tool_producao_por_data] Falha ao calcular: {e}")
        return "Ocorreu um erro técnico inesperado ao tentar acessar os dados reais de produção."