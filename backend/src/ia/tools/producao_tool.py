from ia.tools import dspy_tool
from ia import procedures, services, utils

TODOS_OS_PERIODOS = ['Manhã', 'Tarde', 'Noite']

def _tratar_parametros_iniciais(data: str, setor: str):
    """Trata a data, normaliza o setor e cria aquele texto bonito para a resposta.

    Parâmetros:
        data: data ou referência de tempo como o usuário disse (ex.: 'amanhã', '20/09/2026').
              Vazio, 'none' ou 'null' são tratados como 'hoje'.
        setor: nome do setor, ou vazio para considerar todos.

    Retorna:
        tupla (data_real, setor_limpo, texto_data_amigavel), com a data no formato dd/mm/aaaa.

    Levanta:
        ValueError: se a data não for válida (erro vindo do converter_data_relativa).
    """
    # Valores vazios ou "none"/"null" (que o modelo às vezes manda) viram "hoje"
    data_limpa = str(data) if data and str(data).strip().lower() not in ['none', 'null'] else "hoje"

    data_real = utils.converter_data_relativa(data_limpa)
    setor_limpo = utils.normalizar_setor(setor) if setor else ""

    # Referências relativas mostram o termo e a data real; datas numéricas mostram "no dia ..."
    termo = data_limpa.strip().lower()
    if termo in ['hoje', 'hj', 'ontem', 'anteontem', 'amanhã', 'amanha'] or 'dias' in termo:
        texto_data_amigavel = f"{termo} ({data_real})"
    else:
        texto_data_amigavel = f"no dia {data_real}"

    return data_real, setor_limpo, texto_data_amigavel

def _formatar_lista_produtos(resultado: list) -> str:
    """Organiza os produtos por setor e coloca a unidade junto da quantidade."""
    nomes_por_sku = procedures.produtos.obter_dicionario_sku_nome()
    setores = {}

    for posicao, item in enumerate(resultado, start=1):
        nome_com_unidade, _, quantidade = item.rpartition(":")
        nome_com_unidade = nome_com_unidade.strip()
        nome, separador, unidade = nome_com_unidade.rpartition(" (")
        if separador and unidade.endswith(")"):
            nome = nome.strip()
            unidade = unidade[:-1]
        else:
            nome = nome_com_unidade
            unidade = "un"

        sku = next((sku for sku, nome_produto in nomes_por_sku.items() if nome_produto == nome_com_unidade), None)
        setor = procedures.produtos.setor_do_sku(int(sku)) if sku is not None else "Outros"
        setores.setdefault(setor, []).append(
            f"{posicao}. {nome}: {_formatar_quantidade(quantidade.strip(), unidade)}"
        )

    linhas = []
    for setor, produtos in setores.items():
        linhas.append(f"<b>{setor}</b>")
        linhas.extend(produtos)
        linhas.append("")

    return "\n".join(linhas).rstrip()

def _formatar_quantidade(quantidade, unidade: str) -> str:
    try:
        plural = float(str(quantidade).replace(",", ".").strip()) != 1
    except ValueError:
        plural = False

    if unidade.lower() in ["porção", "porcoes"]:
        unidade = "porções" if plural else "porção"
    elif unidade.lower() in ["un", "unidade", "unidades"]:
        unidade = "unidades" if plural else "unidade"

    return f"{quantidade} {unidade}"

