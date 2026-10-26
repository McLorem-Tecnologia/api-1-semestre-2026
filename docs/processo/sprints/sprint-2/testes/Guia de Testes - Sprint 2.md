# Guia de Testes — Sprint 2

Este documento é um **guia para você testar a MIA na prática**, e não um relatório do que já foi testado. A ideia é: você envia cada mensagem sugerida no Telegram, compara com o resultado esperado, anota o que realmente aconteceu e marca o status na tabela do final. Os resultados da execução serão registrados no [Relatório de Testes da Sprint 2](./Relatório%20de%20Testes%20-%20Sprint%202.md), criado ao final da execução.

A Sprint 2 reúne as User Stories 05 a 12 (as US09 a US12 vieram da antiga Sprint 3, que foi fundida a esta).

> **Casos transversais:** os casos 0.x continuam a numeração da Sprint 1. Reexecute também os casos 0.1.1 a 0.1.4, 0.2.1 a 0.2.4 e 0.3.1 a 0.3.3 (catálogo, saudação, despedida, fora de escopo, formato não suportado e formatação básica), que valem para todas as sprints; abaixo estão apenas os novos casos 0.2.5 em diante e 0.3.4 em diante.

## Pré-requisitos antes de começar

- [ ] Ollama aberto, com o modelo `ollama pull gemma4:e2b` baixado
- [ ] Arquivo `.env` configurado em `backend/src/.env` com `TELEGRAM_BOT_KEY` válido
- [ ] `python main.py` rodando sem erros no terminal (verifique se aparece "[IA] Modelos configurados com sucesso.")
- [ ] Bot respondendo a `/start` no Telegram
- [ ] CSVs de vendas com a **informação de horário** (ou regra para derivar o período do dia) disponíveis em `backend/dados/` (definição da US05)
- [ ] CSVs com **preço de venda** e **custo unitário** dos produtos disponíveis em `backend/dados/` (definição das US06, US07 e US08)
- [ ] Solução de transcrição de áudio instalada e funcionando localmente (definida no Planning da US09)
- [ ] CSVs de **matéria-prima** (consumo por produto e estoque por setor) disponíveis em `backend/dados/` (definição das US10 e US11)
- [ ] Registro de **transferências entre setores**, com motivo, disponível em `backend/dados/` (definição da US12)
- [ ] Celular com Telegram para gravar as mensagens de voz

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

| ID  | Mensagem para enviar                                                      | Resultado esperado                                                                                                                                                                                              |
| --- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5.1 | "O que eu devo produzir de manhã na padaria?"                             | Produtos da Padaria (10 produtos) a produzir na manhã, com a quantidade e a unidade de medida de cada um (Kg, Un, Porção ou L)                                                                                  |
| 5.2 | "O que produzir em cada período do dia na padaria?"                       | Produtos e quantidades separados por período (manhã, tarde e noite), no mesmo formato para todos os períodos. Cada período é projetado separadamente, então a soma pode divergir da previsão do dia (caso 13.2) |
| 5.3 | "O que preciso fazer à tarde no açougue?"                                 | Mesmo cálculo, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta                                                                                                                  |
| 5.4 | "O que devo produzir de manhã na padaira?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro                                                                                                                                                |
| 5.5 | "O que devo produzir de manhã?" (sem informar o setor)                    | Sem setor, a MIA traz os produtos de todos os setores (33 produtos) no período da manhã; sem data, assume hoje                                                                                                  |
| 5.6 | "O que devo produzir à noite amanhã na cozinha?"                          | `converter_data_relativa` resolve "amanhã" e a resposta traz só o período da noite, só da Cozinha (5 produtos)                                                                                                  |
| 5.7 | Pedir um período sem histórico de vendas (ex.: madrugada)                 | `converter_periodo` converte "madrugada" em "noite" (período mais próximo) e a resposta usa os dados da noite; o ideal é a MIA avisar que usou a noite                                                          |
| 5.8 | "O que devo produzir à tarde e à noite na padaria?"                       | Combinação de períodos: cada produto da Padaria com as sublinhas de tarde e noite, sem a manhã                                                                                                                  |

---

## US06 — Reais descartados em cada setor (gerente)

| ID  | Mensagem para enviar                                                                          | Resultado esperado                                                                                                                                                                                         |
| --- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 6.1 | "Quantos reais foram descartados no dia 01/10/2026 em cada setor?"                            | Valor em R$ de cada setor (Padaria, Cozinha, Peixaria, Açougue e Processados). A tool calcula um setor por vez, então a MIA consulta setor a setor. Se apresentar um total geral, ele é a soma dos setores |
| 6.2 | "Quantos reais foram descartados no dia 01/10/2026 na padaria?"                               | Um único valor em R$ da Padaria, no formato "Custo total do desperdício ontem (dd/mm/aaaa) (Setor: Padaria): R$ x". A tool devolve só o total, sem detalhe por produto                                     |
| 6.3 | "Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?"                        | Valor em R$ do período para a Peixaria ("no período de 01/09/2026 a 15/09/2026"); testa `data_inicio`, `data_fim` e setor juntos                                                                           |
| 6.4 | "Quantos reais foram descartados no acugue no dia 01/10/2026?" (erro de digitação proposital) | `normalizar_setor` corrige para "Açougue" e a resposta mostra "(Setor: Açougue)"                                                                                                                           |
| 6.5 | "Quantos reais foram descartados no dia 01/10/2026?" (sem informar o setor)                   | Total da empresa inteira (todos os setores somados), sem "(Setor: ...)" na frase                                                                                                                           |
| 6.7 | "Quantos reais foram descartados em 01/01/2020?" (data sem registros)                         | Hoje a tool devolve R$ 0,00; decidir no Planning se a MIA deve avisar que não há registros nessa data                                                                                                      |

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

