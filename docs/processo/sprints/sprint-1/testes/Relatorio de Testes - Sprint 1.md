# Relatório de Testes — Sprint 1

Este documento registra a execução manual dos testes da MIA na Sprint 1: cada linha da tabela de registro mostra a mensagem enviada no Telegram e o resultado obtido. As evidências completas (respostas longas do bot) estão no final do documento.

## Pré-requisitos antes de começar

- [x] Ollama aberto, com o modelo `ollama pull gemma4:e2b` baixado
- [x] Arquivo `.env` configurado em `backend/src/.env` com `TELEGRAM_BOT_KEY` válido
- [x] `python main.py` rodando sem erros no terminal (verifique se aparece "[IA] Modelos configurados com sucesso.")
- [x] Bot respondendo a `/start` no Telegram

---

## US01 — Quais produtos devem ser produzidos

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 1.1 | "O que devo produzir hoje?" | Lista só com **nomes** de produtos (sem quantidade), baseada na média de vendas de dias com o mesmo perfil (bom/ruim) de hoje |
| 1.2 | "O que preciso produzir amanhã?" | `converter_data_relativa` deve resolver "amanhã" para a data correta antes de calcular |
| 1.3 | "Quais produtos devo produzir hoje na padaria?" | Lista filtrada só com produtos do setor Padaria |
| 1.4 | "Quais produtos devo produzir no dia 20/09/2026?" | Aceita data explícita no formato `DD/MM/AAAA` sem passar por `converter_data_relativa` |

---

## US02 — Quantos produtos produzir

| ID | Mensagem para enviar | Resultado esperado |
|---|---|---|
| 2.1 | "Quantas unidades devo produzir hoje?" | Lista com nome do produto **e** quantidade recomendada (média arredondada pra cima) |
| 2.2 | "Quanto de coxinha devo fazer amanhã?" | Consegue filtrar por um produto específico dentro da resposta |
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

---

## Catálogo de produtos (fora das 4 US, mas testável)

| # | Mensagem para enviar | Resultado esperado |
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
| 6.4 | Enviar um áudio ou uma foto | O bot deve ignorar silenciosamente (não travar nem responder algo sem sentido) |

---

## Formatação da resposta

| ID | O que verificar | Resultado esperado |
|---|---|---|
| 7.1 | Listas na resposta | Sempre usam `•`, nunca `*` |
| 7.2 | Início da resposta | Nunca começa repetindo saudação ("Olá! Aqui está...") |
| 7.3 | Pergunta com múltiplos setores | Cada setor aparece claramente separado (ver seção "separar por mensagem", se já implementado) |

---

## Tabela de Registro dos Testes