def _calcular_previsao_do_dia(data: str, setor: str):
    """Calcula a produção média ideal de cada produto para a data (base das tools de previsão e de meta).

    Parâmetros:
        data: data ou referência de tempo como o usuário disse.
        setor: nome do setor, ou vazio para considerar todos.

    Retorna:
        tupla (previsao_por_produto, setor_limpo, texto_data), onde previsao_por_produto é:
        - None, se não há histórico de dias parecidos com a data;
        - lista vazia, se há histórico mas nenhum produto (ex.: setor sem vendas);
        - lista de textos "Produto: quantidade", nos demais casos.

    Levanta:
        ValueError: se a data não for válida.
    """
    data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)

    # Busca dias do passado com mesmo dia efetivo (feriado/véspera), ciclo financeiro e clima
    vendas_similares = services.producao.dataframe_vendas_similares(data_real)
    if vendas_similares.empty:
        return None, setor, texto_data

    # Enriquecimento opcional do texto_data com o perfil climático/calendário do dia
    perfil = utils.perfil_do_dia(data_real)
    detalhes = [f"clima {perfil['clima'].lower()}", perfil['fase_financeira'].lower()]
    if perfil["eh_feriado"]:
        detalhes.append("feriado")
    elif perfil["eh_vespera"]:
        detalhes.append("véspera de feriado")

    texto_data_enriquecido = f"{texto_data} ({', '.join(detalhes)})"

    # Média de saída de cada produto, já com a margem de produção (+5%)
    previsao_por_produto = services.producao.media_vendas_produtos(vendas_similares, setor)
    return previsao_por_produto, setor, texto_data_enriquecido

@dspy_tool('PRODUCAO')
def tool_previsao_vendas_por_data(data: str = "hoje", setor: str = "") -> str:
    # US-01 e US-02: a resposta traz sempre a quantidade de cada produto
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
        
    REGRA ABSOLUTA: Entregue os dados com foco em AÇÃO. Repasse EXATAMENTE os números retornados.

    Retorna: texto com a lista numerada de produtos e a quantidade de cada um
    ou uma mensagem explicando por que não foi possível calcular (sem histórico, data inválida ou erro nos dados).
    """
    try:
        previsao_por_produto, setor, texto_data = _calcular_previsao_do_dia(data, setor)

        # Sem dias parecidos no histórico, não há como projetar
        if previsao_por_produto is None:
            return f"Não encontrei dados históricos compatíveis para projetar a produção {texto_data}."

        # Há histórico, mas nenhum produto (ex.: setor sem vendas)
        if not previsao_por_produto:
            trecho_setor = f" no setor '{setor}'" if setor else ""
            return f"Não há histórico suficiente para projetar a produção{trecho_setor} {texto_data}."

        aviso_setor = f" (Setor: {setor})" if setor else ""
        texto_resposta = f"PREVISÃO DE PRODUÇÃO: O que DEVE ser produzido {texto_data}{aviso_setor}:\n"
        texto_resposta += "(Baseado no perfil de demanda projetado para esta data)\n\n"

        texto_resposta += _formatar_lista_produtos(previsao_por_produto)
        return texto_resposta

    except KeyError as erro:
        # KeyError do pandas pode vir como 'Column not found: Qtd'; fica só o nome da coluna
        coluna = str(erro.args[0]).replace("Column not found: ", "")
        print(f"[ERRO - tool_previsao_vendas_por_data] Coluna não encontrada nos dados: '{coluna}'")
        return f"Não foi possível projetar a produção: a coluna '{coluna}' não foi encontrada nos arquivos de dados."
    except (ValueError, TypeError) as erro:
        print(f"[ERRO - tool_previsao_vendas_por_data] Valor inválido: {erro!r}")
        # ValueError do converter_data_relativa: a data informada não é válida
        if str(erro).startswith("Data inválida"):
            return f"{erro}. Peça ao usuário para informar a data novamente (ex.: 20/09/2026)."
        return "Não foi possível projetar a produção: há valores inválidos nos dados de vendas."
    except Exception as erro:
        print(f"[ERRO - tool_previsao_vendas_por_data] Falha: {erro!r}")
        return "Ocorreu um erro técnico ao cruzar os dados. Informe ao usuário que não foi possível projetar a produção neste momento."

@dspy_tool('PRODUCAO')
def tool_meta_producao_passada(data: str = "hoje", setor: str = "") -> str:
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

    Retorna: texto com a lista numerada de produtos e a quantidade de cada um
    ou uma mensagem explicando por que não foi possível calcular (sem histórico, data inválida ou erro nos dados).
    """
    try:
        previsao_por_produto, setor, texto_data = _calcular_previsao_do_dia(data, setor)

        # Sem dias parecidos no histórico, não há como auditar a meta
        if previsao_por_produto is None:
            return f"Não encontrei histórico compatível para auditar a meta {texto_data}."

        # Há histórico, mas nenhum produto (ex.: setor sem vendas)
        if not previsao_por_produto:
            trecho_setor = f" no setor '{setor}'" if setor else ""
            return f"Não há dados suficientes para estipular o que deveria ter sido produzido{trecho_setor} {texto_data}."

        aviso_setor = f" (Setor: {setor})" if setor else ""
        texto_resposta = f"RELATÓRIO DE META: O que DEVERIA TER SIDO PRODUZIDO {texto_data}{aviso_setor}:\n"
        texto_resposta += "(Cálculo da meta ideal baseada no perfil histórico do dia)\n\n"

        texto_resposta += _formatar_lista_produtos(previsao_por_produto)
        return texto_resposta

    except KeyError as erro:
        # KeyError do pandas pode vir como 'Column not found: Qtd'; fica só o nome da coluna
        coluna = str(erro.args[0]).replace("Column not found: ", "")
        print(f"[ERRO - tool_meta_producao_passada] Coluna não encontrada nos dados: '{coluna}'")
        return f"Não foi possível calcular a meta: a coluna '{coluna}' não foi encontrada nos arquivos de dados."
    except (ValueError, TypeError) as erro:
        print(f"[ERRO - tool_meta_producao_passada] Valor inválido: {erro!r}")
        # ValueError do converter_data_relativa: a data informada não é válida
        if str(erro).startswith("Data inválida"):
            return f"{erro}. Peça ao usuário para informar a data novamente (ex.: 20/09/2026)."
        return "Não foi possível calcular a meta: há valores inválidos nos dados de vendas."
    except Exception as erro:
        print(f"[ERRO - tool_meta_producao_passada] Falha: {erro!r}")
        return "Ocorreu um erro técnico ao calcular a meta histórica de produção."

