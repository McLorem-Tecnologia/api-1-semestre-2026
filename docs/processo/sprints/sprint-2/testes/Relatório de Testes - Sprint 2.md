# Relatório de Testes — Sprint 2

Este documento registra a execução manual dos testes da MIA na Sprint 2: cada linha da tabela de registro mostra a mensagem enviada no Telegram e o resultado obtido. As evidências completas (respostas longas do bot) estão no final do documento.

## Identificação da execução

| Item              | Valor                                                                                     |
| ----------------- | ----------------------------------------------------------------------------------------- |
| Datas de execução | Mirela - `23/10/2026`, Marcus, Ian e Eduardo - `25/10/2026`                               |
| Executado por     | Marcus Vinícius, Ian Victor (10.1 a 10.4) Eduardo Granja (8.1 a 8.3) e Mirela (9.1 a 9.4) |
| Modelo            | ollama/gemma4:e2b                                                                         |
| Python            | Python 3.13.6                                                                             |

## Resumo

| Total | ✅ Aprovados | ⚠️ Com ressalva | ❌ Reprovados |
| :---: | :---------: | :------------: | :----------: |
|  42   |     33      |       8        |      1       |

---

## Pré-requisitos antes de começar

- [x] Ollama aberto, com o modelo `ollama pull gemma4:e2b` baixado
- [x] Arquivo `.env` configurado em `backend/src/.env` com `TELEGRAM_BOT_KEY` válido
- [x] `python main.py` rodando sem erros no terminal (verifique se aparece "[IA] Modelos configurados com sucesso.")
- [x] Bot respondendo a `/start` no Telegram
- [x] CSVs de vendas com a **informação de horário** (ou regra para derivar o período do dia) disponíveis em `backend/dados/` (definição da US05)
- [x] CSVs com **preço de venda** e **custo unitário** dos produtos disponíveis em `backend/dados/` (definição das US06, US07 e US08)
- [x] Solução de transcrição de áudio instalada e funcionando localmente (definida no Planning da US09)
- [x] CSVs de **matéria-prima** (consumo por produto e estoque por setor) disponíveis em `backend/dados/` (definição das US10 e US11)
- [x] Celular com Telegram para gravar as mensagens de voz

---

## Roteamento e comportamento social (`agentes.py`)

Continuação dos casos 0.2.1 a 0.2.4 da Sprint 1.

| ID    | Mensagem para enviar                                 | Resultado esperado                                                                            |
| ----- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 0.2.5 | "Quanto devo produzir amanhã?"                       | Responde em unidades de **produto**, sem confundir com matéria-prima (US10)                   |
| 0.2.6 | "Quanto lucro a concorrência teve?" (fora do escopo) | Recusa padrão: a MIA só responde sobre os dados do próprio supermercado, sem inventar valores |

---

## Formatação da resposta

Continuação dos casos 0.3.1 a 0.3.3 da Sprint 1.

| ID    | O que verificar              | Resultado esperado                                                                     |
| ----- | ---------------------------- | -------------------------------------------------------------------------------------- |
| 0.3.4 | Valores monetários           | Sempre no padrão brasileiro, com duas casas decimais (ex.: R$ 1.234,56)                |
| 0.3.5 | Quantidades de matéria-prima | Sempre acompanhadas da unidade de medida (kg, L, unidade)                              |
| 0.3.6 | Resposta a um áudio          | Mesma formatação da resposta a um texto                                                |
| 0.3.7 | Resposta por período do dia  | Os períodos aparecem em ordem cronológica (manhã, tarde, noite) e claramente separados |

---

## US05 — O que produzir em cada período do dia (líder)

| ID  | Mensagem para enviar                                                      | Resultado esperado                                                                                                                                                                                  |
| --- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5.1 | "O que eu devo produzir de manhã na padaria?"                             | Produtos da Padaria (10 produtos) a produzir na manhã, com a quantidade e a unidade de medida de cada um (Kg, Un, Porção ou L)                                                                      |
| 5.2 | "O que produzir em cada período do dia na padaria?"                       | Produtos e quantidades separados por período (manhã, tarde e noite), no mesmo formato para todos os períodos. Cada período é projetado separadamente, então a soma pode divergir da previsão do dia |
| 5.3 | "O que preciso fazer à tarde no açougue?"                                 | Mesmo cálculo, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta                                                                                                      |
| 5.4 | "O que devo produzir de manhã na padaira?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro                                                                                                                                    |
| 5.5 | "O que devo produzir de manhã?" (sem informar o setor)                    | Sem setor, a MIA traz os produtos de todos os setores (33 produtos) no período da manhã; sem data, assume hoje                                                                                      |
| 5.6 | "O que devo produzir à noite amanhã na cozinha?"                          | `converter_data_relativa` resolve "amanhã" e a resposta traz só o período da noite, só da Cozinha (5 produtos)                                                                                      |
| 5.7 | Pedir um período sem histórico de vendas (ex.: madrugada)                 | `converter_periodo` converte "madrugada" em "noite" (período mais próximo) e a resposta usa os dados da noite; o ideal é a MIA avisar que usou a noite                                              |
| 5.8 | "O que devo produzir à tarde e à noite na padaria?"                       | Combinação de períodos: cada produto da Padaria com as sublinhas de tarde e noite, sem a manhã                                                                                                      |

---

## US06 — Reais descartados em cada setor (gerente)

