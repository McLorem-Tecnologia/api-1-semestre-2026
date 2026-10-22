from faster_whisper import WhisperModel

modelo = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def transcrever_audio(caminho_audio: str) -> str:
    """Transcreve um arquivo de áudio para texto."""
    segmentos, _ = modelo.transcribe(
        caminho_audio,
        language="pt",
        vad_filter=True
    )

    texto = " ".join(
        segmento.text.strip()
        for segmento in segmentos
    )

    return texto.strip()