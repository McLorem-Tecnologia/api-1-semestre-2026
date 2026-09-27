# Funções para estimativa de produção.
# Função para TOOLS do DSPY relacionadas a produção.
from pathlib import Path
from ia.tools.utils import dspy_tool, converter_data_relativa, normalizar_setor, classificar_dia
from ia.procedures import procedures

@dspy_tool
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
    - tipo_pergunta (OBRIGATÓRIO AVALIAR): Você deve classificar a intenção da frase do usuário. Se ele usar palavras como "Qual", "Quais", ou perguntar "O que", preencha EXATAMENTE com a string "quais". Se ele perguntar "Quanto", "Quantos", ou pedir números, preencha com "quanto".
        
    REGRA ABSOLUTA: Entregue os dados com foco em AÇÃO. Repasse EXATAMENTE os números retornados.
    """
    try:
        if not data: data = "hoje"
        if not tipo_pergunta: tipo_pergunta = "quanto"
        if setor: setor = normalizar_setor(setor)
        
        data_real = converter_data_relativa(data)

        termo = data.strip().lower()
        if termo in ['hoje', 'hj', 'amanhã', 'amanha']:
            texto_data_amigavel = f"{termo} ({data_real})"
        else:
            texto_data_amigavel = f"no dia {data_real}"

        filtro_correto = classificar_dia(data_real)
        df_historico_limpo = procedures.vendas.dataframe_vendas_similares(data_real, filtro_correto)
        
        if df_historico_limpo.empty:
            return f"Não encontrei dados históricos compatíveis para projetar a produção do dia {texto_data_amigavel}."
            
        resultado = procedures.vendas.media_vendas_produtos(df_historico_limpo, setor)
        
        if not resultado:
            texto_setor = f" no setor '{setor}'" if setor else ""
            return f"Não há histórico suficiente para projetar a produção{texto_setor} do dia {texto_data_amigavel}."
            
        aviso_setor = f" (Setor: {setor})" if setor else ""
        
        # Resposta com foco em AÇÃO / FUTURO
        texto_resposta = f"PREVISÃO DE PRODUÇÃO: O que DEVE ser produzido para o dia {texto_data_amigavel}{aviso_setor}:\n"
        texto_resposta += "(Baseado no perfil de demanda projetado para esta data)\n\n"
        
        for item in resultado:
            if tipo_pergunta.lower() in ['qual', 'quais', 'o que']:
                nome_produto = item.split(":")[0]
                texto_resposta += f"- {nome_produto}\n"
            else:
                texto_resposta += f"- {item} unidades\n"
            
        return texto_resposta

    except Exception as e:
        print(f"[ERRO - tool_previsao_vendas_por_data] Falha: {e}")
        return "Ocorreu um erro técnico inesperado ao cruzar os dados para a previsão. Informe ao usuário de forma amigável que não foi possível projetar a produção neste momento."

@dspy_tool
def tool_meta_producao_passada(data: str = "hoje", setor: str = "", tipo_pergunta: str = "quanto") -> str:
    # US-04
    # US-04: Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de consultar a meta ideal.
    """Use esta ferramenta EXCLUSIVAMENTE para AUDITORIA e METAS PASSADAS (foco em cobrança ou verificação).
    Acione-a para responder perguntas como: "O que DEVERIA ter sido produzido ontem?", "Qual era a meta de 3 dias atrás?" ou "Quais produtos a equipe deveria ter feito há 2 dias?".
    
    Lógica interna: Ela cruza o perfil histórico do dia para dizer a média ideal que a equipe DEVERIA ter alcançado.
    
    Parâmetros:
    - data (opcional): data exata ('20/09/2026'), palavras relativas ('ontem', 'hoje') ou tempo relativo ('3 dias atrás', 'há 5 dias'). SE NÃO ESPECIFICADO, DEIXE VAZIO (o sistema assumirá 'hoje').
    - setor (opcional): nome do setor (ex: 'Padaria'). Deixe vazio se não for especificado.
    - tipo_pergunta (OBRIGATÓRIO AVALIAR): Você deve classificar a intenção da frase do usuário. Se ele usar palavras como "Qual", "Quais", ou perguntar "O que", preencha EXATAMENTE com a string "quais". Se ele perguntar "Quanto", "Quantos", ou pedir números, preencha com "quanto".

    REGRA ABSOLUTA: Entregue os dados com foco em AUDITORIA (Ex: "O que deveria ter sido produzido era..."). Repasse EXATAMENTE os números retornados.
    """
    try:
        if not data: data = "hoje"
        if setor: setor = normalizar_setor(setor)
            
        data_real = converter_data_relativa(data)

        termo = data.strip().lower()
        if termo in ['hoje', 'hj', 'ontem', 'anteontem', 'amanhã', 'amanha'] or 'dias' in termo:
            texto_data_amigavel = f"{termo} ({data_real})"
        else:
            texto_data_amigavel = f"no dia {data_real}"

        filtro_correto = classificar_dia(data_real)
        df_historico_limpo = procedures.vendas.dataframe_vendas_similares(data_real, filtro_correto)
        
        if df_historico_limpo.empty:
            return f"Não encontrei histórico compatível para auditar a meta do dia {texto_data_amigavel}."
            
        resultado = procedures.vendas.media_vendas_produtos(df_historico_limpo, setor)
        
        if not resultado:
            texto_setor = f" no setor '{setor}'" if setor else ""
            return f"Não há dados suficientes para estipular o que deveria ter sido produzido{texto_setor} no dia {texto_data_amigavel}."
            
        aviso_setor = f" (Setor: {setor})" if setor else ""
        texto_resposta = f"RELATÓRIO DE META: O que DEVERIA TER SIDO PRODUZIDO no dia {texto_data_amigavel}{aviso_setor}:\n"
        texto_resposta += "(Cálculo da meta ideal baseada no perfil histórico do dia)\n\n"
        
        for item in resultado:
            if tipo_pergunta.lower() in ['qual', 'quais', 'o que']:
                nome_produto = item.split(":")[0]
                texto_resposta += f"- {nome_produto}\n"
            else:
                texto_resposta += f"- {item} unidades\n"
            
        return texto_resposta

    except Exception as e:
        print(f"[ERRO - tool_meta_producao_passada] Falha: {e}")
        return "Ocorreu um erro técnico ao calcular a meta histórica de produção. Peça desculpas ao usuário de forma amigável."

@dspy_tool
def tool_producao_por_data(data: str, setor: str = "") -> str:
    # US-03
    # US-03: Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y.
    """Use esta ferramenta EXCLUSIVAMENTE para consultar a PRODUÇÃO REAL (produtividade já executada) em uma data exata.
    Acione-a para responder perguntas como: "O que foi produzido hoje?", "O que produzimos há 3 dias na Padaria?", "Qual a produtividade da Confeitaria ontem?".
    
    Lógica interna: A ferramenta soma automaticamente os registros reais de Vendas + Descartes do dia para entregar o total produzido. Pode ser usada para um setor específico ou para todo o supermercado.
    
    Parâmetros:
    - data (obrigatório): data exata ('15/08/2026'), palavras relativas ('ontem', 'hoje') ou tempo relativo ('3 dias atrás', 'há 2 dias').
    - setor (opcional): nome do setor (ex: 'Padaria', 'Açougue'). Se o usuário perguntar o geral do supermercado, sem citar setor, deixe vazio (None).
    
    REGRA ABSOLUTA: Entregue os dados com foco no PASSADO/REALIZADO. Repasse EXATAMENTE os números retornados.
    """
    try:
        if not data or str(data).strip().lower() in ['none', 'null']:
            return "Falta a data. Pergunte ao usuário de qual data ele quer saber a produção."
            
        if setor: setor = normalizar_setor(setor)
            
        data_real = converter_data_relativa(data)

        termo = data.strip().lower()
        if termo in ['hoje', 'hj', 'ontem', 'anteontem', 'amanhã', 'amanha'] or 'dias' in termo:
            texto_data_amigavel = f"{termo} ({data_real})"
        else:
            texto_data_amigavel = f"no dia {data_real}"

        # Chama a procedure (agora com o nome atualizado)
        dados_calculados = procedures.producao.calcular_producao_data(data_real, setor)
        
        if dados_calculados is None:
            return f"Nenhum produto encontrado para o setor '{setor}'."
            
        if not dados_calculados:
            texto_setor = f" no setor '{setor}'" if setor else " no panorama geral"
            return f"Não houve registros de produção{texto_setor} em {texto_data_amigavel}."
            
        aviso_setor = f" ({setor})" if setor else ""
        texto_resposta = f"RELATÓRIO DE PRODUÇÃO REAL: O que FOI PRODUZIDO {texto_data_amigavel}{aviso_setor}:\n"
        texto_resposta += "(Soma real das vendas e descartes registrados)\n\n"

        producao_total = 0
        
        for produto, valores in sorted(dados_calculados.items()):
            producao_total += valores['producao']
            texto_resposta += f"- {produto} | Total Produzido: {valores['producao']} (Vendas: {valores['vendas']}, Descarte: {valores['descarte']})\n"

        texto_resposta += f"\nNo total foram produzidas {producao_total} unidades"
        
        return texto_resposta

    except Exception as e:
        print(f"[ERRO - tool_producao_por_data] Falha ao calcular: {e}")
        return "Ocorreu um erro técnico inesperado ao tentar acessar os dados reais de produção. Informe ao usuário de forma amigável que não foi possível realizar o cálculo neste momento."
