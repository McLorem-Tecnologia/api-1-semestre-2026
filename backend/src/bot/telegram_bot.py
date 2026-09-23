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
            "Olá! 👋 Prazer, eu sou a *MIA*, sua assistente inteligente para análise de dados! ✨📊\n\n"
            "Meu trabalho aqui é ajudar a equipe de liderança a planejar nossa produção, garantindo bons resultados. 🛒💚\n\n"
            "Pode conversar comigo do seu jeito, de forma natural, como se estivesse batendo um papo com alguém da equipe! 🧠💬\n\n"
            "Para testar, que tal me perguntar coisas como:\n\n"
            "🍞 _\"MIA, quais produtos precisamos produzir hoje?\"_\n"
            "📈 _\"Quantas unidades do produto X devemos fazer com base nas vendas do último mês?\"_\n\n"
            "Como eu posso facilitar o seu planejamento hoje? 🥰"
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
    bot.infinity_polling(timeout=20, long_polling_timeout=20)