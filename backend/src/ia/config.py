import dspy

# Modelos de IA
# IA_FILTRO = dspy.LM(model="ollama/gemma3:1b", api_base="http://localhost:11434")
IA_APRIMORADA = dspy.LM(model="ollama/gemma4:e2b", api_base="http://localhost:11434", max_tokens=4096, num_ctx=8192)

def iniciar_configuracoes_ia():
    dspy.configure(lm=IA_APRIMORADA, verbose=True)
    print("[IA] Modelos configurados com sucesso.")