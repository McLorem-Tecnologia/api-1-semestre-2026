# 📘 Manual do Usuário — MIA - Assistente de Análise de Dados

Bem-vindo ao manual de utilização da **MIA**! Este documento destina-se aos usuários finais (Líderes e Gerentes de Produção) e explica como interagir com a nossa assistente inteligente integrada diretamente no Telegram.

## 1. O que é a MIA?
A MIA é uma Assistente de Inteligência Artificial desenhada para processar dados de supermercados (vendas, descartes e regras de produção) e devolver *insights* valiosos de forma rápida. Seu grande diferencial é a **ausência de comandos complexos**: toda a interação é feita através de linguagem natural.

## 2. Primeiros Passos
1. **Acesso:** Abra o aplicativo do Telegram no seu celular ou computador.
2. **Início:** Pesquise pelo *username* do nosso bot (fornecido pela equipe técnica) e clique no botão **"Iniciar"**.
3. **Apresentação:** Ao iniciar, o Telegram envia um comando oculto (`/start`) e a MIA vai se apresentar prontamente no chat, ficando imediatamente pronta para receber suas perguntas.

## 3. Como Interagir (Linguagem Natural)
Esqueça os menus numéricos e as barras de comandos. Trate a MIA como uma colega de trabalho! O modelo de IA, executado localmente, interpreta o seu texto (ou a sua voz) e identifica o que você quer saber.

**Por texto ou por voz:** digite a pergunta ou grave uma **mensagem de voz** no Telegram (segure o botão do microfone). A MIA transcreve o áudio, avisa que entendeu e responde por texto, como se você tivesse digitado.

As recomendações de produção são estimativas baseadas no histórico de dias parecidos (dias de pagamento, fins de semana e feriados), com margem de segurança.
As receitas, o estoque e o custo dos ingredientes já são usados (matéria-prima e custo do desperdício). A planilha de regras (clima, vésperas) já está no sistema, mas ainda não é usada nas respostas.

### O que você pode perguntar
| Assunto | Exemplos |
| ------- | -------- |
| O que produzir (previsão) | "O que precisamos produzir amanhã na padaria?", "Quantas unidades devo produzir hoje?" |
| Produção por período do dia | "Quanto de pão francês amanhã de manhã?", "Previsão de hoje à tarde e à noite", "Quanto produzir em cada período hoje?" |
| O que foi produzido / a meta do dia | "O que foi produzido em 10/10/2026 na confeitaria?", "O que deveria ter sido produzido segunda passada?" |
| Matéria-prima | "Quanta matéria-prima preciso separar para amanhã?" |
| Produtos e preços | "Quais produtos tem no açougue?", "Qual o preço do pão francês e do frango assado?" |
| Custo do desperdício | "Quanto foi descartado em reais no dia 10/10/2026?", "Qual o custo do desperdício da padaria de 1 a 15 de setembro?" |

## 4. Como fazer boas perguntas
* **Setores reconhecidos:** Açougue, Padaria, Cozinha/Rotisseria (também "cozinha" ou "rotisseria"), Peixaria (também "peixe") e Confeitaria (também "doce"). Pequenos erros de digitação são corrigidos (ex.: "acugue").
* **Datas:** "hoje", "hj", "amanhã", "ontem", "anteontem", "há 3 dias", "3 dias atrás", "daqui a 2 dias", "em 5 dias" ou uma data no formato DD/MM/AAAA. Dias da semana ("segunda passada", "próxima sexta") e datas por extenso ("2 de novembro de 2026") também são reconhecidos. Na voz, números por extenso funcionam ("há três dias").
* **Matéria-prima:** a MIA lista os ingredientes de cada produto com a unidade já ajustada (por exemplo, 350 g em vez de 0,35 Kg; mL em vez de L quando for pouco). Se o estoque não for suficiente, ela avisa quanto é necessário e quanto há disponível.
* **Períodos do dia:** manhã, tarde e noite ("de manhã", "à noite", "manhã e tarde"). Para o dia todo, peça "por período" ou "em cada período".
* **Período dos dados:** vendas de 01/01/2025 a 26/10/2026 e descartes de 01/01/2026 a 26/10/2026.
* **Texto e voz:** mensagens de voz são aceitas. Arquivo de áudio, foto, vídeo, documento, figurinha, GIF, localização e contato recebem um aviso de formato não suportado. Em ambiente barulhento, fale perto do microfone e use frases curtas.
* **Fora do escopo:** perguntas que não são sobre a produção do supermercado recebem "Desculpe, meu sistema é restrito à análise e produção do supermercado."

## 5. Mensagens de erro
| Mensagem                                                 | O que fazer                                                      |
| -------------------------------------------------------- | ---------------------------------------------------------------- |
| "⚠️ Ops! Minha inteligência artificial teve um branco..." | Reformule a pergunta de forma mais direta.                       |
| "⚠️ Ocorreu um erro inesperado de conexão com a IA."      | O motor de IA está fora do ar. Avise o administrador do sistema. |
| "Não consegui identificar a fala no áudio. Tente enviar novamente." | Grave de novo, mais perto do microfone e com menos ruído. |
| "Não consegui processar seu áudio. Tente novamente." | Envie o áudio outra vez; se persistir, mande a pergunta por texto e avise o administrador. |
| Nenhuma resposta                                         | O bot está desligado. Avise o administrador do sistema.          |