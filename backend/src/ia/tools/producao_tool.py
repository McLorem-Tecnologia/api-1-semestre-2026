# Funções para estimativa de produção.
# Função para TOOLS do DSPY relacionadas a produção.
import math
import sys
from pathlib import Path
import pandas as pd
from ia.procedures import procedures
from ia.tools.utils import dspy_tool
import traceback

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ia.procedures import procedures
from ia.tools.utils import classificar_dia


def media_vendas_produtos(vendas, setor=None):
    """
    Calcula a média de vendas de cada produto e arredonda o resultado
    para cima.

    Args:
        vendas (list): Lista de vendas no formato de registros
            de um DataFrame do pandas.
        setor (str, opcional): Setor utilizado para filtrar os produtos.
            Se não for informado, calcula a média de todos os produtos.

    Returns:
        list: Lista contendo o nome de cada produto e sua média
            de vendas arredondada para cima.

            Exemplo:
            ['Brigadeiro: 4', 'Temaki: 7', 'Pão Francês: 4']
    """

    dados = pd.DataFrame(vendas)

    if setor is not None:
        produtos_setor = procedures.produtos.buscar_por_setor(setor)

        nomes_produtos = [
            produto["Produto"]
            for produto in produtos_setor
        ]

        dados = dados[
            dados["Produto"].isin(nomes_produtos)
        ]

    medias = dados.groupby("Produto")["Qtd"].mean()

    resultado = []

    for produto, media in medias.items():
        media_arredondada = math.ceil(media)

        resultado.append(
            f"{produto}: {media_arredondada}"
        )

    return resultado


