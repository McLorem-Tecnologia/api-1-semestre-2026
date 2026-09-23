import telebot
from telebot.apihelper import ApiTelegramException
from ia.message import processar_mensagem

def iniciar_bot(bot_key):
    bot = telebot.TeleBot(bot_key)

    tipos_nao_suportados = [
        'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 
        'voice', 'location', 'contact', 'animation'
    ]

    @bot.message_handler(commands=['start'])
    def comando_start(message):
        texto_boas_vindas = (
            "Olá! 👋 Eu sou a *MIA*, a sua Assistente de Inteligência Artificial para Análise de Dados.\n\n"
            "Estou aqui para ajudar a equipa de liderança a otimizar o planeamento de produção e a reduzir o desperdício no supermercado.\n\n"
            "Não precisa de utilizar barras ou decorar comandos difíceis! Pode falar comigo de forma totalmente natural, como se estivesse a falar com um colega de trabalho. 🧠💬\n\n"
            "Para começarmos, experimente perguntar-me coisas como:\n"
            "🔹 _\"Quais produtos precisamos de produzir hoje?\"_\n"
            "🔹 _\"Quantas unidades do produto X devemos fazer tendo em conta as vendas do último mês?\"_\n\n"
            "Como posso ajudar no seu planeamento hoje?"
        )
        
        # O parse_mode='Markdown' permite que o Telegram leia os * (negrito) e _ (itálico)
        bot.reply_to(message, texto_boas_vindas, parse_mode='Markdown')
    
    @bot.message_handler(content_types=['text'])
    def receber_texto(message):
        print(f"[DEBUG] Mensagem recebida: {message.text}")

        msg_temp = bot.reply_to(message, "⏳ <b><i>Processando sua solicitação...</i></b>", parse_mode='HTML')
        bot.send_chat_action(message.chat.id, 'typing')

        resposta_bruta = str(processar_mensagem(message.text))
        resposta = resposta_bruta.replace('```html', '').replace('```', '').replace('[[ ## completed ]]', '').strip()

        print(f"[DEBUG] Resposta processada: {resposta}")
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_temp.message_id,
            text=resposta
        )
    
    @bot.message_handler(content_types=tipos_nao_suportados)
    def receber_formatos_invalidos(message):
        bot.reply_to(
            message, 
            "Desculpe, no momento eu não suporto esse formato enviado. Por favor, me envie apenas mensagens de texto!"
        )

    print("MIA está online e ouvindo...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)