| ID  | Mensagem para enviar                                                                          | Resultado esperado                                                                                                                                                                                         |
| --- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 6.1 | "Quantos reais foram descartados no dia 01/10/2026 em cada setor?"                            | Valor em R$ de cada setor (Padaria, Cozinha, Peixaria, Açougue e Processados). A tool calcula um setor por vez, então a MIA consulta setor a setor. Se apresentar um total geral, ele é a soma dos setores |
| 6.2 | "Quantos reais foram descartados no dia 01/10/2026 na padaria?"                               | Um único valor em R$ da Padaria, no formato "Custo total do desperdício ontem (dd/mm/aaaa) (Setor: Padaria): R$ x". A tool devolve só o total, sem detalhe por produto                                     |
| 6.3 | "Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?"                        | Valor em R$ do período para a Peixaria ("no período de 01/09/2026 a 15/09/2026"); testa `data_inicio`, `data_fim` e setor juntos                                                                           |
| 6.4 | "Quantos reais foram descartados no acugue no dia 01/10/2026?" (erro de digitação proposital) | `normalizar_setor` corrige para "Açougue" e a resposta mostra "(Setor: Açougue)"                                                                                                                           |
| 6.5 | "Quantos reais foram descartados no dia 01/10/2026?" (sem informar o setor)                   | Total da empresa inteira (todos os setores somados), sem "(Setor: ...)" na frase                                                                                                                           |
| 6.6 | "Quantos reais foram descartados em 01/01/2020?" (data sem registros)                         | Hoje a tool devolve R$ 0,00; decidir no Planning se a MIA deve avisar que não há registros nessa data                                                                                                      |

---

## US07 — Reais descartados na empresa (gerente)

| ID  | Mensagem para enviar                                                    | Resultado esperado                             |
| --- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| 7.1 | "Quantos reais foram descartados em 07/04/2026 na empresa toda?"        | Valor total em R$ somando todos os setores     |
| 7.2 | "Qual foi o custo total de desperdício em setembro?"                    | Valor total do período; fraseado diferente     |
| 7.3 | "Quantos reais foram descartados no dia 01/10/2026? Separe por setores" | Total geral e o valor de cada setor, agrupados |

---

## US08 — Produtos mais lucrativos na empresa (gerente)

*A fórmula de lucro é definida no Planning (proposta: (preço de venda − custo unitário) × quantidade vendida).*

| ID  | Mensagem para enviar                                                                   | Resultado esperado                                                                             |
| --- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 8.1 | "Quais produtos da empresa trazem mais lucro?"                                         | Ranking geral de todos os setores, ordenado por lucro em R$, indicando o setor de cada produto |
| 8.2 | "Me mostra os 5 produtos mais lucrativos do mercado"                                   | Ranking limitado a 5 itens                                                                     |
| 8.3 | Verificação cruzada: calcular à mão o lucro de um produto do caso 8.1 a partir dos CSV | O valor calculado é igual ao exibido pela MIA                                                  |

---

## US09 — Perguntas por áudio (gestor)

| ID  | Mensagem para enviar                                                              | Resultado esperado                                                                                                                                    |
| --- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 9.1 | Áudio dizendo: "O que devo produzir hoje?"                                        | Transcreve e responde igual ao caso 1.1 da Sprint 1 (lista só com nomes)                                                                              |
| 9.2 | Áudio dizendo: "Quantas unidades devo produzir amanhã na padaria?"                | Resolve "amanhã" e o setor a partir da fala; resposta com nome e quantidade                                                                           |
| 9.3 | Áudio dizendo: "Quanto de coxinha devo fazer amanhã?" em ambiente com ruído       | Transcrição aceitável; se não entender, pede para repetir, sem inventar resposta                                                                      |
| 9.4 | Áudio vazio ou só com silêncio                                                    | Mensagem amigável pedindo para enviar novamente, sem travar o bot                                                                                     |
| 9.5 | Áudio dizendo: "Qual é a capital da França?"                                      | Agente Roteador identifica `INVALIDO`; mesma recusa padrão do texto                                                                                   |
| 9.6 | Enviar a mesma pergunta digitada e depois por áudio                               | As duas respostas têm o mesmo conteúdo                                                                                                                |
| 9.7 | Enviar uma foto                                                                   | Continua respondendo a mensagem fixa de formato não suportado (o caso 0.2.4 da Sprint 1 passa a valer só para formatos que não sejam texto nem áudio) |
| 9.8 | Após os testes, conferir a pasta de arquivos temporários da máquina               | Não restaram arquivos de áudio temporários                                                                                                            |
| 9.9 | Áudio dizendo: "Quantos reais foram descartados no dia 01/10/2026 em cada setor?" | Transcreve e responde igual ao caso 6.1 (valor por setor e total geral)                                                                               |

---

## US10 — Matéria-prima para o dia seguinte (líder)

*Os nomes das matérias-primas abaixo são exemplos: ajuste aos nomes reais da planilha.*

| ID   | Mensagem para enviar                                                                  | Resultado esperado                                                                                       |
| ---- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 10.1 | "Quanta matéria-prima preciso deixar preparada para amanhã na padaria?"               | Lista de matérias-primas da Padaria, com quantidade e unidade, baseada na previsão de produção de amanhã |
| 10.2 | "O que preciso separar de ingredientes para amanhã na cozinha?"                       | Mesmo cálculo, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta           |
| 10.3 | "Quanto de farinha preciso para amanhã?"                                              | Filtra uma matéria-prima e soma o consumo de todos os produtos que a usam                                |
| 10.4 | "Quanta matéria-prima preciso para amanhã?" (sem informar o setor)                    | Comportamento definido no Planning: todos os setores ou pedido do setor ao líder                         |
| 10.5 | "Quanta matéria-prima preciso para a padaira amanhã?" (erro de digitação proposital)  | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro                                         |
| 10.6 | Verificação cruzada: comparar com "Quantas unidades devo produzir amanhã na padaria?" | Quantidade de matéria-prima = quantidade prevista de cada produto × consumo por unidade                  |

