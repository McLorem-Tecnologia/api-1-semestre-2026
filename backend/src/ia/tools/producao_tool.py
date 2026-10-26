from ia.tools import dspy_tool
from ia import procedures; from ia import services; from ia import utils

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
    i = 1
    
    for item in resultado:
        if tipo_pergunta.lower() in ['qual', 'quais', 'o que']:
            nome_produto = item.split(":")[0]
            texto += f"{i} {nome_produto}\n"
        else:
            texto += f"{i} {item} unidades\n"
        i += 1
            
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
    - data (opcional): data ou referência de tempo exatamente como o usuário disse, sem
      calcular a data. Aceita datas numéricas ('20/09/2026'), por extenso ('2 de novembro de 2026'),
      termos relativos ('hoje', 'ontem', 'amanhã', 'depois de amanhã'), contagem de dias
      ('há 2 dias', 'daqui a 5 dias') e dias da semana ('segunda passada', 'próxima sexta').
      Se não especificado, assume 'hoje'.
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
    - data (opcional): data ou referência de tempo exatamente como o usuário disse, sem
      calcular a data. Aceita datas numéricas ('20/09/2026'), por extenso ('2 de novembro de 2026'),
      termos relativos ('hoje', 'ontem', 'amanhã', 'depois de amanhã'), contagem de dias
      ('há 2 dias', 'daqui a 5 dias') e dias da semana ('segunda passada', 'próxima sexta').
      Se não especificado, assume 'hoje'.
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
    - data (obrigatório): data ou referência de tempo exatamente como o usuário disse, sem
      calcular a data. Aceita datas numéricas ('20/09/2026'), por extenso ('2 de novembro de 2026'),
      termos relativos ('hoje', 'ontem', 'amanhã', 'depois de amanhã'), contagem de dias
      ('há 2 dias', 'daqui a 5 dias') e dias da semana ('segunda passada', 'próxima sexta').
      Se não especificado, assume 'hoje'.
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

@dspy_tool('PRODUCAO')
def tool_previsao_quantidade_mp (data = "hoje", setor = "" ):
    """
    Parâmetros:US-10: Quantidade de Matéria-Prima ou Ingredientes para deixar preparada ou separada para a produção de um dia específico.

Permite consultar e calcular a quantidade total de cada matéria-prima necessária
para atender ao planejamento de produção de uma determinada data, consolidando
os insumos utilizados por todos os produtos programados. O objetivo é auxiliar
na separação e preparação antecipada dos materiais necessários para a operação.

    - data (opcional): data ou referência de tempo exatamente como o usuário disse, sem
      calcular a data. Aceita datas numéricas ('20/09/2026'), por extenso ('2 de novembro de 2026'),
      termos relativos ('hoje', 'ontem', 'amanhã', 'depois de amanhã'), contagem de dias
      ('há 2 dias', 'daqui a 5 dias') e dias da semana ('segunda passada', 'próxima sexta').
      Se não especificado, assume 'hoje'.
    - setor (opcional): nome do setor (ex: 'Padaria'). Deixe vazio se não for especificado.
    """
    data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)

    df_historico_limpo = services.producao.dataframe_vendas_similares(data_real)
    
    if df_historico_limpo.empty:
        return f"Não encontrei histórico compatível para auditar a meta do dia {texto_data}."
        
    resultado = services.producao.media_vendas_produtos(df_historico_limpo, setor)
    texto = ""
    lista = []
    for item in resultado:
        nome = item.split(":")[0]
        nome = procedures.produtos.nome_para_skus(nome)
        lista.append(nome)

    produtos_disponiveis = procedures.ingredientes.formatacao_pre_calculo(lista)

    for item in resultado:
        nome_produto = item.split(":")[0]
        quantidade_produto = float(item.split(":")[1])
        sku_produto = procedures.produtos.nome_para_skus(nome_produto)
        for obj in produtos_disponiveis:
            if obj['SKU'] == sku_produto:
              ingredientes = obj['Ingrediente']
              quantidade_produto *= obj['Quantidade na Receita']
              sobra = obj['Quantidade em Estoque'] - quantidade_produto
              if sobra > 0 :
                  texto += f"- {nome_produto}: {ingredientes} - {quantidade_produto:.2f} unidades (Sobra: {sobra:.2f} unidades)\n"
              else:
                  texto += f"- {nome_produto}: quantidade insuficiente em estoque (Necessário: {quantidade_produto:.2f} unidades, Estoque: {obj['Quantidade em Estoque']:.2f} unidades)\n"

    return f"""
Matéria-prima necessária para {texto_data}:

{texto}
"""

