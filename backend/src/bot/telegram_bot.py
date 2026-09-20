import telebot
from ia.config import processar_mensagem

def iniciar_bot(bot_key):
    bot = telebot.TeleBot(bot_key)

    tipos_nao_suportados = [
        'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 
        'voice', 'location', 'contact', 'animation'
    ]
    
    @bot.message_handler(content_types=['text'])
    def receber_texto(message):
        print(f"[Bot] Mensagem recebida: {message.text}")
        mensagem_status = bot.reply_to(message, "Pensando...")
        bot.send_chat_action(message.chat.id, "typing")
        resposta = processar_mensagem(message.text)
        bot.edit_message_text(
            str(resposta),
            message.chat.id,
            mensagem_status.message_id,
        )
    
    @bot.message_handler(content_types=tipos_nao_suportados)
    def receber_formatos_invalidos(message):
        bot.reply_to(
            message, 
            "Desculpe, no momento eu não suporto esse formato enviado. Por favor, me envie apenas mensagens de texto!"
        )

    print("Bot está online e ouvindo...")
    bot.infinity_polling()