---

## Tabela de Registro dos Testes

| Caso  | Mensagem enviada                                                                       | Resultado obtido                                                                                                                                                                                                                                            | Status | Observações                                                                                                                                                                                                                                                 |
| ----- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.2.5 | Quanto devo produzir amanhã?                                                           | Lista os 33 produtos catalogados em `produtos.csv`, sem confundir com matéria-prima (US10). Ver [evidência completa](#evidencia-025)                                                                                                                        |   ✅    |                                                                                                                                                                                                                                                             |
| 0.2.6 | Quanto lucro a concorrência teve?                                                      | . Ver [evidência completa](#evidencia-027)                                                                                                                                                                                                                  |   ✅    |                                                                                                                                                                                                                                                             |
| 0.3.4 | Valores monetários                                                                     | Mostrou corretamente o valor `R$ 0,00`. Ver [evidência completa](#evidencia-034)                                                                                                                                                                            |   ✅    |                                                                                                                                                                                                                                                             |
| 0.3.5 | Quantidades de matéria-prima                                                           | Está acompanhando a unidade de medida corretamente, no nome do produto. Como podemos ver no [10.1](#evidencia-101)                                                                                                                                          |   ⚠️    | Melhorar na Sprint 3, para que, em vez de mostrar `unidades`, mostre a unidade de medida correta (kg, g, L e mL)                                                                                                                                            |
| 0.3.6 | Resposta a um áudio                                                                    | Correto, pois é feita a transcrição do áudio, que depois é enviada para a mesma função que trata mensagens de texto.                                                                                                                                        |   ✅    |                                                                                                                                                                                                                                                             |
| 0.3.7 | Resposta por período do dia                                                            | Está lidando corretamente com períodos. Como podemos ver na [5.1](#evidencia-51)                                                                                                                                                                            |   ✅    | Se o usuário quiser a produção do dia inteiro separada por períodos, ele deve solicitar todos os períodos ou o dia todo.                                                                                                                                    |
| 5.1   | O que eu devo produzir de manhã na padaria?                                            | Listou os 10 produtos do setor de Padaria, com a quantidade que deve ser produzida no período da manhã. Ver [evidência completa](#evidencia-51)                                                                                                             |   ✅    |                                                                                                                                                                                                                                                             |
| 5.2   | O que produzir em cada período do dia na padaria?                                      | Listou os 10 produtos do setor de Padaria, com a quantidade que deve ser produzida, separada por período. Ver [evidência completa](#evidencia-52)                                                                                                           |   ⚠️    | A resposta não é única; é necessária uma melhoria no Roteador/formatador final.                                                                                                                                                                             |
| 5.3   | O que preciso fazer à tarde no açougue?                                                | Listou corretamente os 6 produtos do setor de Açougue, com a quantidade que deve ser produzida no período da tarde, assim como na 5.1. Ver [evidência completa](#evidencia-53)                                                                              |   ✅    |                                                                                                                                                                                                                                                             |
| 5.4   | O que devo produzir de manhã na padaira?                                               | `normalizar_setor` corrigiu corretamente para `Padaria` mesmo com o erro. Mesma resposta da [5.1](#evidencia-51)                                                                                                                                            |   ✅    |                                                                                                                                                                                                                                                             |
| 5.5   | O que devo produzir de manhã?                                                          | Listou os 33 produtos catalogados em `produtos.csv`, com as quantidades que devem ser produzidas no período da manhã. Ver [evidência completa](#evidencia-55)                                                                                               |   ✅    | Funcionou sem indicar uma data (tratou a data como hoje) e sem indicar um setor (trouxe o mercado todo)                                                                                                                                                     |
| 5.6   | O que devo produzir à noite amanhã na cozinha?                                         | Listou os 5 produtos do setor de Cozinha, com a quantidade que deve ser produzida na noite de amanhã. Ver [evidência completa](#evidencia-56)                                                                                                               |   ✅    |                                                                                                                                                                                                                                                             |
| 5.7   | Pedir um período sem histórico de vendas                                               | Em vez de negar o período, a MIA faz o cálculo utilizando o período mais próximo, que nesse caso é a noite. Ver [evidência completa](#evidencia-57)                                                                                                         |   ⚠️    | Ela responde com o termo `madrugada`, porém a função `converter_periodo` transformou `madrugada` em `noite` para poder realizar o cálculo com os dados do período da `noite`                                                                                |
| 5.8   | O que devo produzir à tarde e à noite na padaria?                                      | Lista o 10 produtos do setor da Padaria mostrando o que deve ser produzido de `tarde` e de `noite`. Ver [evidência completa](#evidencia-58)                                                                                                                 |   ✅    |                                                                                                                                                                                                                                                             |
| 6.1   | Quantos reais foram descartados no dia 01/10/2026 em cada setor?                       | Aqui estão as informações sobre o descarte no dia 01/10/2026:<br>• O custo total do desperdício no dia 01/10/2026 foi de R$ 482.01. A distribuição por setor não foi detalhada pela ferramenta                                                              |   ✅    |                                                                                                                                                                                                                                                             |
| 6.2   | Quantos reais foram descartados no dia 01/10/2026 na padaria?                          | Aqui estão os dados da padaria:<br>• Descarte no dia 01/10/2026: R$ 97,69                                                                                                                                                                                   |   ✅    |                                                                                                                                                                                                                                                             |
| 6.3   | Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?                   | Aqui estão os dados sobre o descarte da peixaria:<br>• Perda total no período de 01/09/2026 a 15/09/2026: R$ 806,36                                                                                                                                         |   ✅    |                                                                                                                                                                                                                                                             |
| 6.4   | Quantos reais foram descartados no acugue no dia 01/10/2026?                           | Aqui estão os valores consultados: R$ 150.60.                                                                                                                                                                                                               |   ✅    |                                                                                                                                                                                                                                                             |
| 6.5   | Quantos reais foram descartados no dia 01/10/2026?                                     | Aqui está a informação sobre o descarte no dia 01/10/2026:<br>• Valor descartado: R$ 482,01                                                                                                                                                                 |   ✅    |                                                                                                                                                                                                                                                             |
| 6.6   | Quantos reais foram descartados em 01/01/2020?                                         | Aqui estão as informações sobre o descarte em 01/01/2020:<br>• Descarte total: R$ 0.00                                                                                                                                                                      |   ✅    |                                                                                                                                                                                                                                                             |
| 7.1   | Quantos reais foram descartados em 07/04/2026 na empresa toda?                         | Aqui estão os dados sobre o descarte na empresa:<br>• Total descartado em 07/04/2026: R$ 543.59                                                                                                                                                             |   ✅    |                                                                                                                                                                                                                                                             |
| 7.2   | Qual foi o custo total de desperdício em setembro?                                     | O custo total de desperdício em setembro foi de R$ 17.094,53.                                                                                                                                                                                               |   ✅    |                                                                                                                                                                                                                                                             |
| 7.3   | Quantos reais foram descartados no dia 01/10/2026? Separe por setores                  | Aqui estão os dados sobre o descarte no dia 01/10/2026:<br>• Custo total descartado: R$ 482.01 (A separação por setores não foi fornecida pela ferramenta).                                                                                                 |   ⚠️    | Atualmente a ferramenta não divide por setor o quando cada setor teve de real descartado.                                                                                                                                                                   |
| 8.1   | Quais produtos da empresa trazem mais lucro?                                           | Mostrou o produto que traz mais lucro para empresa. Ver [evidência completa](#evidencia-81)                                                                                                                                                                 |   ✅    |                                                                                                                                                                                                                                                             |
| 8.2   | Me mostra os 5 produtos mais lucrativos do mercado                                     | Listou os 5 produtos mais lucrativos do supermercado. Ver [evidência completa](#evidencia-82)                                                                                                                                                               |   ✅    |                                                                                                                                                                                                                                                             |
| 8.3   | Verificação cruzada: calcular à mão o lucro de um produto do caso 8.1 a partir dos CSV | O valor calculado bate com os CSV's                                                                                                                                                                                                                         |   ✅    |                                                                                                                                                                                                                                                             |
| 9.1   | Áudio dizendo: "O que devo produzir hoje?"                                             | Lista os 33 produtos catalogados em `produtos.csv`. Ver [evidência completa](#evidencia-91)                                                                                                                                                                 |   ✅    |                                                                                                                                                                                                                                                             |
| 9.2   | Áudio dizendo: "Quantas unidades devo produzir amanhã na padaria?"                     | Listou os 10 produtos do setor de Padaria que devem ser produzidos amanhã. Ver [evidência completa](#evidencia-92)                                                                                                                                          |   ✅    |                                                                                                                                                                                                                                                             |
| 9.3   | Áudio dizendo: "Quanto de coxinha devo fazer amanhã?" em ambiente com ruído            | Aqui estão as informações sobre a produção de coxinha para amanhã:<br>• Coxinha: 172 unidades produzidas.                                                                                                                                                   |   ✅    | Não inventou nenhuma informação e quando não entendeu informou corretamente.                                                                                                                                                                                |
| 9.4   | Áudio vazio ou só com silêncio                                                         | Não consegui identificar a fala no áudio. Tente enviar novamente.                                                                                                                                                                                           |   ✅    |                                                                                                                                                                                                                                                             |
| 9.5   | Áudio dizendo: "Qual é a capital da França?"                                           | Desculpe, Meu sistema é restrito à análise e produção do supermercado.                                                                                                                                                                                      |   ✅    |                                                                                                                                                                                                                                                             |
| 9.6   | Enviar a mesma pergunta digitada e depois por áudio                                    | Funcionou perfeitamente: a resposta foi igual à da [5.1](#evidencia-51)                                                                                                                                                                                     |   ✅    |                                                                                                                                                                                                                                                             |
| 9.7   | Enviar uma foto                                                                        | Desculpe, no momento eu não suporto esse formato enviado. Por favor, me envie apenas mensagens de texto ou de voz!                                                                                                                                          |   ✅    |                                                                                                                                                                                                                                                             |
| 9.8   | Após os testes, conferir a pasta de arquivos temporários da máquina                    | Arquivo foi apagado corretamente.                                                                                                                                                                                                                           |   ✅    |                                                                                                                                                                                                                                                             |
| 9.9   | Áudio dizendo: "Quantos reais foram descartados no dia 01/10/2026 em cada setor?"      | Não foi possível obter o custo de descarte por setor, pois a ferramenta forneceu apenas o custo total do desperdício (R$ 907.33) e não o detalhamento por setor.                                                                                            |   ⚠️    | Erro por conta da ferramente entregar o valor cheio e não divido                                                                                                                                                                                            |
| 10.1  | Quanta matéria-prima preciso deixar preparada para amanhã na padaria?                  | Listou os 10 produtos do setor de Padaria, com a respectiva matéria-prima e a quantidade necessária que deve ficar pronta. Ver [evidência completa](#evidencia-101)                                                                                         |   ⚠️    | Está repetindo o nome do produto para cada matéria-prima, como pode ser visto na [evidência](#evidencia-101), e também não está calculando corretamente os ingredientes que utilizam fração de quantidade, como `0.1` kg. Corrigir esses erros na Sprint 3. |
| 10.2  | O que preciso separar de ingredientes para amanhã na cozinha?                          | Funcionou corretamente, assim como na 10.1, porém listando os produtos que devem ser produzidos `amanhã` na `cozinha`. Ver [evidência completa](#evidencia-102)                                                                                             |   ⚠️    | Apesar de a resposta estar correta, como podemos ver na [evidência](#evidencia-102), talvez seja melhor remover a `Sobra` e resolver os problemas da 10.1, para evitar mensagens muito longas e erros no `telebot`.                                         |
| 10.3  | Quanto de farinha preciso para amanhã?                                                 | A Ferramenta calcula a quantidade de Farinhas de Trigo necessária para cada produto, faz a soma de cada e devolve o total. Ver [evidência completa](#evidencia-103)                                                                                         |   ✅    |                                                                                                                                                                                                                                                             |
| 10.4  | Quanta matéria-prima preciso para amanhã?                                              | `2026-10-25 17:38:10,157 (__init__.py:1301 MainThread) ERROR - TeleBot: "Threaded polling exception: A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: MESSAGE_TOO_LONG"  `                                        |   ❌    | Como informado na 10.2, ocorreu o erro `MESSAGE_TOO_LONG`.                                                                                                                                                                                                  |
| 10.5  | Quanta matéria-prima preciso para a padaira amanhã?                                    | Corrigiu corretamente o nome do setor para `Padaria`. Mesma resposta da [10.1](#evidencia-101)                                                                                                                                                              |   ✅    |                                                                                                                                                                                                                                                             |
| 10.6  | Verificação cruzada: comparar com "Quantas unidades devo produzir amanhã na padaria?"  | Sim. Fazendo o cálculo com a pergunta `Quantos produtos devo produzir amanhã na padaria` e multiplicando pela quantidade de ingredientes por item, o resultado está correto, com exceção dos ingredientes que utilizam fração de quantidade, como `0.1` kg. |   ⚠️    | Problema informado na 10.1.                                                                                                                                                                                                                                 |

---

## Evidências Completas

Respostas longas do bot (que não cabem na tabela) ficam guardadas aqui, uma por caso de teste, dentro de um bloco recolhível.

<details>
<summary><b>0.2.5</b> — "Quanto devo produzir amanhã?"</summary>
<a id="evidencia-025"></a>

```
Aqui estão as previsões de produção para amanhã (26/10/2026):
• Pão Francês (Kg): 134 unidades
• Pão de queijo (Kg): 20 unidades
• Croissant (Kg): 9 unidades
• Coxinha (Un): 172 unidades
• Enroladinho (Un): 132 unidades
• Bolo de chocolate (Kg): 9 unidades
• Torta de limão (Kg): 5 unidades
• Pudim (Un): 43 unidades
• Brigadeiro (Kg): 5 unidades
• Beijinho (Kg): 5 unidades
• Frango assado (Un): 41 unidades
• Marmita (Un): 138 unidades
• Lasanha (Kg): 18 unidades
• Macarrão (Kg): 14 unidades
• Purê de batata (Kg): 15 unidades
• Salgadinhos (Kg): 14 unidades
• Hot Roll (Porção): 22 unidades
• Combo Sushi (Porção): 15 unidades
• Sashimi (Porção): 7 unidades
• Maki (Porção): 13 unidades
• Temaki (Un): 20 unidades
• Ceviche (Porção): 10 unidades
• Hambúrguer (Kg): 14 unidades
• Espetinho (Kg): 28 unidades
• Frango temp (Kg): 21 unidades
• Linguiça (Kg): 19 unidades
• Kafta (Kg): 10 unidades
• Kit Feijoada (Kg): 15 unidades
• Suco Laranja (L): 67 unidades
• Salada Frutas (Kg): 27 unidades
• Caldos/Sopas (Kg): 26 unidades
• Legumes (Kg): 27 unidades
• Salada Verde (Kg): 21 unidades
```

</details>

<details>
<summary><b>0.2.6</b> — "Quanto lucro a concorrência teve?"</summary>
<a id="evidencia-027"></a>

```

```

</details>

<details>
<summary><b>0.3.4</b> — "Valores monetários"</summary>
<a id="evidencia-034"></a>

```
Aqui estão as informações sobre a coxinha:
• SKU: 1004
• Produto: Coxinha (Un)
• Setor: Padaria
• Preço: R$ 6,50
• Tempo de preparo: 5 min.
```

</details>

<details>
<summary><b>5.1</b> — "O que eu devo produzir de manhã na padaria?"</summary>
<a id="evidencia-51"></a>

```
Aqui estão os produtos previstos para produção na manhã da padaria:
• Pão Francês: 107 Kg
• Pão de queijo: 16 Kg
• Croissant: 8 Kg
• Coxinha: 77 Un
• Enroladinho: 60 Un
• Bolo de chocolate: 9 Kg
• Torta de limão: 4 Kg
• Pudim: 26 Un
• Brigadeiro: 5 Kg
• Beijinho: 5 Kg
```

</details>

<details>
<summary><b>5.2</b> — "O que produzir em cada período do dia na padaria?"</summary>
<a id="evidencia-52"></a>

```
Aqui estão as sugestões de produção para cada período do dia na padaria:

• **Manhã:**
    • Pão Francês (Kg): 107
    • Pão de queijo (Kg): 16
    • Croissant (Kg): 8
    • Coxinha (Un): 77
    • Enroladinho (Un): 60
    • Bolo de chocolate (Kg): 9
    • Torta de limão (Kg): 4
    • Pudim (Un): 26
    • Brigadeiro (Kg): 5
    • Beijinho (Kg): 5
    • Frango assado (Un): 66
    • Marmita (Un): 31
    • Lasanha (Kg): 11
    • Macarrão (Kg): 8
    • Purê de batata (Kg): 9
    • Salgadinhos (Kg): 2
    • Hot Roll (Porção): 3
    • Combo Sushi (Porção): 2
    • Sashimi (Porção): 2
    • Maki (Porção): 2
    • Temaki (Un): 3
    • Ceviche (Porção): 5
    • Hambúrguer (Kg): 13
    • Espetinho (Kg): 27
    • Frango temp (Kg): 19
    • Linguiça (Kg): 18
    • Kafta (Kg): 9
    • Kit Feijoada (Kg): 12
    • Suco Laranja (L): 28
    • Salada Frutas (Kg): 12
    • Caldos/Sopas (Kg): 2
    • Legumes (Kg): 8
    • Salada Verde (Kg): 6

• **Tarde:**
    • Pão Francês (Kg): 64
    • Pão de queijo (Kg): 10
    • Croissant (Kg): 5
    • Coxinha (Un): 102
    • Enroladinho (Un): 80
    • Bolo de chocolate (Kg): 6
    • Torta de limão (Kg): 7
    • Pudim (Un): 35
    • Brigadeiro (Kg): 3
    • Beijinho (Kg): 3
    • Frango assado (Un): 66
    • Marmita (Un): 39
    • Lasanha (Kg): 21
    • Macarrão (Kg): 16
    • Purê de batata (Kg): 17
    • Salgadinhos (Kg): 4
    • Hot Roll (Porção): 8
    • Combo Sushi (Porção): 5
    • Sashimi (Porção): 3
    • Maki (Porção): 5
    • Temaki (Un): 7
    • Ceviche (Porção): 7
    • Hambúrguer (Kg): 16
    • Espetinho (Kg): 34
    • Frango temp (Kg): 24
    • Linguiça (Kg): 22
    • Kafta (Kg): 11
    • Kit Feijoada (Kg): 15
    • Suco Laranja (L): 37
    • Salada Frutas (Kg): 15
    • Caldos/Sopas (Kg): 5
    • Legumes (Kg): 10
    • Salada Verde (Kg): 11

• **Noite:**
    • Pão Francês (Kg): 43
    • Pão de queijo (Kg): 7
    • Croissant (Kg): 3
    • Coxinha (Un): 77
    • Enroladinho (Un): 60
    • Bolo de chocolate (Kg): 4
    • Torta de limão (Kg): 2
    • Pudim (Un): 26
    • Brigadeiro (Kg): 2
    • Beijinho (Kg): 2
    • Frango assado (Un): 0
    • Marmita (Un): 8
    • Lasanha (Kg): 4
    • Macarrão (Kg): 3
    • Purê de batata (Kg): 3
    • Salgadinhos (Kg): 16
    • Hot Roll (Porção): 39
    • Combo Sushi (Porção): 27
    • Sashimi (Porção): 13
    • Maki (Porção): 22
    • Temaki (Un): 35
    • Ceviche (Porção): 5
    • Hambúrguer (Kg): 4
    • Espetinho (Kg): 7
    • Frango temp (Kg): 5
    • Linguiça (Kg): 5
    • Kafta (Kg): 3
    • Kit Feijoada (Kg): 3
    • Suco Laranja (L): 28
    • Salada Frutas (Kg): 12
    • Caldos/Sopas (Kg): 25
    • Legumes (Kg): 8
```

</details>

<details>
<summary><b>5.3</b> — "O que preciso fazer à tarde no açougue?"</summary>
<a id="evidencia-53"></a>

```
Aqui estão as previsões de produção para a tarde no setor de Açougue:
• Hambúrguer (Kg): 16
• Espetinho (Kg): 34
• Frango temp (Kg): 24
• Linguiça (Kg): 22
• Kafta (Kg): 11
• Kit Feijoada (Kg): 15
```

</details>

<details>
<summary><b>5.5</b> — "O que devo produzir de manhã?"</summary>
<a id="evidencia-55"></a>

```
Aqui estão os itens previstos para produção na manhã:
• Pão Francês: 107 Kg
• Pão de queijo: 16 Kg
• Croissant: 8 Kg
• Coxinha: 77 Un
• Enroladinho: 60 Un
• Bolo de chocolate: 9 Kg
• Torta de limão: 4 Kg
• Pudim: 26 Un
• Brigadeiro: 5 Kg
• Beijinho: 5 Kg
• Frango assado: 66 Un
• Marmita: 31 Un
• Lasanha: 11 Kg
• Macarrão: 8 Kg
• Purê de batata: 9 Kg
• Salgadinhos: 2 Kg
• Hot Roll: 3 Porção
• Combo Sushi: 2 Porção
• Sashimi: 2 Porção
• Maki: 2 Porção
• Temaki: 3 Un
• Ceviche: 5 Porção
• Hambúrguer: 13 Kg
• Espetinho: 27 Kg
• Frango temp: 19 Kg
• Linguiça: 18 Kg
• Kafta: 9 Kg
• Kit Feijoada: 12 Kg
• Suco Laranja: 28 L
• Salada Frutas: 12 Kg
• Caldos/Sopas: 2 Kg
• Legumes: 8 Kg
• Salada Verde: 6 Kg
```

</details>

<details>
<summary><b>5.6</b> — "O que devo produzir à noite amanhã na cozinha?"</summary>
<a id="evidencia-56"></a>

```
Aqui estão as previsões de produção para a noite de amanhã na cozinha:
• Marmita: 14 unidades
• Lasanha: 2 Kg
• Macarrão: 2 Kg
• Purê de batata: 2 Kg
• Salgadinhos: 11 Kg
```

</details>

<details>
<summary><b>5.7</b> — "Pedir um período sem histórico de vendas"</summary>
<a id="evidencia-57"></a>

```
Aqui estão as previsões de produção para esta madrugada:
• Pão Francês (Kg): 43
• Pão de queijo (Kg): 7
• Croissant (Kg): 3
• Coxinha (Un): 77
• Enroladinho (Un): 60
• Bolo de chocolate (Kg): 4
• Torta de limão (Kg): 2
• Pudim (Un): 26
• Brigadeiro (Kg): 2
• Beijinho (Kg): 2
• Marmita (Un): 8
• Lasanha (Kg): 4
• Macarrão (Kg): 3
• Purê de batata (Kg): 3
• Salgadinhos (Kg): 16
• Hot Roll (Porção): 39
• Combo Sushi (Porção): 27
• Sashimi (Porção): 13
• Maki (Porção): 22
• Temaki (Un): 35
• Ceviche (Porção): 5
• Hambúrguer (Kg): 4
• Espetinho (Kg): 7
• Frango temp (Kg): 5
• Linguiça (Kg): 5
• Kafta (Kg): 3
• Kit Feijoada (Kg): 3
• Suco Laranja (L): 28
• Salada Frutas (Kg): 12
• Caldos/Sopas (Kg): 25
• Legumes (Kg): 8
• Salada Verde (Kg): 3
```

</details>

<details>
<summary><b>5.8</b> — "O que devo produzir à tarde e à noite na padaria?"</summary>
<a id="evidencia-58"></a>

```
Aqui estão as previsões de produção para a padaria à tarde e à noite:

**Produção da Tarde:**
• Pão Francês: 64 Kg
• Pão de queijo: 10 Kg
• Croissant: 5 Kg
• Coxinha: 102 unidades
• Enroladinho: 80 unidades
• Bolo de chocolate: 6 Kg
• Torta de limão: 7 Kg
• Pudim: 35 unidades
• Brigadeiro: 3 Kg
• Beijinho: 3 Kg

**Produção da Noite:**
• Pão Francês: 43 Kg
• Pão de queijo: 7 Kg
• Croissant: 3 Kg
• Coxinha: 77 unidades
• Enroladinho: 60 unidades
• Bolo de chocolate: 4 Kg
• Torta de limão: 2 Kg
• Pudim: 26 unidades
• Brigadeiro: 2 Kg
• Beijinho: 2 Kg
```

</details>

<details>
<summary><b>8.1</b> — "Quais produtos da empresa trazem mais lucro?"</summary>
<a id="evidencia-81"></a>

```
Aqui estão as informações sobre os produtos:
• O produto com o maior preço de venda listado nos dados disponíveis é o Sashimi (Porção) com R$ 85,00. Não é possível calcular o lucro real, pois os custos dos produtos não foram fornecidos.
```

</details>

<details>
<summary><b>8.2</b> — "Me mostra os 5 produtos mais lucrativos do mercado"</summary>
<a id="evidencia-82"></a>

```
Aqui estão os 5 produtos mais lucrativos do mercado, baseados nos valores de venda:
• Sashimi (Porção): R$ 85,00
• Brigadeiro (Kg): R$ 80,00
• Beijinho (Kg): R$ 80,00
• Bolo de chocolate (Kg): R$ 65,00
• Salgadinhos (Kg): R$ 60,00
```

</details>

<details>
<summary><b>9.1</b> — "Áudio dizendo: "O que devo produzir hoje?""</summary>
<a id="evidencia-91"></a>

```
Aqui estão as previsões de produção para hoje (25/10/2026):
• Pão Francês (Kg): 213 unidades
• Pão de queijo (Kg): 32 unidades
• Croissant (Kg): 15 unidades
• Coxinha (Un): 255 unidades
• Enroladinho (Un): 200 unidades
• Bolo de chocolate (Kg): 18 unidades
• Torta de limão (Kg): 11 unidades
• Pudim (Un): 86 unidades
• Brigadeiro (Kg): 9 unidades
• Beijinho (Kg): 9 unidades
• Frango assado (Un): 132 unidades
• Marmita (Un): 77 unidades
• Lasanha (Kg): 34 unidades
• Macarrão (Kg): 27 unidades
• Purê de batata (Kg): 29 unidades
• Salgadinhos (Kg): 21 unidades
• Hot Roll (Porção): 49 unidades
• Combo Sushi (Porção): 34 unidades
• Sashimi (Porção): 16 unidades
• Maki (Porção): 28 unidades
• Temaki (Un): 43 unidades
• Ceviche (Porção): 16 unidades
• Hambúrguer (Kg): 32 unidades
• Espetinho (Kg): 68 unidades
• Frango temp (Kg): 47 unidades
• Linguiça (Kg): 44 unidades
• Kafta (Kg): 22 unidades
• Kit Feijoada (Kg): 29 unidades
• Suco Laranja (L): 92 unidades
• Salada Frutas (Kg): 37 unidades
• Caldos/Sopas (Kg): 31 unidades
• Legumes (Kg): 25 unidades
• Salada Verde (Kg): 19 unidades
```

</details>

<details>
<summary><b>9.2</b> — "Áudio dizendo: "Quantas unidades devo produzir amanhã na padaria?""</summary>
<a id="evidencia-92"></a>

```
Aqui estão as unidades de produção previstas para amanhã na padaria:
• Pão Francês (Kg): 134 unidades
• Pão de queijo (Kg): 20 unidades
• Croissant (Kg): 9 unidades
• Coxinha (Un): 172 unidades
• Enroladinho (Un): 132 unidades
• Bolo de chocolate (Kg): 9 unidades
• Torta de limão (Kg): 5 unidades
• Pudim (Un): 43 unidades
• Brigadeiro (Kg): 5 unidades
• Beijinho (Kg): 5 unidades
```

</details>

<details>
<summary><b>10.1</b> — "Quanta matéria-prima preciso deixar preparada para amanhã na padaria?"</summary>
<a id="evidencia-101"></a>

```
Aqui estão os itens de matéria-prima necessários para amanhã (26/10/2026):
• Pão Francês (Kg): Farinha de Trigo - 87.10 unidades
• Pão Francês (Kg): Água - 30.48 unidades
• Pão Francês (Kg): Sal - 0.61 unidades
• Pão Francês (Kg): Fermento - 0.01 unidades
• Pão de queijo (Kg): Polvilho - 10.00 unidades
• Pão de queijo (Kg): Queijo Mussarela - 3.00 unidades
• Pão de queijo (Kg): Leite - 0.30 unidades
• Pão de queijo (Kg): Óleo de Soja - 0.02 unidades
• Croissant (Kg): Farinha de Trigo - 4.50 unidades
• Croissant (Kg): Manteiga - 1.80 unidades
• Croissant (Kg): Água - 0.18 unidades
• Croissant (Kg): Açúcar - 0.01 unidades
• Coxinha (Un): Farinha de Trigo - 5.50 unidades
• Coxinha (Un): Frango Desfiado - 0.13 unidades
• Coxinha (Un): Batata - 0.00 unidades
• Coxinha (Un): Óleo de Soja - 0.00 unidades
• Enroladinho (Un): Farinha de Trigo - 5.28 unidades
• Enroladinho (Un): Presunto - 0.06 unidades
• Enroladinho (Un): Queijo Mussarela - 0.00 unidades
• Bolo de chocolate (Kg): Farinha de Trigo - 2.70 unidades
• Bolo de chocolate (Kg): Açúcar - 0.81 unidades
• Bolo de chocolate (Kg): Cacau em Pó - 0.08 unidades
• Bolo de chocolate (Kg): Leite - 0.01 unidades
• Torta de limão (Kg): Leite Condensado - 2.00 unidades
• Torta de limão (Kg): Biscoito Maizena - 0.40 unidades
• Torta de limão (Kg): Limão - 0.08 unidades
• Torta de limão (Kg): Creme de Leite - 0.01 unidades
• Pudim (Un): Leite Condensado - 17.20 unidades
• Pudim (Un): Leite - 6.88 unidades
• Pudim (Un): Ovos - 1.03 unidades
• Pudim (Un): Açúcar - 0.05 unidades
• Brigadeiro (Kg): Leite Condensado - 4.00 unidades
• Brigadeiro (Kg): Cacau em Pó - 0.40 unidades
• Brigadeiro (Kg): Manteiga - 0.04 unidades
• Beijinho (Kg): Leite Condensado - 4.00 unidades
• Beijinho (Kg): Coco Ralado - 0.60 unidades
• Beijinho (Kg): Manteiga - 0.03 unidades
```

</details>

<details>
<summary><b>10.2</b> — "O que preciso separar de ingredientes para amanhã na cozinha?"</summary>
<a id="evidencia-102"></a>

```
Aqui estão os ingredientes necessários para amanhã (26/10/2026):
• Frango assado (Un): Frango Inteiro - 41.00 unidades (Sobra: 239.05 unidades)
• Frango assado (Un): Tempero Pronto - 2.05 unidades (Sobra: 10.98 unidades)
• Marmita (Un): Arroz Branco - 20.70 unidades (Sobra: 51.26 unidades)
• Marmita (Un): Feijão Carioca - 2.07 unidades (Sobra: 37.77 unidades)
• Marmita (Un): Carne Bovina - 0.31 unidades (Sobra: 112.37 unidades)
• Marmita (Un): Batata - 0.03 unidades (Sobra: 103.41 unidades)
• Lasanha (Kg): Massa de Lasanha - 5.40 unidades (Sobra: 12.80 unidades)
• Lasanha (Kg): Carne Bovina Moída - 1.62 unidades (Sobra: 26.15 unidades)
• Lasanha (Kg): Queijo - 0.32 unidades (Sobra: 22.68 unidades)
• Lasanha (Kg): Molho Tomate - 0.06 unidades (Sobra: 42.18 unidades)
• Macarrão (Kg): Macarrão - 7.00 unidades (Sobra: 36.60 unidades)
• Macarrão (Kg): Carne Bovina Moída - 1.40 unidades (Sobra: 26.37 unidades)
• Macarrão (Kg): Molho Tomate - 0.42 unidades (Sobra: 41.82 unidades)
• Purê de batata (Kg): Batata - 12.00 unidades (Sobra: 91.44 unidades)
• Purê de batata (Kg): Leite - 1.20 unidades (Sobra: 8.27 unidades)
• Purê de batata (Kg): Manteiga - 0.12 unidades (Sobra: 8.11 unidades)
• Salgadinhos (Kg): Farinha de Trigo - 7.00 unidades (Sobra: 41.25 unidades)
• Salgadinhos (Kg): Frango Desfiado - 1.40 unidades (Sobra: 11.24 unidades)
• Salgadinhos (Kg): Carne - 0.28 unidades (Sobra: 14.30 unidades)
• Salgadinhos (Kg): Óleo de Soja - 0.03 unidades (Sobra: 8.81 unidades)
```

</details>

<details>
<summary><b>10.3</b> — "Quanto de farinha preciso para amanhã?"</summary>
<a id="evidencia-103"></a>

```
Aqui está a quantidade de farinha de trigo necessária para amanhã:
• Quantidade total de farinha de trigo necessária para amanhã é de 112.08 unidades (considerando as unidades listadas na observação da ferramenta).
```

</details>