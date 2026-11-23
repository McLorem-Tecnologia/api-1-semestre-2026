import math

from ia import procedures, services, utils
from ia.tools import dspy_tool


TOLERANCIA_SALDO = 0.01


def _tratar_parametros_iniciais(data: str, setor: str):
    """Normaliza data e setor e prepara o texto que identifica o período."""
    data_limpa = (
        str(data)
        if data and str(data).strip().lower() not in {"none", "null"}
        else "hoje"
    )
    data_real = utils.converter_data_relativa(data_limpa)
    setor_limpo = utils.normalizar_setor(setor) if setor else ""
    termo = data_limpa.strip().lower()
    if termo in {"hoje", "hj", "ontem", "anteontem", "amanhã", "amanha"} or "dias" in termo:
        texto_data = f"{termo} ({data_real})"
    else:
        texto_data = f"no dia {data_real}"
    return data_real, setor_limpo, texto_data


def _contexto_planejamento_dia(data_real: str) -> str:
    """Descreve os fatores de calendário usados na previsão do dia."""
    perfil = utils.perfil_do_dia(data_real)
    tags = [f"clima {perfil['clima'].lower()}", perfil["fase_financeira"].lower()]
    if perfil["eh_feriado"]:
        tags.append("feriado")
    elif perfil["eh_vespera"]:
        tags.append("véspera de feriado")
    return ", ".join(tags)


def _quantidade_numerica(valor) -> float:
    return float(str(valor).strip().replace(",", "."))


def _calcular_necessidades_mp(historico):
    """Calcula necessidade por ingrediente e setor usando a previsão oficial."""
    necessidades = {}
    produtos_sem_receita = set()
    previsao_produtos = services.producao.media_vendas_produtos(historico, "")
    if not previsao_produtos:
        return necessidades, produtos_sem_receita

    nomes_por_sku = procedures.produtos.obter_dicionario_sku_nome()
    sku_por_nome = {nome: int(sku) for sku, nome in nomes_por_sku.items()}

    for item in previsao_produtos:
        nome_completo, separador, quantidade_texto = item.rpartition(":")
        if not separador:
            continue
        nome_completo = nome_completo.strip()
        quantidade_produto = _quantidade_numerica(quantidade_texto)
        sku = sku_por_nome.get(nome_completo)
        if sku is None:
            sku_texto = procedures.produtos.nome_para_skus(nome_completo)
            if sku_texto != "0000":
                sku = int(sku_texto)
        if sku is None:
            produtos_sem_receita.add(nome_completo)
            continue

        setor_produto = procedures.produtos.setor_do_sku(sku)
        receita = procedures.ingredientes.buscar_receita_por_sku(sku)
        if not receita:
            nome_limpo, separador, unidade_produto = nome_completo.rpartition(" (")
            produtos_sem_receita.add(
                nome_limpo.strip()
                if separador and unidade_produto.endswith(")")
                else nome_completo
            )
            continue

        for registro in receita:
            ingrediente = registro["Ingrediente"]
            unidade = registro.get("Unidade") or registro.get("Unidade de Medida") or "un"
            quantidade_receita = _quantidade_numerica(
                registro.get("Qtd", registro.get("Quantidade", 0))
            )
            quantidade = quantidade_produto * quantidade_receita
            dados = necessidades.setdefault(
                ingrediente,
                {"unidade": unidade, "por_setor": {}},
            )
            por_setor = dados["por_setor"]
            por_setor[setor_produto] = por_setor.get(setor_produto, 0.0) + quantidade

    return necessidades, produtos_sem_receita


def _estoque_por_setor(ingrediente: str):
    estoque = {}
    for registro in procedures.ingredientes.consultar_estoque_por_ingrediente(ingrediente):
        setor = registro["Setor"]
        estoque[setor] = estoque.get(setor, 0.0) + _quantidade_numerica(registro["Estoque Atual"])
    return estoque


