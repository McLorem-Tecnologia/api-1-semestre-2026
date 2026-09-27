# 📘 Manual do Usuário - MIA — Assistente de Análise de Dados

Bem-vindo ao manual de utilização da **MIA**! Este documento destina-se aos usuários finais (Líderes e Gerentes de Produção) e explica como interagir com a nossa assistente inteligente integrada diretamente no Telegram.

## 1. O que é a MIA?
A MIA é uma Assistente de Inteligência Artificial desenhada para processar dados de supermercados (vendas, descartes e regras de produção) e devolver *insights* valiosos de forma rápida. Seu grande diferencial é a **ausência de comandos complexos**: toda a interação é feita através de linguagem natural.

## 2. Primeiros Passos
1. **Acesso:** Abra o aplicativo do Telegram no seu celular ou computador.
2. **Início:** Pesquise pelo *username* do nosso bot (fornecido pela equipe técnica) e clique no botão **"Iniciar"**.
3. **Apresentação:** Ao iniciar, o Telegram envia um comando oculto (`/start`) e a MIA vai se apresentar prontamente no chat, ficando imediatamente pronta para receber suas perguntas.

## 3. Como Interagir (Linguagem Natural)
Esqueça os menus numéricos e as barras de comandos. Trate a MIA como uma colega de trabalho! O modelo de IA, executado localmente, interpreta o seu texto e identifica o que você quer saber.

As recomendações de produção são estimativas baseadas no histórico de dias parecidos (dias de pagamento, fins de semana e feriados), com margem de segurança.
As planilhas de ingredientes e de regras (clima, vésperas) já estão no sistema, mas ainda não são usadas nas respostas.

## 4. Como fazer boas perguntas
* **Setores reconhecidos:** Açougue, Padaria, Cozinha/Rotisseria (também "cozinha" ou "rotisseria"), Peixaria (também "peixe") e Confeitaria (também "doce"). Pequenos erros de digitação são corrigidos (ex.: "acugue").
* **Datas:** "hoje", "hj", "amanhã", "ontem", "anteontem", "há 3 dias", "3 dias atrás", "daqui a 2 dias", "em 5 dias" ou uma data no formato DD/MM/AAAA. Dias da semana ("segunda passada") ainda não são garantidos.
* **Período dos dados:** de 01/08/2026 a 30/09/2026 (descartes só de setembro).
* **Somente texto:** áudio, foto, vídeo, documento, figurinha e localização recebem um aviso de formato não suportado.
* **Fora do escopo:** perguntas que não são sobre a produção do supermercado recebem "Desculpe, meu sistema é restrito à análise e produção do supermercado."

## 5. Mensagens de erro
| Mensagem | O que fazer |
| --- | --- |
| "⚠️ Ops! Minha inteligência artificial teve um branco..." | Reformule a pergunta de forma mais direta. |
| "⚠️ Ocorreu um erro inesperado de conexão com a IA." | O motor de IA está fora do ar. Avise o administrador do sistema. |
| Nenhuma resposta | O bot está desligado. Avise o administrador do sistema. |