@dspy_tool('PRODUCAO')
def tool_producao_por_data(data: str, setor: str = "") -> str:
    # US-03: Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y.
    """Use esta ferramenta EXCLUSIVAMENTE para consultar a PRODUÇÃO REAL (produtividade já executada) em uma data exata.
    Acione-a para responder perguntas como: "O que foi produzido hoje?", "Qual a produtividade da Confeitaria ontem?".
    
    Lógica interna: Soma automaticamente os registros reais de Vendas + Descartes do dia para entregar o total produzido.
    
    Parâmetros:
    - data (obrigatório): data ou referência de tempo exatamente como o usuário disse, sem
      calcular a data. Aceita datas numéricas ('20/09/2026'), por extenso ('2 de novembro de 2026'),
      termos relativos ('hoje', 'ontem', 'amanhã', 'depois de amanhã'), contagem de dias
      ('há 2 dias', 'daqui a 5 dias') e dias da semana ('segunda passada', 'próxima sexta').
      Se o usuário não informar a data, a ferramenta pede que ela seja informada.
    - setor (opcional): nome do setor (ex: 'Padaria'). Se o usuário perguntar o geral, deixe vazio.
    
    REGRA ABSOLUTA PARA A RESPOSTA FINAL: 
    NÃO RESUMA. NÃO ABREVIES. O usuário PRECISA ver a lista de todos os produtos.
    Você DEVE transcrever a tabela inteira gerada por esta ferramenta na sua resposta final, linha por linha.

    Retorna: tabela com a produção, as vendas e o descarte de cada produto
    ou uma mensagem explicando por que não foi possível consultar (sem registros, data inválida ou erro nos dados).
    """
    try:
        if not data or str(data).strip().lower() in ['none', 'null', '']:
            return "Falta a data. Pergunte ao usuário de qual data ele quer saber a produção."

        data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)

        # Produção real de cada produto: vendas + descartes do dia
        producao_por_produto = services.producao.calcular_producao_data(data_real, setor)

        # None indica que o setor não tem produtos cadastrados
        if producao_por_produto is None:
            return f"Nenhum produto encontrado para o setor '{setor}'."

        if not producao_por_produto:
            trecho_setor = f" no setor '{setor}'" if setor else " no panorama geral"
            return f"Não houve registros de produção{trecho_setor} {texto_data}."

        aviso_setor = f" ({setor})" if setor else ""
        cabecalho = f"RELATÓRIO DE PRODUÇÃO REAL: O que FOI PRODUZIDO <b>{texto_data}</b>{aviso_setor}:\n"
        cabecalho += "(Soma real das vendas e descartes registrados)\n\n"

        setores = {}
        nomes_por_sku = procedures.produtos.obter_dicionario_sku_nome()

        for produto, totais in sorted(producao_por_produto.items()):
            nome, separador, unidade = produto.rpartition(" (")
            if separador and unidade.endswith(")"):
                produto = nome.strip()
                unidade = unidade[:-1]
            else:
                unidade = "un"

            sku = next((sku for sku, nome_produto in nomes_por_sku.items()
                        if nome_produto == f"{produto} ({unidade})"), None)
            setor_produto = procedures.produtos.setor_do_sku(int(sku)) if sku is not None else "Outros"
            linha_produto = f"{produto}: {_formatar_quantidade(totais['producao'], unidade)}"
            if totais['descarte'] != 0:
                linha_produto += (
                    f" (Vendas: {totais['vendas']}, Descarte: {totais['descarte']})"
                )
            setores.setdefault(setor_produto, []).append(linha_produto)

        linhas_produtos = []
        posicao_produto = 1
        for setor_produto, produtos in setores.items():
            linhas_produtos.append(f"<b>{setor_produto}</b>")
            for produto in produtos:
                linhas_produtos.append(f"{posicao_produto}. {produto}")
                posicao_produto += 1
            linhas_produtos.append("")

        return cabecalho + "\n".join(linhas_produtos).rstrip()

    except KeyError as erro:
        # KeyError do pandas pode vir como 'Column not found: Qtd'; fica só o nome da coluna
        coluna = str(erro.args[0]).replace("Column not found: ", "")
        print(f"[ERRO - tool_producao_por_data] Coluna não encontrada nos dados: '{coluna}'")
        return f"Não foi possível consultar a produção real: a coluna '{coluna}' não foi encontrada nos arquivos de dados."
    except (ValueError, TypeError) as erro:
        print(f"[ERRO - tool_producao_por_data] Valor inválido: {erro!r}")
        # ValueError do converter_data_relativa: a data informada não é válida
        if str(erro).startswith("Data inválida"):
            return f"{erro}. Peça ao usuário para informar a data novamente (ex.: 20/09/2026)."
        return "Não foi possível consultar a produção real: há valores inválidos nos dados de vendas."
    except Exception as erro:
        print(f"[ERRO - tool_producao_por_data] Falha: {erro!r}")
        return "Ocorreu um erro técnico inesperado ao tentar acessar os dados reais de produção."

