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





    """
    try:





