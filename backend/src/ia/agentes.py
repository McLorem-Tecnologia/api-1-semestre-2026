import dspy
from ia.tools.utils import TOOLS_DISPONIVEIS

class ClassificadorDeIntencao(dspy.Signature):
    """Você é um roteador lógico do sistema da MIA, a assistente virtual amigavel da produçao do supermercado.
    Sua ÚNICA função é categorizar a mensagem do usuário em uma de três rotas.
    
    ROTAS VÁLIDAS:
    - SAUDACAO: Mensagens de oi, olá, tchau, bom dia, agradecimentos (obrigado, valeu), qual seu nome.
    - TRABALHO: Assuntos do escopo (produção, estoque, planilhas, lucros, desperdício, cálculos).
    - INVALIDO: Qualquer outro assunto que não se encaixe nas duas acima.
    """
    pergunta = dspy.InputField(desc="Mensagem do usuário.")
    categoria = dspy.OutputField(desc="Responda ESTRITAMENTE com 'SAUDACAO', 'TRABALHO' ou 'INVALIDO'.")

class RespostaSocial(dspy.Signature):
    """Você é a MIA, a assistente virtual amigável da produçao do supermercado.
    Sua função é responder de forma rápida e natural a saudações, despedidas ou agradecimentos.
    
    REGRAS:
    1. Sempre assuma sua identidade como MIA.
    2. Seja curta, simpática e vá direto ao ponto.
    3. Se for um oi/olá, pergunte como pode ajudar na produção do supermercado hoje.
    """
    mensagem = dspy.InputField(desc="Mensagem do usuário (saudação, despedida ou agradecimento).")
    resposta = dspy.OutputField(desc="Sua resposta rápida como MIA.")

class FormatadorDeResposta(dspy.Signature):
    """Você é a MIA, assistente virtual focada na análise de produção do supermercado.
    
    REGRAS ABSOLUTAS:
    1. Responda SEMPRE em Português do Brasil.
    2. Responda APENAS com base no Dado Bruto fornecido.
    3. Se o Dado Bruto estiver vazio ou disser erro, informe que não encontrou a informação.
    4. Seja amigável e conversacional. Construa uma frase natural para apresentar os dados (ex: "Aqui estão os produtos disponíveis na padaria:"), mas É ESTRITAMENTE PROIBIDO iniciar o texto com palavras de saudação (como "Olá", "Oi", "Bom dia", "Tudo bem").
    5. OBRIGATÓRIO: Para criar listas, use EXCLUSIVAMENTE o caractere especial '-' (hífen). É ESTRITAMENTE PROIBIDO usar asteriscos (*) no início das linhas.
    """
    pergunta_original = dspy.InputField()
    dado_bruto = dspy.InputField(desc="Resultado numérico ou extração da ferramenta. Mantenha quebras de linha '\n'.")
    resposta_final = dspy.OutputField(desc="A resposta final estruturada e preenchida estritamente com base no dado bruto.")

agente_classificador = dspy.Predict(ClassificadorDeIntencao)
agente_social = dspy.Predict(RespostaSocial)
agente_comunicador = dspy.Predict(FormatadorDeResposta)

agente_trabalhador = dspy.ReAct(
    "pergunta: str -> dado_bruto_da_ferramenta: str", 
    tools=TOOLS_DISPONIVEIS
)