## Tabela de registro (preencha ao testar)

| Caso  | Mensagem enviada                                                                       | Resultado obtido | Status | Observações |
| ----- | -------------------------------------------------------------------------------------- | ---------------- | :----: | ----------- |
| 0.2.5 | Quanto devo produzir amanhã?                                                           |                  |        |             |
| 0.2.6 | Quanto lucro a concorrência teve?                                                      |                  |        |             |
| 0.3.4 | Valores monetários                                                                     |                  |        |             |
| 0.3.5 | Quantidades de matéria-prima                                                           |                  |        |             |
| 0.3.6 | Resposta a um áudio                                                                    |                  |        |             |
| 0.3.7 | Resposta por período do dia                                                            |                  |        |             |
| 5.1   | O que eu devo produzir de manhã na padaria?                                            |                  |        |             |
| 5.2   | O que produzir em cada período do dia na padaria?                                      |                  |        |             |
| 5.3   | O que preciso fazer à tarde no açougue?                                                |                  |        |             |
| 5.4   | O que devo produzir de manhã na padaira?                                               |                  |        |             |
| 5.5   | O que devo produzir de manhã?                                                          |                  |        |             |
| 5.6   | O que devo produzir à noite amanhã na cozinha?                                         |                  |        |             |
| 5.7   | Pedir um período sem histórico de vendas                                               |                  |        |             |
| 5.8   | O que devo produzir à tarde e à noite na padaria?                                      |                  |        |             |
| 6.1   | Quantos reais foram descartados no dia 01/10/2026 em cada setor?                       |                  |        |             |
| 6.2   | Quantos reais foram descartados no dia 01/10/2026 na padaria?                          |                  |        |             |
| 6.3   | Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?                   |                  |        |             |
| 6.4   | Quantos reais foram descartados no acugue no dia 01/10/2026?                           |                  |        |             |
| 6.5   | Quantos reais foram descartados no dia 01/10/2026?                                     |                  |        |             |
| 6.6   | Quantos reais foram descartados em 01/01/2020?                                         |                  |        |             |
| 7.1   | Quantos reais foram descartados em 07/04/2026 na empresa toda?                         |                  |        |             |
| 7.2   | Qual foi o custo total de desperdício em setembro?                                     |                  |        |             |
| 7.3   | Quantos reais foram descartados no dia 01/10/2026? Separe por setores                  |                  |        |             |
| 8.1   | Quais produtos da empresa trazem mais lucro?                                           |                  |        |             |
| 8.2   | Me mostra os 5 produtos mais lucrativos do mercado                                     |                  |        |             |
| 8.3   | Verificação cruzada: calcular à mão o lucro de um produto do caso 8.1 a partir dos CSV |                  |        |             |
| 9.1   | Áudio dizendo: "O que devo produzir hoje?"                                             |                  |        |             |
| 9.2   | Áudio dizendo: "Quantas unidades devo produzir amanhã na padaria?"                     |                  |        |             |
| 9.3   | Áudio dizendo: "Quanto de coxinha devo fazer amanhã?" em ambiente com ruído            |                  |        |             |
| 9.4   | Áudio vazio ou só com silêncio                                                         |                  |        |             |
| 9.5   | Áudio dizendo: "Qual é a capital da França?"                                           |                  |        |             |
| 9.6   | Enviar a mesma pergunta digitada e depois por áudio                                    |                  |        |             |
| 9.7   | Enviar uma foto                                                                        |                  |        |             |
| 9.8   | Após os testes, conferir a pasta de arquivos temporários da máquina                    |                  |        |             |
| 9.9   | Áudio dizendo: "Quantos reais foram descartados no dia 01/10/2026 em cada setor?"      |                  |        |             |
| 10.1  | Quanta matéria-prima preciso deixar preparada para amanhã na padaria?                  |                  |        |             |
| 10.2  | O que preciso separar de ingredientes para amanhã na cozinha?                          |                  |        |             |
| 10.3  | Quanto de farinha preciso para amanhã?                                                 |                  |        |             |
| 10.4  | Quanta matéria-prima preciso para amanhã?                                              |                  |        |             |
| 10.5  | Quanta matéria-prima preciso para a padaira amanhã?                                    |                  |        |             |
| 10.6  | Verificação cruzada: comparar com "Quantas unidades devo produzir amanhã na padaria?"  |                  |        |             |