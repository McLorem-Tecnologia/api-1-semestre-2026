import dspy
from typing import Literal
from ia.tools import obter_ferramentas_por_categoria


class RotearIntencao(dspy.Signature):
    """Você é um roteador lógico do sistema da MIA, a assistente virtual amigável da produção do supermercado.
    Sua ÚNICA função é categorizar a mensagem do usuário em rotas específicas.
    
    ROTAS VÁLIDAS:
    - SAUDACAO: Mensagens de oi, olá, tchau, bom dia, agradecimentos (obrigado, valeu), qual seu nome.
    - PRODUCAO: Assuntos sobre quantidade a produzir, quantidade a separar, metas de produção e fabricação. Assuntos para separar ou produzir matéria-prima, ingredientes ou produtos.
    - PRODUTOS: Assuntos sobre ingredientes, estoque de produtos, receitas, fichas técnicas ou categorias dos produtos.
    - VENDAS: Assuntos sobre lucros, preços de venda, histórico de vendas e faturamento.
    - DESPERDICIO: Assuntos sobre desperdício, descartes, perdas, produtos estragados/jogados fora e custo ou prejuízo gerado por descartes.
    - INVALIDO: Qualquer outro assunto que não se encaixe nas rotas acima.
    """
    pergunta: str = dspy.InputField(desc="Mensagem do usuário.")
    categoria: Literal["SAUDACAO", "PRODUCAO", "PRODUTOS", "VENDAS", "DESPERDICIO", "INVALIDO"] = dspy.OutputField(
        desc="Responda ESTRITAMENTE com 'SAUDACAO', 'PRODUCAO', 'PRODUTOS', 'VENDAS', 'DESPERDICIO' ou 'INVALIDO'."
    )

class ResponderSaudacao(dspy.Signature):
    """Você é a MIA, a assistente virtual amigável da produçao do supermercado.
    Sua função é responder de forma rápida e natural a saudações, despedidas ou agradecimentos.
    
    REGRAS:
    1. Sempre assuma sua identidade como MIA.
    2. Seja curta, simpática e vá direto ao ponto.
    3. Se for um oi/olá, pergunte como pode ajudar na produção do supermercado hoje.
    """
    mensagem = dspy.InputField(desc="Mensagem do usuário (saudação, despedida ou agradecimento).")
    resposta = dspy.OutputField(desc="Sua resposta rápida como MIA.")

class RedigirResposta(dspy.Signature):
    """Você é a MIA, assistente virtual focada na análise de produção do supermercado.
    
    REGRAS ABSOLUTAS:
    1. Responda SEMPRE em Português do Brasil.
    2. Responda APENAS com base no Dado Bruto fornecido.
    3. Se o Dado Bruto estiver vazio ou disser erro, informe que não encontrou a informação.
    4. Seja amigável e conversacional. Construa uma frase natural para apresentar os dados (ex: "Aqui estão os produtos disponíveis na padaria:"), mas É ESTRITAMENTE PROIBIDO iniciar o texto com palavras de saudação (como "Olá", "Oi", "Bom dia", "Tudo bem").
    5. OBRIGATÓRIO: Para criar listas, use EXCLUSIVAMENTE o caractere especial '•' (bullet). É ESTRITAMENTE PROIBIDO usar asteriscos (*) no início das linhas.
    6. RETENÇÃO DE DADOS: É estritamente proibido ocultar ou resumir números. Se o Dado Bruto contiver métricas extras (como vendas e descartes entre parênteses), você DEVE transcrever esses valores na resposta final. Exemplo de formato: "• [Produto]: [X] produzidos (Vendas: [Y], Descarte: [Z])".
    7. OBRIGATÓRIO quando tiver preço no dato: Preço deve retornar como R$ X,XX.
    """
    mensagem = dspy.InputField()
    dado_consultado = dspy.InputField(desc="Resultado numérico ou extração da ferramenta. Mantenha todas as métricas originais, sem resumir.")
    resposta_final = dspy.OutputField(desc="A resposta final estruturada e preenchida estritamente com base no dado bruto.")
    
agente_roteador = dspy.Predict(RotearIntencao)
agente_relacional = dspy.Predict(ResponderSaudacao)
agente_redator = dspy.Predict(RedigirResposta)

class AgenteAnalista(dspy.Module):
    def __init__(self, categoria: str):
        super().__init__()
        ferramentas_da_categoria = obter_ferramentas_por_categoria(categoria)
        
        nomes_ferramentas = [f.name for f in ferramentas_da_categoria]
        print(f"\n[DEBUG ROTEAMENTO] Categoria escolhida: {categoria}")
        print(f"[DEBUG ROTEAMENTO] Ferramentas ativas: {nomes_ferramentas}\n")
        
        self.ciclo_react = dspy.ReAct(
            "pergunta: str -> dado_calculado: str", 
            tools=ferramentas_da_categoria
        )
        
    def forward(self, pergunta):
        return self.ciclo_react(pergunta=pergunta)