@dspy_tool('PRODUCAO')
def tool_previsao_vendas_por_periodo(periodo: str, data: str = "hoje", setor: str = "") -> str:
    """Consulta a previsão de vendas/produção separada por PERÍODO DO DIA (manhã, tarde, noite).

    USE esta ferramenta SOMENTE quando o usuário mencionar um período do dia ou pedir a
    divisão por período. Exemplos:
    - "quanto de pão francês amanhã de manhã?"  -> periodo="manhã"
    - "previsão de hoje à tarde e à noite"      -> periodo="tarde e noite"
    - "previsão do dia todo, por período"       -> periodo="dia todo"
    - "quanto produzir em cada período hoje?"   -> periodo="cada período"

    NÃO USE esta ferramenta se o usuário informar apenas data ou setor, sem nenhuma
    referência a período do dia. Nesse caso, use a ferramenta de previsão sem período.

    Parâmetros:
    - periodo (OBRIGATÓRIO): o período exatamente como o usuário disse. Aceita 'manhã', 'tarde',
      'noite', combinações ('manhã e tarde') ou 'dia todo' / 'todos os períodos' / 'cada período'.
      Não converta nem calcule nada, apenas repasse o termo dito.
    - data (opcional): data ou referência de tempo exatamente como o usuário disse, sem calcular.
      Aceita datas numéricas ('20/09/2026'), por extenso ('2 de novembro de 2026'),
      termos relativos ('hoje', 'ontem', 'amanhã', 'depois de amanhã'), contagem de dias
      ('há 2 dias', 'daqui a 5 dias') e dias da semana ('segunda passada', 'próxima sexta').
      Se não especificado, assume 'hoje'.
    - setor (opcional): nome do setor (ex: 'Padaria'). Deixe vazio se não for citado.

    Retorno: lista de produtos já formatada.
    - Se foi pedido UM período: lista simples "- produto: quantidade".
    - Se foi pedido o dia todo ou mais de um período: cada produto com a quantidade de
      cada período (manhã, tarde, noite).
    Apresente ao usuário exatamente no formato retornado, sem somar os períodos entre si.
    """
    # corpo igual ao da versão anterior
    try:
        data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)
        periodos = utils.converter_periodo(periodo)
        dividir_por_periodo = len(periodos) > 1

        por_produto = {}
        for p in periodos:
            df_periodo = services.producao.dataframe_vendas_por_periodo(data_real, p)
            if df_periodo.empty:
                continue

            resultado = services.producao.media_vendas_produtos(df_periodo, setor)
            for item in resultado or []:
                nome, _, qtd = item.partition(":")   # item no formato "pao frances: 10"
                por_produto.setdefault(nome.strip(), {})[p] = qtd.strip()

        label_periodo = "o dia todo (dividido por período)" if len(periodos) == 3 \
            else " e ".join(p.lower() for p in periodos)
        aviso_setor = f" (Setor: {setor})" if setor else ""

        if not por_produto:
            return (f"Não encontrei dados históricos suficientes para projetar a produção "
                    f"{texto_data}, {label_periodo}{aviso_setor}.")

        linhas = [
            f"PREVISÃO DE PRODUÇÃO - {texto_data}, {label_periodo}{aviso_setor}",
            "(Baseado no perfil de demanda projetado para esta data. Quantidades em unidades.)",
            "",
        ]

        for nome, valores in por_produto.items():
            if dividir_por_periodo:
                linhas.append(f"* {nome}")
                for p in periodos:
                    linhas.append(f"   - {p.lower()}: {valores.get(p, '0')}")
            else:
                linhas.append(f"- {nome}: {valores.get(periodos[0], '0')}")

        return "\n".join(linhas)

    except Exception as e:
        print(f"[ERRO - tool_previsao_vendas_por_periodo] Falha: {e!r}")
        return "Ocorreu um erro técnico ao cruzar os dados. Informe ao usuário que não foi possível projetar a produção neste momento."