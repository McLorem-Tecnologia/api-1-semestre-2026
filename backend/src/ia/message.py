import dspy
import re
import unicodedata
from dspy.utils.exceptions import AdapterParseError
from ia import procedures
from ia.config import IA_APRIMORADA 
from ia.agentes import agente_roteador, agente_relacional, agente_redator, AgenteAnalista
from ia.tools.desperdicio_tool import tool_buscar_por_intervalo


def _normalizar_texto(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(caractere for caractere in texto if not unicodedata.combining(caractere))


def _resposta_de_produtos_solicitados(pergunta: str, previsao: str) -> str | None:
    pergunta_normalizada = _normalizar_texto(pergunta)
    nomes = procedures.produtos.obter_dicionario_sku_nome().values()
    produtos_solicitados = []
    for nome_com_unidade in sorted(nomes, key=len, reverse=True):
        nome = nome_com_unidade.rpartition(" (")[0]
        nome_normalizado = _normalizar_texto(nome)
        if nome_normalizado and nome_normalizado in pergunta_normalizada:
            produtos_solicitados.append(nome_normalizado)
    if not produtos_solicitados:
        return None

    linhas = previsao.splitlines()
    separador = next((indice for indice, linha in enumerate(linhas) if not linha.strip()), len(linhas))
    cabecalho = [linha for linha in linhas[:separador] if linha.strip()]
    selecionadas = {}
    setor_atual = ""
    for linha in linhas[separador + 1:]:
        if linha.strip().startswith("<b>"):
            setor_atual = linha.strip()
        correspondencia = re.match(r"^\s*\d+\.\s*(.+?):\s*(.+)$", linha)
        if correspondencia:
            nome_produto = _normalizar_texto(correspondencia.group(1))
            if any(nome_produto == nome for nome in produtos_solicitados):
                selecionadas.setdefault(setor_atual, []).append(
                    f"{correspondencia.group(1)}: {correspondencia.group(2)}"
                )
    if not selecionadas:
        return None
    linhas_resposta = list(cabecalho)
    for setor, produtos in selecionadas.items():
        if setor:
            linhas_resposta.append(setor)
        linhas_resposta.extend(f"{indice}. {produto}" for indice, produto in enumerate(produtos, start=1))
    return "\n".join(linhas_resposta)


def _resposta_descarte_por_setor(pergunta: str) -> str | None:
    pergunta_normalizada = _normalizar_texto(pergunta)
    solicita_setores = (
        "cada setor" in pergunta_normalizada
        or "por setor" in pergunta_normalizada
        or "por setores" in pergunta_normalizada
        or "separe por setor" in pergunta_normalizada
        or "separe por setores" in pergunta_normalizada
    )
    if not solicita_setores:
        return None

    datas = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b", pergunta)
    if len(datas) > 1:
        return None
    data = datas[0] if datas else next(
        (termo for termo in ("ontem", "hoje", "amanhã", "amanha") if termo in pergunta_normalizada),
        "hoje",
    )
    setores = procedures.produtos.prod_tb["Setor"].dropna().drop_duplicates().tolist()
    resultados = []
    total = 0.0
    for setor in setores:
        resposta = str(tool_buscar_por_intervalo(data_inicio=data, setor=str(setor)))
        valor = re.search(r"R\$\s*([\d.,]+)", resposta)
        if not valor:
            return None
        quantidade = float(valor.group(1).replace(",", "."))
        total += quantidade
        resultados.append(f"• <b>{setor}</b>: R$ {quantidade:.2f}")
    texto_data = re.search(r"no dia \d{2}/\d{2}/\d{4}|\w+ \(\d{2}/\d{2}/\d{4}\)", resposta)
    periodo = texto_data.group(0) if texto_data else "no período solicitado"
    return (
        f"Custo total do desperdício por setor {periodo}:\n"
        + "\n".join(resultados)
        + f"\n• <b>Total geral</b>: R$ {total:.2f}"
    )

def processar_mensagem(texto_usuario: str) -> str:
    """Recebe a mensagem do Telegram e orquestra a resposta da IA."""
    
    try:
        with dspy.context(lm=IA_APRIMORADA):
            
            analise = agente_roteador(pergunta=texto_usuario)
            categoria = str(analise.categoria).strip().upper()
            
            if "SAUDACAO" in categoria:
                resposta = agente_relacional(mensagem=texto_usuario)
                return resposta.resposta
                
            elif "INVALIDO" in categoria:
                return "Desculpe, Meu sistema é restrito à análise e produção do supermercado."
            else:
                if "DESPERDICIO" in categoria:
                    resposta_setores = _resposta_descarte_por_setor(texto_usuario)
                    if resposta_setores:
                        return resposta_setores

                analista = AgenteAnalista(categoria)
                resultado = analista(pergunta=texto_usuario)
                
                dspy.inspect_history(n=1) 

                # Em matéria-prima, preserve a lista calculada integralmente.
                # O redator pode omitir ingredientes em respostas longas.
                if categoria == "MATERIA_PRIMA":
                    return str(resultado.dado_calculado)

                if categoria == "PRODUCAO":
                    resposta_filtrada = _resposta_de_produtos_solicitados(
                        texto_usuario,
                        str(resultado.dado_calculado),
                    )
                    if resposta_filtrada:
                        return resposta_filtrada
                
                texto_final = agente_redator(
                    mensagem=texto_usuario, 
                    dado_consultado=resultado.dado_calculado
                )
                return re.sub(
                    r"<b\b[^>]*>(.*?)</b\s*>",
                    r"<b>\1</b>",
                    texto_final.resposta_final,
                    flags=re.IGNORECASE | re.DOTALL,
                )

    except AdapterParseError as erro_dspy:
        print(f"[ERRO DSPY] O modelo travou e retornou nulo. Log: {erro_dspy}")
        return "⚠️ Ops! Minha inteligência artificial teve um branco e não conseguiu processar as ferramentas."
        
    except Exception as erro_geral:
        print(f"[ERRO GERAL IA] {erro_geral}")
        return "⚠️ Ocorreu um erro inesperado de conexão com a IA."
