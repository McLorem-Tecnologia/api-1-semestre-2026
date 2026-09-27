# Guia de Testes — Sprint 1

Este documento é um **guia para você testar a MIA na prática**, e não um relatório do que já foi testado. A ideia é: você envia cada mensagem sugerida no Telegram, compara com o resultado esperado, anota o que realmente aconteceu e marca o status na tabela do final. Os resultados da execução ficam no [Relatório de Testes - Sprint 1](./Relatório%20de%20Testes%20-%20Sprint%201.md).

## Pré-requisitos antes de começar

- [ ] Ollama aberto, com o modelo `ollama pull gemma4:e2b` baixado
- [ ] Arquivo `.env` configurado em `backend/src/.env` com `TELEGRAM_BOT_KEY` válido
- [ ] `python main.py` rodando sem erros no terminal (verifique se aparece "[IA] Modelos configurados com sucesso.")
- [ ] Bot respondendo a `/start` no Telegram

---

## US01 — Quais produtos devem ser produzidos

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 1.1 | "O que devo produzir hoje?" | Lista só com **nomes** de produtos (sem quantidade), baseada na média de vendas de dias com o mesmo perfil (bom/ruim) de hoje |
| 1.2 | "O que preciso produzir amanhã?" | `converter_data_relativa` deve resolver "amanhã" para a data correta antes de calcular |
| 1.3 | "Quais produtos devo produzir hoje na padaria?" | Lista filtrada só com produtos do setor Padaria |
| 1.4 | "Quais produtos devo produzir no dia 20/09/2026?" | Aceita data explícita no formato `DD/MM/AAAA` (devolvida sem alteração por `converter_data_relativa`) |

---

## US02 — Quantos produtos produzir

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 2.1 | "Quantas unidades devo produzir hoje?" | Lista com nome do produto e quantidade recomendada (média histórica arredondada para cima + 30%) |
| 2.2 | "Quanto de coxinha devo fazer amanhã?" | A tool devolve todos os produtos e o Formatador mostra só a Coxinha. |
| 2.3 | "Quantos produtos da padaria devo produzir hoje?" | Filtra por setor mantendo as quantidades |

---

## US03 — O que foi produzido

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 3.1 | "O que foi produzido ontem na padaria?" | Lista por produto: Total Produzido, Vendas e Descarte, só da Padaria |
| 3.2 | "O que foi produzido ontem no açougue, na padaria e na cozinha?" | Deve conseguir consultar os três setores (o `ReAct` aciona a tool uma vez por setor) e apresentar tudo organizado |
| 3.3 | "O que foi produzido ontem?" | Deve retornar a produção de todos os setores |
| 3.4 | "O que foi produzido ontem? Separe a lista por setores" | Deve retornar a produção de todos os setores, agrupada por setor |
| 3.5 | "O que foi produzido no acugue ontem?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Açougue" mesmo com o erro |

---

## US04 — O que deveria ter sido produzido

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 4.1 | "O que deveria ter sido produzido ontem na padaria?" | Mostra a meta de produção por produto da Padaria, em tom de relatório/cobrança |
| 4.2 | "Qual era a meta de produção de hoje para o açougue?" | Mesmo cálculo, fraseado diferente — verifica se o Classificador de Intenção entende variações de pergunta |
| 4.3 | "Quanto deveria ter sido produzido ontem na padaria?" | Mostra a meta de produção **com quantidade** por produto da Padaria — mesmo comportamento do 4.1, mas fraseado com "Quanto" de forma explícita |

---

## Catálogo de produtos (fora das 4 US, mas testável)

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 5.1 | "Quais produtos vocês têm?" | Lista completa de produtos (`listar_todos_produtos`) |
| 5.2 | "Me dá os detalhes de todos os produtos" | Lista com Nome, Setor e Tempo de preparo |
| 5.3 | "Quais são as informações da coxinha?" | Detalhes de um produto específico |
| 5.4 | "Quais produtos são da cozinha?" | Lista filtrada por setor |

---

## Roteamento e comportamento social (`agentes.py`)

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 6.1 | "Oi" / "Bom dia" | Classificador identifica `SAUDACAO`; resposta curta e simpática, sem acionar nenhuma tool |
| 6.2 | "Tchau" / "Obrigado!" | Mesma rota `SAUDACAO` |
| 6.3 | "Qual é a capital da França?" (fora do escopo) | Classificador identifica `INVALIDO`; resposta explicando que só responde sobre produção/vendas, sem tentar adivinhar |
| 6.4 | Enviar um áudio ou uma foto | O bot responde com a mensagem fixa de formato não suportado, sem acionar a IA. |

---

## Formatação da resposta

| ID | O que verificar | Resultado esperado |
|---|---|---|
| 7.1 | Listas na resposta | Sempre usam `•`, nunca `*` |
| 7.2 | Início da resposta | Nunca começa repetindo saudação ("Olá! Aqui está...") |
| 7.3 | Pergunta com múltiplos setores | Cada setor aparece claramente separado (ver seção "separar por mensagem", se já implementado) |

---

## Tabela de registro (preencha ao testar)

| Caso | Mensagem enviada | Resultado obtido | Status | Observações |
|---|---|---|---|---|
| 1.1 | Quais produtos devo produzir hoje? |  |  |  |
| 1.2 | Quais produtos preciso produzir amanhã? |  |  |  |
| 1.3 | Quais produtos devo produzir hoje na padaria? |  |  |  |
| 1.4 | Quais produtos devo produzir no dia 20/09/2026? |  |  |  |
| 2.1 | Quantas unidades devo produzir hoje? |  |  |  |
| 2.2 | Quanto de coxinha devo fazer amanhã? |  |  |  |
| 2.3 | Quantos produtos da padaria devo produzir hoje? |  |  |  |
| 3.1 | O que foi produzido ontem na padaria? |  |  |  |
| 3.2 | O que foi produzido ontem no açougue, na padaria e na cozinha? |  |  |  |
| 3.3 | O que foi produzido ontem? |  |  |  |
| 3.4 | O que foi produzido ontem? Separe a lista por setores |  |  |  |
| 3.5 | O que foi produzido no acugue ontem? |  |  |  |
| 4.1 | O que deveria ter sido produzido ontem na padaria? |  |  |  |
| 4.2 | Qual era a meta de produção de hoje para o açougue? |  |  |  |
| 4.3 | Quanto deveria ter sido produzido ontem na padaria? |  |  |  |
| 5.1 | Quais produtos vocês têm? |  |  |  |
| 5.2 | Me dá os detalhes de todos os produtos |  |  |  |
| 5.3 | Quais são as informações da coxinha? |  |  |  |
| 5.4 | Quais produtos são da cozinha? |  |  |  |
| 6.1 | "Oi" / "Bom dia" |  |  |  |
| 6.2 | "Tchau" / "Obrigado!" |  |  |  |
| 6.3 | Qual é a capital da França? |  |  |  |
| 6.4 | Enviar um áudio ou uma foto |  |  |  |
| 7.1 | Listas na resposta |  |  |  |
| 7.2 | Início da resposta |  |  |  |
| 7.3 | Pergunta com múltiplos setores |  |  |  |