import os
import time
from types import SimpleNamespace

import dspy
from google import genai
from dspy.clients.base_lm import BaseLM
from ia.tools.utils import (
    clima,
    historico_producao_geral,
    historico_producao_por_setor,
    _extrair_setor,
    previsao_producao_geral,
    previsao_producao_por_produto,
    previsao_producao_por_setor,
    produto_por_nome,
    produtos,
    somar,
    subtrair,
)
from ia.procedures import csv_procedures as procedures

GEMINI_API_KEY = os.getenv("GEMINI_API_FATEC1_KEY")
GEMINI_MODEL = "gemini-3.1-flash-lite"
DSPY_DEBUG = os.getenv("DSPY_DEBUG", "1").lower() in {"1", "true", "yes", "on"}

if not GEMINI_API_KEY:
    raise ValueError("A variável GEMINI_API_FATEC1_KEY não foi encontrada no ambiente do sistema!")

class GoogleGenAILM(BaseLM):
    def __init__(self, api_key, model):
        super().__init__(model=model, model_type="chat")
        self.client = genai.Client(api_key=api_key)

    def forward(self, prompt=None, messages=None, **kwargs):
        if messages:
            contents = "\n".join(
                f"{message.get('role', 'user').upper()}: {message.get('content', '')}"
                for message in messages
            )
        else:
            contents = prompt or ""

        config = {}
        if "temperature" in kwargs:
            config["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            config["max_output_tokens"] = kwargs["max_tokens"]

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config or None,
        )

        return SimpleNamespace(
            id=f"gemini-{int(time.time() * 1000)}",
            object="chat.completion",
            created=int(time.time()),
            model=self.model,
            choices=[
                SimpleNamespace(
                    index=0,
                    message=SimpleNamespace(
                        role="assistant",
                        content=response.text or "",
                    ),
                    finish_reason="stop",
                )
            ],
        )

IA_FILTRO = GoogleGenAILM(api_key=GEMINI_API_KEY, model=GEMINI_MODEL)
IA_APRIMORADA = GoogleGenAILM(api_key=GEMINI_API_KEY, model=GEMINI_MODEL)

dspy.configure(lm=IA_FILTRO)

# 1. Filtro inicial
class FiltroDeIntencao(dspy.Signature):
    """Você é um classificador lógico de um sistema de supermercado.
    Sua ÚNICA função é identificar se o assunto faz parte do seu escopo de trabalho.
    Escopos válidos: produção, estoque, planilhas, lucros, desperdício e cálculos matemáticos.
    """
    pergunta = dspy.InputField(desc="Mensagem do usuário.")
    assunto_valido = dspy.OutputField(desc="Responda ESTRITAMENTE com a palavra 'SIM' ou com a palavra 'NAO'. Não escreva mais nada.")

class FormatadorDeResposta(dspy.Signature):
    """Você é um assistente virtual focado na análise de produção do supermercado.
    
    REGRAS ABSOLUTAS:
    1. Responda SEMPRE em Português do Brasil.
    2. Responda APENAS com base no Dado Bruto fornecido.
    3. Se o Dado Bruto contiver uma lista (ex: itens com '•' ou quebras de linha), MANTENHA A LISTA INTACTA na sua resposta, linha por linha. Nunca junte itens de uma lista no mesmo parágrafo.
    4. Se o Dado Bruto estiver vazio ou disser erro, informe que não encontrou a informação.
    5. Seja claro e amigável.
    """
    pergunta_original = dspy.InputField()
    dado_bruto = dspy.InputField(desc="Resultado numérico ou extração da ferramenta. Se for uma lista, ela possui quebras de linha '\\n' que devem ser mantidas.")
    resposta_final = dspy.OutputField(desc="A resposta final, mantendo a formatação de lista do Dado Bruto intacta.")

class ClassificarPedidoDeProducao(dspy.Signature):
    """Classifique o pedido do cliente sobre produção do supermercado.

    Retorne apenas JSON válido com as chaves:
    - acao: 'historico_setor', 'historico_produto', 'previsao_setor', 'previsao_produto', 'consulta_geral', 'fora_do_escopo'
    - setor: nome do setor ou 'Geral' quando não for específico
    - produto: nome do produto quando for específico, ou ''
    - data: data no formato dd/mm/yyyy ou 'hoje' quando não foi informada
    """
    mensagem = dspy.InputField(desc="Mensagem do cliente em linguagem natural.")
    resposta = dspy.OutputField(desc="JSON válido com a intencão do cliente.")

# 2. Agentes
agente_filtro = dspy.Predict(FiltroDeIntencao)
agente_comunicador = dspy.Predict(FormatadorDeResposta)
agente_intencao_producao = dspy.Predict(ClassificarPedidoDeProducao)
agente_trabalhador = dspy.ReAct("pergunta: str -> dado_bruto_da_ferramenta: str", 
                                tools=[
                                    somar, subtrair, clima, produtos, produto_por_nome,
                                    historico_producao_por_setor, historico_producao_geral,
                                    previsao_producao_por_setor, previsao_producao_por_produto, previsao_producao_geral,
                                    procedures.vendas.buscar_por_nome_produto, procedures.vendas.buscar_por_periodo,
                                    procedures.descarte.buscar_por_produto, procedures.produtos.buscar_por_nome_produto,
                                ])