@dspy_tool('PRODUCAO')
def tool_previsao_vendas_por_periodo(periodo: str = "", data: str = "hoje", setor: str = "") -> str:
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
    - periodo (opcional): o período exatamente como o usuário disse. Aceita 'manhã', 'tarde',
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
    try:
        data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)

        # Texto de período não reconhecido vira o dia todo; madrugada entra como noite.
        periodos = utils.converter_periodo(periodo)
        dividir_por_periodo = len(periodos) > 1

        # Guarda a quantidade de cada produto por período.
        previsao_por_produto = {}
        for nome_periodo in periodos:
            vendas_do_periodo = services.producao.dataframe_vendas_por_periodo(data_real, nome_periodo)

            # Período sem histórico aparece como zero na resposta.
            if vendas_do_periodo.empty:
                continue

            medias_do_periodo = services.producao.media_vendas_produtos(vendas_do_periodo, setor)
            for item in medias_do_periodo or []:
                # O item chega como texto "Produto: quantidade"; rpartition separa no último ":"
                nome_produto, _, quantidade = item.rpartition(":")
                previsao_por_produto.setdefault(nome_produto.strip(), {})[nome_periodo] = quantidade.strip()

        if len(periodos) == len(TODOS_OS_PERIODOS):
            label_periodo = "o dia todo (dividido por período)"
        else:
            label_periodo = " e ".join(nome.lower() for nome in periodos)
        aviso_setor = f" (Setor: {setor})" if setor else ""

        if not previsao_por_produto:
            return (f"Não encontrei dados históricos suficientes para projetar a produção "
                    f"{texto_data}, {label_periodo}{aviso_setor}.")

        linhas = [
            f"PREVISÃO DE PRODUÇÃO - {texto_data}, {label_periodo}{aviso_setor}",
            "(Baseado no perfil de demanda projetado para esta data.)",
            "",
        ]

        setores_por_produto = {}
        nomes_por_sku = procedures.produtos.obter_dicionario_sku_nome()
        for nome_produto, quantidades in previsao_por_produto.items():
            sku = next((sku for sku, nome in nomes_por_sku.items() if nome == nome_produto), None)
            setor_produto = procedures.produtos.setor_do_sku(int(sku)) if sku is not None else "Outros"
            setores_por_produto.setdefault(setor_produto, []).append((nome_produto, quantidades))

        posicao_produto = 1
        for setor_produto, produtos in setores_por_produto.items():
            linhas.append(f"<b>{setor_produto}</b>")
            for nome_produto, quantidades in produtos:
                nome, separador, unidade = nome_produto.rpartition(" (")
                if separador and unidade.endswith(")"):
                    nome_produto = nome.strip()
                    unidade = unidade[:-1]
                else:
                    unidade = "un"
                if dividir_por_periodo:
                    linhas.append(f"{posicao_produto}. {nome_produto}")
                    for nome_periodo in periodos:
                        qtd_periodo = quantidades.get(nome_periodo, '0')
                        linhas.append(f"   - {nome_periodo.lower()}: {_formatar_quantidade(qtd_periodo, unidade)}")
                else:
                    qtd_periodo = quantidades.get(periodos[0], '0')
                    linhas.append(f"{posicao_produto}. {nome_produto}: {_formatar_quantidade(qtd_periodo, unidade)}")
                posicao_produto += 1
            linhas.append("")

        return "\n".join(linhas)

    except KeyError as erro:
        # KeyError do pandas pode vir como 'Column not found: Qtd'; fica só o nome da coluna
        coluna = str(erro.args[0]).replace("Column not found: ", "")
        print(f"[ERRO - tool_previsao_vendas_por_periodo] Coluna não encontrada nos dados: '{coluna}'")
        return f"Não foi possível projetar a produção: a coluna '{coluna}' não foi encontrada nos arquivos de dados."
    except (ValueError, TypeError) as erro:
        print(f"[ERRO - tool_previsao_vendas_por_periodo] Valor inválido: {erro!r}")
        # ValueError do converter_data_relativa: a data informada não é válida
        if str(erro).startswith("Data inválida"):
            return f"{erro}. Peça ao usuário para informar a data novamente (ex.: 20/09/2026)."
        return "Não foi possível projetar a produção: há valores inválidos nos dados de vendas."
    except Exception as erro:
        print(f"[ERRO - tool_previsao_vendas_por_periodo] Falha: {erro!r}")
        return "Ocorreu um erro técnico ao cruzar os dados. Informe ao usuário que não foi possível projetar a produção neste momento."
