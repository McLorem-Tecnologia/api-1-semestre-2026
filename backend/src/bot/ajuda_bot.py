from telebot import types


MENU = {
    "producao": {
        "titulo": "🍞 Produção",
        "descricao": "Previsão, produção real e metas. As respostas de previsão sempre incluem quantidades.",
        "perguntas": [
            ("Previsão para amanhã", "O que devo produzir amanhã?"),
            ("Previsão por setor", "O que devo produzir amanhã na padaria?"),
            ("Separar por período", "O que devo produzir amanhã em cada período do dia na padaria?"),
            ("Produção realizada", "O que foi produzido ontem na padaria?"),
            ("Meta de produção", "O que deveria ter sido produzido ontem na padaria?"),
        ],
    },
    "materia_prima": {
        "titulo": "🌾 Matéria-prima",
        "descricao": "Necessidade por ingrediente, estoque, sobras e sugestões de transferência. As sugestões não alteram o estoque.",
        "perguntas": [
            ("Necessidade do setor", "Quanta matéria-prima preciso separar para amanhã na padaria?"),
            ("Necessidade geral", "Quanta matéria-prima preciso para amanhã em todos os setores?"),
            ("Ver sobras disponíveis", "Quais matérias-primas estão disponíveis para transferir para outros setores?"),
            ("Sugerir transferência", "O que pode ser transferido da padaria para cobrir faltas em outros setores?"),
        ],
    },
    "descarte": {
        "titulo": "♻️ Descarte e desperdício",
        "descricao": "Consulte o custo do desperdício por data, período ou setor.",
        "perguntas": [
            ("Custo de ontem", "Quanto custou o desperdício ontem?"),
            ("Por setor", "Quanto foi descartado em reais na padaria em 01/10/2026?"),
            ("Por intervalo", "Qual foi o custo do desperdício da peixaria de 01/09/2026 a 15/09/2026?"),
            ("Toda a empresa", "Quanto custou o desperdício na empresa toda em 01/10/2026?"),
        ],
    },
    "produtos": {
        "titulo": "🛒 Produtos e catálogo",
        "descricao": "Veja catálogo, informações de um produto ou setor e tempo de preparo.",
        "perguntas": [
            ("Listar catálogo", "Quais produtos vocês têm?"),
            ("Detalhes do catálogo", "Me mostre os detalhes de todos os produtos."),
            ("Detalhes de um produto", "Quais são as informações da coxinha?"),
            ("Produtos do setor", "Quais produtos são da confeitaria?"),
            ("Tempo de preparo", "Quais produtos ficam prontos em 10 minutos?"),
        ],
    },
    "vendas": {
        "titulo": "📈 Vendas, preços e lucro",
        "descricao": "Consulte preços e rankings de lucro. Para comparar períodos, informe as datas.",
        "perguntas": [
            ("Preço dos produtos", "Qual é o preço do pão francês e da marmita?"),
            ("Produtos e preços por setor", "Quais produtos estão disponíveis na padaria e quanto custam?"),
            ("Ranking de lucro", "Quais produtos deram mais lucro entre 01/09/2026 e 30/09/2026?"),
            ("Top 5", "Quais são os 5 produtos mais lucrativos entre 01/09/2026 e 30/09/2026?"),
            ("Lucro por setor", "Qual setor concentra mais lucro entre os 5 produtos mais lucrativos de 01/09/2026 a 30/09/2026?"),
            ("Conferir um produto", "Confere o lucro da marmita entre 01/09/2026 e 30/09/2026?"),
        ],
    },
}

PERGUNTAS = {
    f"{categoria}:{indice}": pergunta
    for categoria, dados in MENU.items()
    for indice, (_, pergunta) in enumerate(dados["perguntas"])
}


def _teclado_principal():
    teclado = types.InlineKeyboardMarkup(row_width=2)
    botoes = [
        types.InlineKeyboardButton(dados["titulo"], callback_data=f"ajuda:categoria:{categoria}")
        for categoria, dados in MENU.items()
    ]
    botoes.append(types.InlineKeyboardButton("🎙️ Perguntar por áudio", callback_data="ajuda:audio"))
    teclado.add(*botoes)
    return teclado


def _teclado_categoria(categoria):
    teclado = types.InlineKeyboardMarkup(row_width=1)
    for indice, (rotulo, _) in enumerate(MENU[categoria]["perguntas"]):
        teclado.add(
            types.InlineKeyboardButton(
                f"💬 {rotulo}",
                callback_data=f"ajuda:pergunta:{categoria}:{indice}",
            )
        )
    teclado.add(types.InlineKeyboardButton("⬅️ Voltar ao menu", callback_data="ajuda:principal"))
    return teclado


def registrar_comandos_ajuda(bot, processar_mensagem):
    """Registra /ajuda, /help e o menu de exemplos no bot do Telegram."""

    @bot.message_handler(commands=["ajuda", "help"])
    def comando_ajuda(message):
        bot.reply_to(
            message,
            "🤖 <b>Como posso ajudar?</b>\n\n"
            "Escolha um assunto para ver perguntas prontas. Você também pode escrever sua pergunta com suas palavras.\n\n"
            "As previsões de produção sempre mostram quantidades. Os mesmos exemplos podem ser enviados por áudio.",
            parse_mode="HTML",
            reply_markup=_teclado_principal(),
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("ajuda:"))
    def selecionar_opcao(call):
        bot.answer_callback_query(call.id)
        partes = call.data.split(":")
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if partes[1] == "principal":
            bot.edit_message_text(
                "🤖 <b>Como posso ajudar?</b>\n\nEscolha um assunto ou envie uma pergunta em texto ou áudio.",
                chat_id,
                message_id,
                parse_mode="HTML",
                reply_markup=_teclado_principal(),
            )
            return

        if partes[1] == "audio":
            bot.edit_message_text(
                "🎙️ <b>Perguntas por áudio</b>\n\n"
                "Grave qualquer pergunta dos menus e envie como mensagem de voz. A MIA transcreve e usa a mesma análise da pergunta digitada.\n\n"
                "Não precisa separar perguntas de ‘o que’ e ‘quanto’: as previsões de produção sempre trazem as quantidades.",
                chat_id,
                message_id,
                parse_mode="HTML",
                reply_markup=_teclado_principal(),
            )
            return

        if partes[1] == "categoria":
            categoria = partes[2]
            dados = MENU[categoria]
            bot.edit_message_text(
                f"<b>{dados['titulo']}</b>\n\n{dados['descricao']}\n\nToque em uma pergunta para consultar a MIA:",
                chat_id,
                message_id,
                parse_mode="HTML",
                reply_markup=_teclado_categoria(categoria),
            )
            return

        if partes[1] == "pergunta":
            categoria, indice = partes[2], int(partes[3])
            pergunta = PERGUNTAS[f"{categoria}:{indice}"]
            mensagem = bot.send_message(
                chat_id,
                f"💬 <b>{pergunta}</b>\n\n⏳ Consultando…",
                parse_mode="HTML",
            )
            try:
                bot.send_chat_action(chat_id, "typing")
                resposta = str(processar_mensagem(pergunta.lower()))
                bot.edit_message_text(
                    resposta,
                    chat_id,
                    mensagem.message_id,
                    parse_mode="HTML",
                    reply_markup=_teclado_principal(),
                )
            except Exception as erro:
                print(f"[ERRO MENU AJUDA] {erro}")
                bot.edit_message_text(
                    "⚠️ Não consegui concluir essa consulta agora. Tente enviar a pergunta como mensagem de texto.",
                    chat_id,
                    mensagem.message_id,
                    reply_markup=_teclado_principal(),
                )
