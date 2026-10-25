import dspy

REGISTRO_DE_FERRAMENTAS = {}

def dspy_tool(categoria: str):
    """
    Decorador que aplica o dspy.tool nativo e regista a ferramenta numa categoria.
    Uso: @dspy_tool('PRODUCAO')
    """
    categoria_upper = categoria.strip().upper()

    def decorator(func):
        # Aplica o decorador oficial do DSPy
        ferramenta_dspy = dspy.Tool(func)

        # Regista no dicionário
        if categoria_upper not in REGISTRO_DE_FERRAMENTAS:
            REGISTRO_DE_FERRAMENTAS[categoria_upper] = []

        REGISTRO_DE_FERRAMENTAS[categoria_upper].append(ferramenta_dspy)

        return ferramenta_dspy

    return decorator

def obter_ferramentas_por_categoria(categoria: str) -> list:
    """Retorna a lista de ferramentas de uma categoria específica."""
    return REGISTRO_DE_FERRAMENTAS.get(categoria.strip().upper(), [])

# ⚠️ IMPORTANTE: Importar os módulos no final garante que as funções
# sejam lidas pelo Python e os decoradores sejam executados ao iniciar o bot.
import ia.tools.produtos_tools
import ia.tools.producao_tool
import ia.tools.desperdicio_tool
