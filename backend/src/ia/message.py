import dspy
from dspy.utils.exceptions import AdapterParseError
from ia.config import IA_APRIMORADA 
from ia.agentes import agente_roteador, agente_relacional, agente_redator, AgenteAnalista

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
                analista = AgenteAnalista(categoria)
                resultado = analista(pergunta=texto_usuario)
                
                dspy.inspect_history(n=1) 
                
                texto_final = agente_redator(
                    mensagem=texto_usuario, 
                    dado_consultado=resultado.dado_calculado
                )
                return texto_final.resposta_final

    except AdapterParseError as erro_dspy:
        print(f"[ERRO DSPY] O modelo travou e retornou nulo. Log: {erro_dspy}")
        return "⚠️ Ops! Minha inteligência artificial teve um branco e não conseguiu processar as ferramentas."
        
    except Exception as erro_geral:
        print(f"[ERRO GERAL IA] {erro_geral}")
        return "⚠️ Ocorreu um erro inesperado de conexão com a IA."