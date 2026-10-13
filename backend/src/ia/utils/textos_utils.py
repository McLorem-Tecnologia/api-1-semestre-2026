import difflib

def normalizar_setor(setor_informado: str) -> str:
    """
    Corrige erros de digitação e mapeia apelidos para o nome oficial do setor no banco de dados.
    """
    if not setor_informado or setor_informado.lower() in ['none', 'null', 'vazio']:
        return None
        
    setores_oficiais = ["Açougue", "Padaria", "Cozinha/Rotisseria", "Peixaria", "Confeitaria"]
    texto_limpo = setor_informado.strip().lower()
    
    alias_map = {
        "cozinha": "Cozinha/Rotisseria",
        "rotisseria": "Cozinha/Rotisseria",
        "roti": "Cozinha/Rotisseria",
        "acougue": "Açougue",
        "carne": "Açougue",
        "peixe": "Peixaria",
        "doce": "Confeitaria"
    }
    
    for apelido, oficial in alias_map.items():
        if apelido in texto_limpo:
            return oficial
            
    matches = difflib.get_close_matches(setor_informado.title(), setores_oficiais, n=1, cutoff=0.6)
    
    if matches:
        return matches[0]
        
    return setor_informado.capitalize()