def imprimir_trace_dspy():
    if DSPY_DEBUG:
        print("\n===== TRACE DSPY =====")
        dspy.inspect_history(n=1)
        print("===== FIM TRACE DSPY =====\n")

def _eh_pedido_de_producao(texto_usuario):
    texto = (texto_usuario or "").lower()

    historico_terms = [
        "foram feitos", "foram produzidos", "ja foram feitos", "já foram feitos",
        "já foi produzido", "ja foi produzido", "quantos foram produzidos", "quanto foi produzido",
        "quantidade produzida", "o que foi produzido", "produtos que foram feitos", "feitos totais",
        "produzidos totais", "total produzido", "produzidos no setor", "foram feitos no setor",
        "já produzidos", "quantos produtos foram feitos", "quero saber os produtos que foram feitos",
        "o que já foi produzido", "já produzidos no setor", "total de produtos feitos",
        "total de produtos produzidos"
    ]

    if any(termo in texto for termo in historico_terms):
        return False

    termos = [
        "produzir", "produção", "producao", "produca", "quantos produzir", "quanto produzir",
        "estimativa de producao", "estimativa de produção", "o que cada setor deve produzir",
        "setor deve produzir", "precisa produzir", "deve produzir", "meta de producao",
        "meta de produção", "quanto é para produzir", "quero saber o que", "previsao de producao",
        "previsão de produção", "quantidade para produzir", "quantidade a produzir"
    ]
    return any(termo in texto for termo in termos)


def _eh_pedido_historico_producao(texto_usuario):
    texto = (texto_usuario or "").lower()
    termos_historicos = [
        "foram feitos", "foram produzidos", "ja foram feitos", "já foram feitos",
        "já foi produzido", "ja foi produzido", "quantos foram produzidos", "quanto foi produzido",
        "quantidade produzida", "o que foi produzido", "produtos que foram feitos", "feitos totais",
        "produzidos totais", "total produzido", "produzidos no setor", "foram feitos no setor",
        "já produzidos", "quantos produtos foram feitos", "quero saber os produtos que foram feitos",
        "o que já foi produzido", "já produzidos no setor", "total de produtos feitos",
        "total de produtos produzidos"
    ]
    return any(termo in texto for termo in termos_historicos)


def processar_mensagem(texto_usuario):
    print("[DEBUG] Processando resposta...")

    if _eh_pedido_historico_producao(texto_usuario):
        setor = _extrair_setor(texto_usuario)
        if setor:
            return historico_producao_por_setor(setor=setor)
        return historico_producao_geral()

    if not _eh_pedido_de_producao(texto_usuario):
        with dspy.context(lm=IA_APRIMORADA):
            resultado = agente_trabalhador(pergunta=texto_usuario)
            imprimir_trace_dspy()
            texto_final = agente_comunicador(
                pergunta_original=texto_usuario,
                dado_bruto=resultado.dado_bruto_da_ferramenta,
            )
            imprimir_trace_dspy()
            return texto_final.resposta_final

    try:
        with dspy.context(lm=IA_APRIMORADA):
            intencao = agente_intencao_producao(mensagem=texto_usuario)
            intencao_json = intencao.resposta.strip()
            if intencao_json.startswith("```"):
                intencao_json = intencao_json.strip("` ")
            import json
            dados_intencao = json.loads(intencao_json)

            if dados_intencao.get("acao") == "previsao_setor":
                setor = dados_intencao.get("setor", "Geral")
                if str(setor).strip().lower() in {"geral", "todos", "todos os setores"}:
                    setor = None
                data = dados_intencao.get("data", "hoje")
                return previsao_producao_por_setor(setor=setor, data=data)

            if dados_intencao.get("acao") == "historico_setor":
                setor = dados_intencao.get("setor") or _extrair_setor(texto_usuario)
                if setor:
                    return historico_producao_por_setor(setor=setor)
                return historico_producao_geral()

            if dados_intencao.get("acao") == "historico_produto":
                produto = dados_intencao.get("produto") or ""
                if produto:
                    return historico_producao_geral()
                return historico_producao_geral()

            if dados_intencao.get("acao") == "previsao_produto":
                produto = dados_intencao.get("produto", "")
                data = dados_intencao.get("data", "hoje")
                if not produto:
                    return "Não consegui identificar qual produto você quer estimar. Me diga o nome do produto ou o setor."
                return previsao_producao_por_produto(produto=produto, data=data)

            if dados_intencao.get("acao") == "consulta_geral":
                return previsao_producao_geral(data=dados_intencao.get("data", "hoje"))

            resultado = agente_trabalhador(pergunta=texto_usuario)
            imprimir_trace_dspy()
            texto_final = agente_comunicador(
                pergunta_original=texto_usuario,
                dado_bruto=resultado.dado_bruto_da_ferramenta,
            )
            imprimir_trace_dspy()
            return texto_final.resposta_final
    except Exception as exc:
        print(f"[WARN] Falha na classificação DSPy: {exc}")
        with dspy.context(lm=IA_APRIMORADA):
            resultado = agente_trabalhador(pergunta=texto_usuario)
            imprimir_trace_dspy()
            texto_final = agente_comunicador(
                pergunta_original=texto_usuario,
                dado_bruto=resultado.dado_bruto_da_ferramenta,
            )
            imprimir_trace_dspy()
            return texto_final.resposta_final