@dspy_tool
def producao_dia_pelo_setor(data: str, setor: str) -> str:
    """Calcula a produção total de um setor em uma data específica.
    A produção é a soma das vendas com o descarte.
    REGRA ABSOLUTA: Retorne a lista EXATAMENTE no formato que esta ferramenta gerar. Se ocorrer um erro, mostre o erro técnico exato ao usuário.
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
def tool_realocacao_sobra_mp(data="amanhã", setor_origem="") -> str:
    """
    US-11: Realocação de sobras de matéria-prima entre setores para otimizar o uso dos insumos.
    US-12: Sugestão de trensferência de matéria-prima entre setores para reduzir desperdício e atender à demanda.
    
    Calcula sobras de matéria-prima após a produção prevista e recomenda transferências.

    A sobra por setor é o estoque atual menos a necessidade prevista do dia.
    Recomenda transferir a sobra disponível de um setor para outro que tenha
    déficit do mesmo ingrediente. Não altera os estoques registrados.

    - data (opcional): data ou referência relativa para a previsão. Assume amanhã.
    - setor_origem (opcional): limita a busca de sobra a esse setor. Se vazio,
      considera todos os setores.
    """
    data_real, setor_origem, texto_data = _tratar_parametros_iniciais(
        data,
        setor_origem,
    )
    historico = services.producao.dataframe_vendas_similares(data_real)
    if historico.empty:
        return f"Não encontrei histórico compatível para calcular as sobras de {texto_data}."

    necessidades, produtos_sem_receita = _calcular_necessidades_mp(historico)
    if not necessidades:
        return "Não encontrei receitas cadastradas para calcular a necessidade de matéria-prima."

    linhas = []
    encontrou_transferencia = False
    for nome_ingrediente, necessidade in necessidades.items():
        unidade = necessidade["unidade"]
        necessidade_por_setor = necessidade["por_setor"]
        estoque_por_setor = {}
        for registro in procedures.ingredientes.consultar_estoque_por_ingrediente(
            nome_ingrediente
        ):
            nome_setor = registro["Setor"]
            estoque_por_setor[nome_setor] = (
                estoque_por_setor.get(nome_setor, 0.0)
                + float(registro["Estoque Atual"])
            )

        setores = list(dict.fromkeys([*necessidade_por_setor, *estoque_por_setor]))
        saldos = {
            nome_setor: (
                estoque_por_setor.get(nome_setor, 0.0)
                - necessidade_por_setor.get(nome_setor, 0.0)
            )
            for nome_setor in setores
        }
        fontes = [
            nome_setor
            for nome_setor, saldo in saldos.items()
            if saldo > 0
            and (not setor_origem or nome_setor == setor_origem)
        ]
        destinos = [
            nome_setor
            for nome_setor, saldo in saldos.items()
            if saldo < 0
        ]
        sobras_disponiveis = {nome_setor: saldos[nome_setor] for nome_setor in fontes}
        faltas_restantes = {
            nome_setor: -saldos[nome_setor] for nome_setor in destinos
        }
        transferencias = []

        for setor_destino, falta in faltas_restantes.items():
            restante = falta
            for setor_fonte in fontes:
                sobra = sobras_disponiveis[setor_fonte]
                if setor_fonte == setor_destino or sobra <= 0 or restante <= 0:
                    continue
                quantidade_transferir = min(sobra, restante)
                transferencias.append(
                    (setor_fonte, setor_destino, quantidade_transferir)
                )
                sobras_disponiveis[setor_fonte] -= quantidade_transferir
                restante -= quantidade_transferir
            faltas_restantes[setor_destino] = restante

        linhas.append(f"- {nome_ingrediente} ({unidade}):")
        for nome_setor in setores:
            estoque = estoque_por_setor.get(nome_setor, 0.0)
            necessidade_setor = necessidade_por_setor.get(nome_setor, 0.0)
            saldo = saldos[nome_setor]
            descricao_saldo = (
                f"sobra de {saldo:.2f} {unidade}"
                if saldo > 0
                else f"falta de {-saldo:.2f} {unidade}"
                if saldo < 0
                else "sem sobra ou falta"
            )
            linhas.append(
                f"  {nome_setor}: estoque {estoque:.2f} {unidade} - "
                f"necessidade {necessidade_setor:.2f} {unidade} = {descricao_saldo}."
            )

        if transferencias:
            encontrou_transferencia = True
            for setor_fonte, setor_destino, quantidade in transferencias:
                sobra_fonte = saldos[setor_fonte]
                falta_destino = -saldos[setor_destino]
                falta_apos_transferencia = max(falta_destino - quantidade, 0.0)
                linhas.append(
                    f"  Recomendo transferir {quantidade:.2f} {unidade} de "
                    f"{setor_fonte} para {setor_destino}. Justificativa: "
                    f"{setor_fonte} tem sobra de {sobra_fonte:.2f} {unidade} "
                    f"após cobrir sua necessidade prevista, enquanto "
                    f"{setor_destino} tem falta de {falta_destino:.2f} {unidade}. "
                    f"A transferência usa parte dessa sobra sem deixar "
                    f"{setor_fonte} abaixo da própria necessidade e reduz a falta "
                    f"de {setor_destino} para {falta_apos_transferencia:.2f} {unidade}."
                )
        elif destinos:
            linhas.append(
                "  Não há sobra disponível nos setores selecionados para cobrir "
                "as faltas."
            )

        for nome_setor, falta_restante in faltas_restantes.items():
            if falta_restante > 0 and transferencias:
                linhas.append(
                    f"  Após as transferências sugeridas, ainda faltam "
                    f"{falta_restante:.2f} {unidade} em {nome_setor}."
                )

        sobras_apos_transferencias = [
            f"{nome_setor}: {sobra:.2f} {unidade}"
            for nome_setor, sobra in sobras_disponiveis.items()
            if sobra > 0 and transferencias
        ]
        if sobras_apos_transferencias:
            linhas.append(
                "  Sobra não utilizada após as sugestões: "
                + "; ".join(sobras_apos_transferencias)
                + "."
            )

    if produtos_sem_receita:
        linhas.append(
            "Aviso: sem receita cadastrada para "
            f"{', '.join(sorted(produtos_sem_receita))}; a análise pode estar incompleta."
        )
    if not encontrou_transferencia:
        linhas.append("Nenhuma transferência de matéria-prima foi recomendada.")

    filtro_origem = (
        f" considerando sobras do setor {setor_origem}"
        if setor_origem
        else ""
    )
    return (
        f"Análise de sobras e transferências para {texto_data}{filtro_origem} "
        "(não alterei os estoques):\n\n"
        + "\n".join(linhas)
    )

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