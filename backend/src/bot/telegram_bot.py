import time
import os
import tempfile
import telebot
from ia.message import processar_mensagem
from ia.transcricao import transcrever_audio

def iniciar_bot(bot_key):
    bot = telebot.TeleBot(bot_key)

    tipos_nao_suportados = [
        'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 
        'location', 'contact', 'animation'
    ]

    @bot.message_handler(commands=['start'])
    def comando_start(message):
        texto_boas_vindas = (
            "Olá! 👋 Prazer, eu sou a *MIA*, sua assistente inteligente para análise de dados! ✨📊\n\n"
            "Meu trabalho aqui é ajudar a equipe de liderança a planejar nossa produção, garantindo bons resultados. 🛒💚\n\n"
            "Pode conversar comigo do seu jeito, de forma natural, como se estivesse batendo um papo com alguém da equipe! 🧠💬\n\n"
            "Para testar, que tal me perguntar coisas como:\n\n"
            "🍞 _\"MIA, quais produtos precisamos produzir hoje?\"_\n"
            "📈 _\"Quantas unidades devo produzir amanhã?\"_\n\n"
            "Como eu posso facilitar o seu planejamento hoje? 🥰"
        )   
        
        # O parse_mode='Markdown' permite que o Telegram leia os * (negrito) e _ (itálico)
        bot.reply_to(message, texto_boas_vindas, parse_mode='Markdown')
    
    @bot.message_handler(content_types=['text'])
    def receber_texto(message):
        print(f"[DEBUG] Mensagem recebida: {message.text}")

        t0 = time.perf_counter()
        msg_temp = bot.reply_to(message, "⏳ <b><i>Processando sua solicitação...</i></b>", parse_mode='HTML')
        
        resposta = str(processar_mensagem(message.text.lower()))
        
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_temp.message_id,
            text=resposta,
            parse_mode='HTML'
        )
                        
        print(f"[TEMPO TEXTO] Processamento completo: {time.perf_counter()-t0:.2f}s")

    
    @bot.message_handler(content_types=['voice'])
    def receber_audio(message):
        t0 = time.perf_counter()
        msg_temp = bot.reply_to(
            message,
            "🎧 <b>Recebi seu áudio! Estou transcrevendo...</b>",
            parse_mode='HTML'
        )

        caminho_audio = None

        try:
            # Busca as informações do áudio no Telegram
            arquivo = bot.get_file(message.voice.file_id)

            # Baixa o conteúdo do áudio
            conteudo_audio = bot.download_file(arquivo.file_path)

            # Salva o áudio em um arquivo temporário
            with tempfile.NamedTemporaryFile(
                suffix='.ogg',
                delete=False
            ) as arquivo_temp:
                arquivo_temp.write(conteudo_audio)
                caminho_audio = arquivo_temp.name

            # Converte o áudio em texto
            texto = transcrever_audio(caminho_audio)

            if not texto:
                resposta = "Não consegui identificar a fala no áudio. Tente enviar novamente."
            else:
                print(f"[DEBUG] Áudio transcrito: {texto}")

                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=msg_temp.message_id,
                    text="🧠 <b>Entendi seu áudio! Estou analisando...</b>",
                    parse_mode='HTML'
                )

                # Usa o mesmo processamento das mensagens escritas
                resposta = str(processar_mensagem(texto.lower()))

            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_temp.message_id,
                text=resposta,
                parse_mode='HTML'
            )

        except Exception as erro:
            print(f"[ERRO ÁUDIO] {erro}")

            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_temp.message_id,
                text="Não consegui processar seu áudio. Tente novamente.",
                parse_mode='HTML'
            )

        finally:
            # Remove o arquivo temporário após o processamento
            if caminho_audio and os.path.exists(caminho_audio):
                os.remove(caminho_audio)

            print(
                f"[TEMPO ÁUDIO] Processamento completo: "
                f"{time.perf_counter() - t0:.2f}s"
            )

    
    @bot.message_handler(content_types=tipos_nao_suportados)
    def receber_formatos_invalidos(message):
        bot.reply_to(
            message, 
            "Desculpe, no momento eu não suporto esse formato enviado. Por favor, me envie apenas mensagens de texto ou de voz!"
        )

    print("[MIA] Bot no ar! Aguardando mensagens no Telegram...")
    bot.infinity_polling(skip_pending=True)