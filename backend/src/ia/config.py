import dspy

IA_APRIMORADA = dspy.LM(
    model="ollama/gemma4:e2b", 
    api_base="http://localhost:11434", 
    max_tokens=4096, 
    num_ctx=8192, 
    reasoning_effort="None"
)

def configurar_ia():
    dspy.configure(lm=IA_APRIMORADA, verbose=True)
    print("[IA] DSPy vinculado ao modelo com sucesso.")