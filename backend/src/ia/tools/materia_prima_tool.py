import math
from ia import utils


def _tratar_parametros_iniciais(data: str, setor: str):
    """Trata a data, normaliza o setor e prepara o texto da resposta."""
    data_limpa = (
        str(data)
        if data and str(data).strip().lower() not in ["none", "null"]
        else "hoje"
    )

    data_real = utils.converter_data_relativa(data_limpa)
    setor_limpo = utils.normalizar_setor(setor) if setor else ""

    termo = data_limpa.strip().lower()
    if termo in ["hoje", "hj", "ontem", "anteontem", "amanhã", "amanha"] or "dias" in termo:
        texto_data_amigavel = f"{termo} ({data_real})"
    else:
        texto_data_amigavel = f"no dia {data_real}"

    return data_real, setor_limpo, texto_data_amigavel


def _calcular_necessidades_mp(historico):
    necessidades = {}
    produtos_sem_receita = set()

    medias = historico.groupby("SKU")["Qtd"].mean()

    for sku, quantidade_media in medias.items():
        quantidade_produto = math.ceil(float(quantidade_media) * 1.05)
        nome_produto = procedures.produtos.nome_do_sku(int(sku))
        setor_produto = procedures.produtos.setor_do_sku(int(sku))
        receita = procedures.ingredientes.buscar_receita_por_sku(int(sku))

        if not receita:
            produtos_sem_receita.add(nome_produto)
            continue

        for item in receita:
            ingrediente = item["Ingrediente"]
            unidade = item["Unidade"]
            quantidade = quantidade_produto * float(item["Qtd"])

            if ingrediente not in necessidades:
                necessidades[ingrediente] = {
                    "unidade": unidade,
                    "por_setor": {}
                }

            por_setor = necessidades[ingrediente]["por_setor"]
            por_setor[setor_produto] = (
                por_setor.get(setor_produto, 0.0) + quantidade
            )

    return necessidades, produtos_sem_receita



@dspy_tool('MATERIA_PRIMA')
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