@dspy_tool("MATERIA_PRIMA")
def tool_previsao_quantidade_mp(data: str = "hoje", setor: str = "") -> str:
    """Calcula quanto de cada ingrediente precisa ser separado para a produção prevista.

    Use quando a pergunta pedir quantidade ou necessidade de matéria-prima para preparar,
    deixar pronta ou separar para uma data ou setor. Exemplos: "Quanta matéria-prima
    preciso para amanhã na cozinha?" e "Quanto de farinha preciso para amanhã?".
    Não use para listar sobras disponíveis ou recomendar transferência entre setores.
    """
    try:
        data_real, setor, texto_data = _tratar_parametros_iniciais(data, setor)
        historico = services.producao.dataframe_vendas_similares(data_real)
        if historico.empty:
            return f"Não encontrei histórico compatível para calcular a matéria-prima de {texto_data}."

        necessidades, produtos_sem_receita = _calcular_necessidades_mp(historico)
        if not necessidades:
            return f"Não encontrei receitas cadastradas para calcular a matéria-prima de {texto_data}."

        contexto = _contexto_planejamento_dia(data_real)
        linhas = []
        for ingrediente, dados in necessidades.items():
            unidade = dados["unidade"]
            necessidade_setor = dados["por_setor"]
            if setor and necessidade_setor.get(setor, 0.0) <= TOLERANCIA_SALDO:
                continue

            estoque_setor = _estoque_por_setor(ingrediente)
            setores = [setor] if setor else list(dict.fromkeys([*necessidade_setor, *estoque_setor]))
            if setor and setor not in setores:
                setores.append(setor)

            detalhes = []
            for nome_setor in setores:
                necessario = necessidade_setor.get(nome_setor, 0.0)
                if setor and necessario <= TOLERANCIA_SALDO:
                    continue
                estoque = estoque_setor.get(nome_setor, 0.0)
                saldo = estoque - necessario
                if saldo > TOLERANCIA_SALDO:
                    situacao = f"sobra de {saldo:.2f} {unidade}"
                elif saldo < -TOLERANCIA_SALDO:
                    situacao = f"faltam {-saldo:.2f} {unidade}"
                else:
                    situacao = "estoque equilibrado com a necessidade"
                detalhes.append(
                    f"{nome_setor}: necessário {necessario:.2f} {unidade}, "
                    f"estoque {estoque:.2f} {unidade} ({situacao})"
                )
            if detalhes:
                linhas.append(f"- {ingrediente} ({unidade}): " + "; ".join(detalhes))

        if produtos_sem_receita:
            linhas.append(
                "Produtos sem receita cadastrada: "
                + ", ".join(sorted(produtos_sem_receita))
                + "."
            )
        if not linhas:
            return f"Não encontrei matérias-primas previstas para {texto_data} no setor {setor}."

        escopo = f"no setor {setor}" if setor else "em todos os setores"
        return (
            f"Necessidade prevista de matéria-prima para {texto_data}, {escopo} "
            f"(contexto: {contexto}; os estoques não foram alterados):\n\n"
            + "\n".join(linhas)
        )
    except (KeyError, TypeError, ValueError) as erro:
        if str(erro).startswith("Data inválida"):
            return f"{erro}. Informe uma data válida, por exemplo 20/09/2026."
        return "Não foi possível calcular a matéria-prima: há valores inválidos nos dados."
    except Exception as erro:
        print(f"[ERRO - tool_previsao_quantidade_mp] Falha: {erro!r}")
        return "Ocorreu um erro técnico ao calcular a matéria-prima necessária."