| Caso | Mensagem enviada | Resultado obtido |
| --- | --- | --- |
| 1.1 | Quais produtos devo produzir hoje? | Lista os 25 produtos que devem ser produzidos hoje. Ver [evidência completa](#evidencia-11) |
| 1.2 | Quais produtos preciso produzir amanhã? | Lista os 25 produtos e resolve "amanhã" para a data correta (27/09/2026). Ver [evidência completa](#evidencia-12) |
| 1.3 | Quais produtos devo produzir hoje na padaria? | Lista os 5 produtos da padaria apenas. Ver [evidência completa](#evidencia-13) |
| 1.4 | Quais produtos devo produzir no dia 20/09/2026? | Lista os 25 produtos com a média do que foi produzido em dias parecidos mais 30%. Ver [evidência completa](#evidencia-14) |
| 2.1 | Quantas unidades devo produzir hoje? | Lista os 25 produtos que devem ser produzidos hoje com a quantidade. Ver [evidência completa](#evidencia-21) |
| 2.2 | Quanto de coxinha devo fazer amanhã? | Retornou apenas a 'Coxinha' e a quantidade. Ver [evidência completa](#evidencia-22) |
| 2.3 | Quantos produtos da padaria devo produzir hoje? | Lista os 5 produtos da padaria apenas com a quantidade. Ver [evidência completa](#evidencia-23) |
| 3.1 | O que foi produzido ontem na padaria? | Listou os 5 produtos da padaria com o Total Produzido e a explicação de quantos realmente foram vendidos e quantos foram descartados. Ver [evidência completa](#evidencia-31) |
| 3.2 | O que foi produzido ontem no açougue, na padaria e na cozinha? | Lista os produtos de cada setor de forma separada trazendo as mesmas informações do caso 3.1. Ver [evidência completa](#evidencia-32) |
| 3.3 | O que foi produzido ontem? | Lista os 25 produtos (750 un. no total). Ver [evidência completa](#evidencia-33) |
| 3.4 | O que foi produzido ontem? Separe a lista por setores | Lista os 25 produtos separando eles por setores (750 un. no total). Ver [evidência completa](#evidencia-34) |
| 3.5 | O que foi produzido no acugue ontem? | `normalizar_setor` corrigiu corretamente para "Açougue" mesmo com o erro. Ver [evidência completa](#evidencia-35) |
| 4.1 | O que deveria ter sido produzido ontem na padaria? | Lista os 5 produtos que deveria ter sido produzido pela padaria no dia anterior. Ver [evidência completa](#evidencia-41) |
| 4.2 | Qual era a meta de produção de hoje para o açougue? | Lista os 5 produtos que deveria ter sido produzido pelo açougue no dia de hoje. Ver [evidência completa](#evidencia-42) |
| 5.1 | Quais produtos vocês têm? | Lista os 25 produtos catalogados em `produtos_mercado.csv`. Ver [evidência completa](#evidencia-51) |
| 5.2 | Me dá os detalhes de todos os produtos | Listou os 25 produtos assim como no caso 5.1 com o adicional das informações: Produto, Setor e Tempo de preparo de cada produto. Ver [evidência completa](#evidencia-52) |
| 5.3 | Quais são as informações da coxinha? | Retornou as informações: Produto, Setor e Tempo de preparo. Ver [evidência completa](#evidencia-53) |
| 5.4 | Quais produtos são da cozinha? | Lista os 5 produtos do setor especifico no caso cozinha. Ver [evidência completa](#evidencia-54) |
| 6.1 | "Oi" / "Bom dia" | Retorna: 'Oi! Como posso ajudar na produção do supermercado hoje?' / 'Bom dia! Como posso ajudar na produção do supermercado hoje?' |
| 6.2 | "Tchau" / "Obrigado!" | Retorna: 'Tchau! Tenha um ótimo dia.' / 'De nada! Estou aqui para ajudar no que precisar.' |
| 6.3 | Qual é a capital da França? | Retorna: 'Desculpe, Meu sistema é restrito à análise e produção do supermercado.' |
| 6.4 | Enviar um áudio ou uma foto | Retorna: `Desculpe, no momento eu não suporto esse formato enviado. Por favor, me envie apenas mensagens de texto!` |
| 7.1 | Listas na resposta | Como podemos ver nos casos de Listasm, está corrigindo os '*' para '•' corretamente |
| 7.2 | Ínicio da resposta | Como podemos ver em todos os teste, ela não está dizendo olá para cada mensagem (não está repetindo saudações) |
| 7.3 | Pergunta com múltiplos setores | Como podemos ver no caso [3.4](#evidencia-34) e [3.2](#evidencia-32) está respondendo corretamente |

---

## Evidências Completas

Respostas longas do bot (que não cabem na tabela) ficam guardadas aqui, uma por caso de teste, dentro de um bloco recolhível.

<a id="evidencia-11"></a>
<details>
<summary><b>1.1</b> — "Quais produtos devo produzir hoje?"</summary>

```
Aqui estão os produtos que você pode produzir hoje:
• Beijinho
• Bolo de chocolate
• Brigadeiro
• Ceviche
• Coxinha
• Croissant
• Enroladinho de presunto e queijo
• Espetinho de carne
• Frango assado
• Frango temperado
• Hambúrguer artesanal
• Kafta
• Lasanha
• Linguiça artesanal
• Macarrão à bolonhesa
• Maki
• Marmita de arroz e feijão
• Pudim
• Purê de batata
• Pão de queijo
• Pão francês
• Sashimi
• Sushi
• Temaki
• Torta de limão
```

</details>

<a id="evidencia-12"></a>
<details>
<summary><b>1.2</b> — "Quais produtos preciso produzir amanhã?"</summary>

Aqui estão os produtos que devem ser produzidos para o dia amanhã (27/09/2026):

**Mesma lista da [1.1 — "Quais produtos devo produzir hoje?"](#evidencia-11)**

</details>

<a id="evidencia-13"></a>
<details>
<summary><b>1.3</b> — "Quais produtos devo produzir hoje na padaria?"</summary>

```
Aqui estão os produtos disponíveis para produção hoje na padaria:
• Coxinha
• Croissant
• Enroladinho de presunto e queijo
• Pão de queijo
• Pão francês
```

</details>

<a id="evidencia-14"></a>
<details>
<summary><b>1.4</b> — "Quais produtos devo produzir no dia 20/09/2026?"</summary>

```
Aqui estão os produtos que você deve produzir:
• Beijinho
• Bolo de chocolate
• Brigadeiro
• Ceviche
• Coxinha
• Croissant
• Enroladinho de presunto e queijo
• Espetinho de carne
• Frango assado
• Frango temperado
• Hambúrguer artesanal
• Kafta
• Lasanha
• Linguiça artesanal
• Macarrão à bolonhesa
• Maki
• Marmita de arroz e feijão
• Pudim
• Purê de batata
• Pão de queijo
• Pão francês
• Sashimi
• Sushi
• Temaki
• Torta de limão
```

</details>

---

<a id="evidencia-21"></a>
<details>
<summary><b>2.1</b> — "Quantas unidades devo produzir hoje?"</summary>

```
Aqui estão as previsões de produção para hoje (26/09/2026):
• Beijinho: 7 unidades
• Bolo de chocolate: 7 unidades
• Brigadeiro: 7 unidades
• Ceviche: 8 unidades
• Coxinha: 8 unidades
• Croissant: 7 unidades
• Enroladinho de presunto e queijo: 8 unidades
• Espetinho de carne: 8 unidades
• Frango assado: 7 unidades
• Frango temperado: 7 unidades
• Hambúrguer artesanal: 7 unidades
• Kafta: 8 unidades
• Lasanha: 7 unidades
• Linguiça artesanal: 7 unidades
• Macarrão à bolonhesa: 7 unidades
• Maki: 8 unidades
• Marmita de arroz e feijão: 7 unidades
• Pudim: 7 unidades
• Purê de batata: 7 unidades
• Pão de queijo: 7 unidades
• Pão francês: 7 unidades
• Sashimi: 7 unidades
• Sushi: 7 unidades
• Temaki: 8 unidades
• Torta de limão: 8 unidades
```

</details>

<a id="evidencia-22"></a>
<details>
<summary><b>2.2</b> — "Quanto de coxinha devo fazer amanhã"</summary>

```
Aqui estão as quantidades de produção solicitadas:
• Coxinha: 8 unidades
```

</details>

<a id="evidencia-23"></a>
<details>
<summary><b>2.3</b> — "Quantos produtos da padaria devo produzir hoje?"</summary>

```
Aqui estão as quantidades de produtos da padaria que você deve produzir hoje:
• Coxinha: 8 unidades
• Croissant: 7 unidades
• Enroladinho de presunto e queijo: 8 unidades
• Pão de queijo: 7 unidades
• Pão francês: 7 unidades
```

</details>

---

<a id="evidencia-31"></a>
<details>
<summary><b>3.1</b> — "O que foi produzido ontem na padaria?"</summary>

```
Aqui está o relatório de produção da padaria de ontem (25/09/2026):

• Coxinha: Total Produzido: 30 (Vendas: 13, Descarte: 17)
• Croissant: Total Produzido: 30 (Vendas: 9, Descarte: 21)
• Enroladinho de presunto e queijo: Total Produzido: 30 (Vendas: 19, Descarte: 11)
• Pão de queijo: Total Produzido: 30 (Vendas: 12, Descarte: 18)
• Pão francês: Total Produzido: 30 (Vendas: 12, Descarte: 18)

No total, foram produzidas 150 unidades.
```

</details>

<a id="evidencia-32"></a>
<details>
<summary><b>3.2</b> — "O que foi produzido ontem no açougue, na padaria e na cozinha?"</summary>

```
Aqui estão os detalhes da produção realizada ontem (25/09/2026) no açougue, na padaria e na cozinha:

• Açougue:
• Espetinho de carne: 30 produzidos (Vendas: 18, Descarte: 12)
• Frango temperado: 30 produzidos (Vendas: 21, Descarte: 9)
• Hambúrguer artesanal: 30 produzidos (Vendas: 18, Descarte: 12)
• Kafta: 30 produzidos (Vendas: 16, Descarte: 14)
• Linguiça artesanal: 30 produzidos (Vendas: 15, Descarte: 15)

• Padaria:
• Coxinha: 30 produzidos (Vendas: 13, Descarte: 17)
• Croissant: 30 produzidos (Vendas: 9, Descarte: 21)
• Enroladinho de presunto e queijo: 30 produzidos (Vendas: 19, Descarte: 11)
• Pão de queijo: 30 produzidos (Vendas: 12, Descarte: 18)
• Pão francês: 30 produzidos (Vendas: 12, Descarte: 18)

• Cozinha/Rotisseria:
• Frango assado: 30 produzidos (Vendas: 15, Descarte: 15)
• Lasanha: 30 produzidos (Vendas: 13, Descarte: 17)
• Macarrão à bolonhesa: 30 produzidos (Vendas: 17, Descarte: 13)
• Marmita de arroz e feijão: 30 produzidos (Vendas: 15, Descarte: 15)
• Purê de batata: 30 produzidos (Vendas: 13, Descarte: 17)
```

</details>

<a id="evidencia-33"></a>
<details>
<summary><b>3.3</b> — "O que foi produzido ontem?"</summary>

```
Aqui estão os detalhes do que foi produzido ontem (24/09/2026):

• Beijinho | Total Produzido: 30 (Vendas: 9, Descarte: 21)
• Bolo de chocolate | Total Produzido: 30 (Vendas: 10, Descarte: 20)
• Brigadeiro | Total Produzido: 30 (Vendas: 8, Descarte: 22)
• Ceviche | Total Produzido: 30 (Vendas: 5, Descarte: 25)
• Coxinha | Total Produzido: 30 (Vendas: 14, Descarte: 16)
• Croissant | Total Produzido: 30 (Vendas: 17, Descarte: 13)
• Enroladinho de presunto e queijo | Total Produzido: 30 (Vendas: 19, Descarte: 11)
• Espetinho de carne | Total Produzido: 30 (Vendas: 23, Descarte: 7)
• Frango assado | Total Produzido: 30 (Vendas: 17, Descarte: 13)
• Frango temperado | Total Produzido: 30 (Vendas: 18, Descarte: 12)
• Hambúrguer artesanal | Total Produzido: 30 (Vendas: 17, Descarte: 13)
• Kafta | Total Produzido: 30 (Vendas: 17, Descarte: 13)
• Lasanha | Total Produzido: 30 (Vendas: 17, Descarte: 13)
• Linguiça artesanal | Total Produzido: 30 (Vendas: 17, Descarte: 13)
• Macarrão à bolonhesa | Total Produzido: 30 (Vendas: 18, Descarte: 12)
• Maki | Total Produzido: 30 (Vendas: 7, Descarte: 23)
• Marmita de arroz e feijão | Total Produzido: 30 (Vendas: 15, Descarte: 15)
• Pudim | Total Produzido: 30 (Vendas: 7, Descarte: 23)
• Purê de batata | Total Produzido: 30 (Vendas: 17, Descarte: 13)
• Pão de queijo | Total Produzido: 30 (Vendas: 11, Descarte: 19)
• Pão francês | Total Produzido: 30 (Vendas: 11, Descarte: 19)
• Sashimi | Total Produzido: 30 (Vendas: 11, Descarte: 19)
• Sushi | Total Produzido: 30 (Vendas: 4, Descarte: 26)
• Temaki | Total Produzido: 30 (Vendas: 4, Descarte: 26)
• Torta de limão | Total Produzido: 30 (Vendas: 5, Descarte: 25)

No total foram produzidas 750 unidades.
```

</details>

<a id="evidencia-34"></a>
<details>
<summary><b>3.4</b> — "O que foi produzido ontem? Separe a lsita por setores"</summary>

```
Aqui estão os itens produzidos ontem, separados por setor:

• Setor: Açougue
    • Hambúrguer artesanal: Produzido 30 (Vendas: 17, Descarte: 13)
    • Espetinho de carne: Produzido 30 (Vendas: 23, Descarte: 7)
    • Frango temperado: Produzido 30 (Vendas: 18, Descarte: 12)
    • Linguiça artesanal: Produzido 30 (Vendas: 17, Descarte: 13)
    • Kafta: Produzido 30 (Vendas: 17, Descarte: 13)

• Setor: Padaria
    • Pão francês: Produzido 30 (Vendas: 11, Descarte: 19)
    • Pão de queijo: Produzido 30 (Vendas: 11, Descarte: 19)
    • Croissant: Produzido 30 (Vendas: 17, Descarte: 13)
    • Coxinha: Produzido 30 (Vendas: 14, Descarte: 16)
    • Enroladinho de presunto e queijo: Produzido 30 (Vendas: 19, Descarte: 11)

• Setor: Cozinha/Rotisseria
    • Marmita de arroz e feijão: Produzido 30 (Vendas: 15, Descarte: 15)
    • Frango assado: Produzido 30 (Vendas: 17, Descarte: 13)
    • Lasanha: Produzido 30 (Vendas: 17, Descarte: 13)
    • Macarrão à bolonhesa: Produzido 30 (Vendas: 18, Descarte: 12)
    • Purê de batata: Produzido 30 (Vendas: 17, Descarte: 13)

• Setor: Peixaria
    • Sushi: Produzido 30 (Vendas: 4, Descarte: 26)
    • Sashimi: Produzido 30 (Vendas: 11, Descarte: 19)
    • Maki: Produzido 30 (Vendas: 7, Descarte: 23)
    • Ceviche: Produzido 30 (Vendas: 5, Descarte: 25)

• Setor: Confeitaria
    • Bolo de chocolate: Produzido 30 (Vendas: 10, Descarte: 20)
    • Pudim: Produzido 30 (Vendas: 7, Descarte: 23)
    • Torta de limão: Produzido 30 (Vendas: 5, Descarte: 25)
    • Brigadeiro: Produzido 30 (Vendas: 8, Descarte: 22)
    • Beijinho: Produzido 30 (Vendas: 9, Descarte: 21)

Total Geral de Unidades Produzidas: 750 unidades
```

</details>

<a id="evidencia-35"></a>
<details>
<summary><b>3.5</b> — "O que foi produzido no acugue ontem? (erro de digitação proposital)"</summary>

```
Aqui está o relatório de produção do açougue realizado ontem (25/09/2026):
• Espetinho de carne: 30 produzidos (Vendas: 18, Descarte: 12)
• Frango temperado: 30 produzidos (Vendas: 21, Descarte: 9)
• Hambúrguer artesanal: 30 produzidos (Vendas: 18, Descarte: 12)
• Kafta: 30 produzidos (Vendas: 16, Descarte: 14)
• Linguiça artesanal: 30 produzidos (Vendas: 15, Descarte: 15)
No total, foram produzidas 150 unidades.
```

</details>

---

<a id="evidencia-41"></a>
<details>
<summary><b>4.1</b> — "O que deveria ter sido produzido ontem na padaria?"</summary>

```
Aqui estão os produtos que deveriam ter sido produzidos ontem na padaria:
• Coxinha
• Croissant
• Enroladinho de presunto e queijo
• Pão de queijo
• Pão francês
```

</details>

<a id="evidencia-42"></a>
<details>
<summary><b>4.2</b> — "Qual era a meta de produção de hoje para o açougue?"</summary>

```
Aqui estão as metas de produção que deveriam ter sido atingidas no dia 26/09/2026 para o setor de Açougue:
• Espetinho de carne: 8 unidades
• Frango temperado: 7 unidades
• Hambúrguer artesanal: 7 unidades
• Kafta: 8 unidades
• Linguiça artesanal: 7 unidades
```

</details>

---

<a id="evidencia-51"></a>
<details>
<summary><b>5.1</b> — "Quais produtos vocês tem?"</summary>

```
Aqui estão os produtos disponíveis:
• Hambúrguer artesanal
• Espetinho de carne
• Frango temperado
• Linguiça artesanal
• Kafta
• Pão francês
• Pão de queijo
• Croissant
• Coxinha
• Enroladinho de presunto e queijo
• Marmita de arroz e feijão
• Frango assado
• Lasanha
• Macarrão à bolonhesa
• Purê de batata
• Sushi
• Sashimi
• Maki
• Temaki
• Ceviche
• Bolo de chocolate
• Pudim
• Torta de limão
• Brigadeiro
• Beijinho
```

</details>

<a id="evidencia-52"></a>
<details>
<summary><b>5.2</b> — "Me dá os detalhes de todos os produtos"</summary>

```
Aqui estão os detalhes de todos os produtos e seus tempos de preparo:

• Hambúrguer artesanal: Tempo de preparo de 5 min (Setor: Açougue)
• Espetinho de carne: Tempo de preparo de 4 min (Setor: Açougue)
• Frango temperado: Tempo de preparo de 3 min (Setor: Açougue)
• Linguiça artesanal: Tempo de preparo de 5 min (Setor: Açougue)
• Kafta: Tempo de preparo de 5 min (Setor: Açougue)
• Pão francês: Tempo de preparo de 3 min (Setor: Padaria)
• Pão de queijo: Tempo de preparo de 4 min (Setor: Padaria)
• Croissant: Tempo de preparo de 5 min (Setor: Padaria)
• Coxinha: Tempo de preparo de 5 min (Setor: Padaria)
• Enroladinho de presunto e queijo: Tempo de preparo de 5 min (Setor: Padaria)
• Marmita de arroz e feijão: Tempo de preparo de 5 min (Setor: Cozinha/Rotisseria)
• Frango assado: Tempo de preparo de 5 min (Setor: Cozinha/Rotisseria)
• Lasanha: Tempo de preparo de 5 min (Setor: Cozinha/Rotisseria)
• Macarrão à bolonhesa: Tempo de preparo de 5 min (Setor: Cozinha/Rotisseria)
• Purê de batata: Tempo de preparo de 4 min (Setor: Cozinha/Rotisseria)
• Sushi: Tempo de preparo de 3 min (Setor: Peixaria)
• Sashimi: Tempo de preparo de 2 min (Setor: Peixaria)
• Maki: Tempo de preparo de 3 min (Setor: Peixaria)
• Temaki: Tempo de preparo de 4 min (Setor: Peixaria)
• Ceviche: Tempo de preparo de 5 min (Setor: Peixaria)
• Bolo de chocolate: Tempo de preparo de 5 min (Setor: Confeitaria)
• Pudim: Tempo de preparo de 5 min (Setor: Confeitaria)
• Torta de limão: Tempo de preparo de 5 min (Setor: Confeitaria)
• Brigadeiro: Tempo de preparo de 3 min (Setor: Confeitaria)
• Beijinho: Tempo de preparo de 3 min (Setor: Confeitaria)
```

</details>

<a id="evidencia-53"></a>
<details>
<summary><b>5.3</b> — "Quais são as informações da coxinha?"</summary>

```
Aqui estão as informações da coxinha:
• Produto: Coxinha
• Setor: Padaria
• Tempo de preparo: 5 min
```

</details>

<a id="evidencia-54"></a>
<details>
<summary><b>5.4</b> — "Quais produtos são da cozinha?"</summary>

```
Aqui estão os produtos da cozinha:
• Marmita de arroz e feijão
• Frango assado
• Lasanha
• Macarrão à bolonhesa
• Purê de batata
```

</details>