@dspy_tool("MATERIA_PRIMA")
def tool_realocacao_sobra_mp(data: str = "amanhã", setor_origem: str = "") -> str:
    """Lista sobras disponíveis e recomenda transferências entre setores.

    Use quando a pergunta pedir quais matérias-primas estão sobrando/disponíveis ou
    o que pode ser transferido de um setor para cobrir falta em outro. Não use quando
    a pergunta pedir quanto de ingrediente deve ser separado para a produção prevista;
    nesse caso, use tool_previsao_quantidade_mp. Esta ferramenta não altera os estoques.
    """
    try:
        data_real, setor_origem, texto_data = _tratar_parametros_iniciais(data, setor_origem)
        historico = services.producao.dataframe_vendas_similares(data_real)
        if historico.empty:
            return f"Não encontrei histórico compatível para calcular as sobras de {texto_data}."

        necessidades, produtos_sem_receita = _calcular_necessidades_mp(historico)
        if not necessidades:
            return "Não encontrei receitas cadastradas para calcular a necessidade de matéria-prima."

        contexto = _contexto_planejamento_dia(data_real)
        sobras_por_setor = {}
        transferencias = []
        faltas_restantes = {}
        encontrou_disponibilidade = False

        for ingrediente, dados in necessidades.items():
            unidade = dados["unidade"]
            necessidade_setor = dados["por_setor"]
            estoque_setor = _estoque_por_setor(ingrediente)
            setores = list(dict.fromkeys([*necessidade_setor, *estoque_setor]))
            saldos = {
                nome: round(estoque_setor.get(nome, 0.0) - necessidade_setor.get(nome, 0.0), 4)
                for nome in setores
            }
            fontes = [
                nome for nome, saldo in saldos.items()
                if saldo > TOLERANCIA_SALDO and (not setor_origem or nome == setor_origem)
            ]
            destinos = [nome for nome, saldo in saldos.items() if saldo < -TOLERANCIA_SALDO]
            sobras_disponiveis = {nome: saldos[nome] for nome in fontes}
            faltas = {nome: -saldos[nome] for nome in destinos}

            for fonte, quantidade in sobras_disponiveis.items():
                sobras_por_setor.setdefault(fonte, []).append(
                    f"{ingrediente}: {quantidade:.2f} {unidade}"
                )
                encontrou_disponibilidade = True

            for destino, falta in faltas.items():
                restante = falta
                for fonte in fontes:
                    sobra = sobras_disponiveis[fonte]
                    if fonte == destino or sobra <= TOLERANCIA_SALDO or restante <= TOLERANCIA_SALDO:
                        continue
                    quantidade = min(sobra, restante)
                    transferencias.append((ingrediente, unidade, fonte, destino, quantidade))
                    sobras_disponiveis[fonte] -= quantidade
                    restante -= quantidade
                faltas_restantes[(ingrediente, destino)] = restante

        linhas = []
        if sobras_por_setor:
            linhas.append("Sobras disponíveis após reservar a necessidade prevista:")
            for nome_setor, itens in sobras_por_setor.items():
                linhas.append(f"- {nome_setor}: " + "; ".join(itens))
        else:
            linhas.append("Nenhuma sobra disponível para transferência.")

        if transferencias:
            linhas.append("\nTransferências recomendadas:")
            for ingrediente, unidade, fonte, destino, quantidade in transferencias:
                # Recalcula os dados do ingrediente para justificar a recomendação.
                dados = necessidades[ingrediente]
                estoque_setor = _estoque_por_setor(ingrediente)
                necessidade_setor = dados["por_setor"]
                sobra_origem = estoque_setor.get(fonte, 0.0) - necessidade_setor.get(fonte, 0.0)
                falta_destino = necessidade_setor.get(destino, 0.0) - estoque_setor.get(destino, 0.0)
                falta_restante = faltas_restantes.get((ingrediente, destino), 0.0)
                linhas.append(
                    f"- {ingrediente}: transferir {quantidade:.2f} {unidade} de {fonte} para {destino}; "
                    f"a origem mantém {necessidade_setor.get(fonte, 0.0):.2f} {unidade} reservados "
                    f"e ainda tem sobra de {sobra_origem:.2f} {unidade}; o destino tinha falta de "
                    f"{falta_destino:.2f} {unidade}; após a transferência, a falta será "
                    f"{max(falta_restante, 0.0):.2f} {unidade} ({contexto})."
                )
        if produtos_sem_receita:
            linhas.append(
                "Aviso: sem receita cadastrada para "
                + ", ".join(sorted(produtos_sem_receita))
                + "; a análise pode estar incompleta."
            )
        if not encontrou_disponibilidade:
            linhas.append("Nenhuma transferência foi recomendada porque não há sobra disponível para cobrir déficit compatível.")
        elif not transferencias:
            linhas.append("Nenhuma transferência foi recomendada porque nenhum setor apresenta falta compatível no período.")

        filtro = f" considerando sobras do setor {setor_origem}" if setor_origem else ""
        resposta = (
            f"Análise de sobras e transferências de matéria-prima para {texto_data}{filtro} "
            f"(contexto: {contexto}; não alterei os estoques):\n\n" + "\n".join(linhas)
        )
        if len(resposta) > 4096:
            return "A análise de matéria-prima excede o limite de uma mensagem do Telegram. Aplique um filtro de setor para reduzir a resposta."
        return resposta
    except (KeyError, TypeError, ValueError) as erro:
        if str(erro).startswith("Data inválida"):
            return f"{erro}. Informe uma data válida, por exemplo 20/09/2026."
        return "Não foi possível analisar as sobras de matéria-prima: há valores inválidos nos dados."
    except Exception as erro:
        print(f"[ERRO - tool_realocacao_sobra_mp] Falha: {erro!r}")
        return "Ocorreu um erro técnico ao analisar as sobras de matéria-prima."
