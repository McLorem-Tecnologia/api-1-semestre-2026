# Relatório de Testes — MIA (Regressão completa)

## Objetivo

Registrar uma nova execução de regressão funcional das capacidades das Sprints 1, 2 e 3. Resultados e evidências das rodadas anteriores foram removidos para que os critérios sejam testados novamente após as mudanças em matéria-prima e na organização das tools.

## Identificação da execução

| Item | Valor |
| --- | --- |
| Data | 22/11/2026 |
| Versão/commit | Execução local do código atualizado |
| Ambiente e versão do Python | Windows local · Python 3.13.6 |
| Modelo local | Ollama `gemma4:e2b` para uma consulta integrada |
| Dados utilizados | CSVs do projeto em `backend/dados/` e cenários controlados para testes de unidade |
| Responsável | Execução automatizada local |

## Resultado geral

| Indicador | Resultado |
| --- | --- |
| Casos previstos nesta regressão | 63 |
| Executados | 13 de 63 |
| Aprovados | 13 |
| Reprovados | 0 |
| Bloqueados | 0 |

Foram executados 13 testes automatizados do menu e das tools de matéria-prima, além de uma consulta pelo fluxo local da MIA. Os demais casos permanecem sem status para uma regressão posterior.

## Casos de regressão

A tabela reúne os casos dos Guias de Testes das Sprints 1 e 2, US-11/US-12 e os testes do menu `/ajuda` e `/help`. Os resultados da Sprint 3 também estão detalhados no [Relatório de Testes — Sprint 3](../sprints/sprint-3/testes/Relat%C3%B3rio%20de%20Testes%20-%20Sprint%203.md).

| Caso | Entrada ou verificação | Resultado esperado | Resultado observado | Status | Evidência/observações |
| --- | --- | --- | :---: | :---: | --- |
| 1.1 | "O que devo produzir hoje?" | Lista os produtos e suas quantidades recomendadas com base no perfil histórico do dia |  |  |  |
| 1.2 | "O que preciso produzir amanhã?" | `converter_data_relativa` deve resolver "amanhã" para a data correta antes de calcular |  |  |  |
| 1.3 | "Quais produtos devo produzir hoje na padaria?" | Lista filtrada só com produtos do setor Padaria |  |  |  |
| 1.4 | "Quais produtos devo produzir no dia 20/09/2026?" | Aceita data explícita no formato `DD/MM/AAAA` (devolvida sem alteração por `converter_data_relativa`) |  |  |  |
| 2.1 | "Quantas unidades devo produzir hoje?" | Lista com nome do produto e quantidade recomendada (média histórica acrescida de 5% e arredondada para cima) |  |  |  |
| 2.2 | "Quanto de coxinha devo fazer amanhã?" | A tool devolve todos os produtos e o Formatador mostra só a Coxinha. |  |  |  |
| 2.3 | "Quantos produtos da padaria devo produzir hoje?" | Filtra por setor mantendo as quantidades |  |  |  |
| 3.1 | "O que foi produzido ontem na padaria?" | Lista por produto: Total Produzido, Vendas e Descarte, só da Padaria |  |  |  |
| 3.2 | "O que foi produzido ontem no açougue, na padaria e na cozinha?" | Deve conseguir consultar os três setores (o `ReAct` aciona a tool uma vez por setor) e apresentar tudo organizado |  |  |  |
| 3.3 | "O que foi produzido ontem?" | Deve retornar a produção de todos os setores |  |  |  |
| 3.4 | "O que foi produzido ontem? Separe a lista por setores" | Deve retornar a produção de todos os setores, agrupada por setor |  |  |  |
| 3.5 | "O que foi produzido no acugue ontem?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Açougue" mesmo com o erro |  |  |  |
| 4.1 | "O que deveria ter sido produzido ontem na padaria?" | Mostra a meta de produção por produto da Padaria, em tom de relatório/cobrança |  |  |  |
| 4.2 | "Qual era a meta de produção de hoje para o açougue?" | Mesmo cálculo, fraseado diferente — verifica se o Classificador de Intenção entende variações de pergunta |  |  |  |
| 4.3 | "Quanto deveria ter sido produzido ontem na padaria?" | Mostra a meta de produção **com quantidade** por produto da Padaria — mesmo comportamento do 4.1, mas fraseado com "Quanto" de forma explícita |  |  |  |
| 5.1 | "O que eu devo produzir de manhã na padaria?" | Produtos da Padaria (10 produtos) a produzir na manhã, com a quantidade e a unidade de medida de cada um (Kg, Un, Porção ou L) |  |  |  |
| 5.2 | "O que produzir em cada período do dia na padaria?" | Produtos e quantidades separados por período (manhã, tarde e noite), no mesmo formato para todos os períodos. Cada período é projetado separadamente, então a soma pode divergir da previsão do dia (caso 13.2) |  |  |  |
| 5.3 | "O que preciso fazer à tarde no açougue?" | Mesmo cálculo, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta |  |  |  |
| 5.4 | "O que devo produzir de manhã na padaira?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro |  |  |  |
| 5.5 | "O que devo produzir de manhã?" (sem informar o setor) | Sem setor, a MIA traz os produtos de todos os setores (33 produtos) no período da manhã; sem data, assume hoje |  |  |  |
| 5.6 | "O que devo produzir à noite amanhã na cozinha?" | `converter_data_relativa` resolve "amanhã" e a resposta traz só o período da noite, só da Cozinha (5 produtos) |  |  |  |
| 5.7 | Pedir um período sem histórico de vendas (ex.: madrugada) | `converter_periodo` converte "madrugada" em "noite" (período mais próximo) e a resposta usa os dados da noite; o ideal é a MIA avisar que usou a noite |  |  |  |
| 5.8 | "O que devo produzir à tarde e à noite na padaria?" | Combinação de períodos: cada produto da Padaria com as sublinhas de tarde e noite, sem a manhã |  |  |  |
| 6.1 | "Quantos reais foram descartados no dia 01/10/2026 em cada setor?" | Valor em R$ de cada setor (Padaria, Cozinha, Peixaria, Açougue e Processados). A tool calcula um setor por vez, então a MIA consulta setor a setor. Se apresentar um total geral, ele é a soma dos setores |  |  |  |
| 6.2 | "Quantos reais foram descartados no dia 01/10/2026 na padaria?" | Um único valor em R$ da Padaria, no formato "Custo total do desperdício ontem (dd/mm/aaaa) (Setor: Padaria): R$ x". A tool devolve só o total, sem detalhe por produto |  |  |  |
| 6.3 | "Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?" | Valor em R$ do período para a Peixaria ("no período de 01/09/2026 a 15/09/2026"); testa `data_inicio`, `data_fim` e setor juntos |  |  |  |
| 6.4 | "Quantos reais foram descartados no acugue no dia 01/10/2026?" (erro de digitação proposital) | `normalizar_setor` corrige para "Açougue" e a resposta mostra "(Setor: Açougue)" |  |  |  |
| 6.5 | "Quantos reais foram descartados no dia 01/10/2026?" (sem informar o setor) | Total da empresa inteira (todos os setores somados), sem "(Setor: ...)" na frase |  |  |  |
| 6.7 | "Quantos reais foram descartados em 01/01/2020?" (data sem registros) | Hoje a tool devolve R$ 0,00; decidir no Planning se a MIA deve avisar que não há registros nessa data |  |  |  |
| 7.1 | "Quantos reais foram descartados em 07/04/2026 na empresa toda?" | Valor total em R$ somando todos os setores |  |  |  |
| 7.2 | "Qual foi o custo total de desperdício em setembro?" | Valor total do período; fraseado diferente |  |  |  |
| 7.3 | "Quantos reais foram descartados no dia 01/10/2026? Separe por setores" | Total geral e o valor de cada setor, agrupados |  |  |  |
| 8.1 | "Quais produtos da empresa trazem mais lucro?" | Ranking geral de todos os setores, ordenado por lucro em R$, indicando o setor de cada produto |  |  |  |
| 8.2 | "Me mostra os 5 produtos mais lucrativos do mercado" | Ranking limitado a 5 itens |  |  |  |
| 8.3 | Verificação cruzada: calcular à mão o lucro de um produto do caso 8.1 a partir dos CSV | O valor calculado é igual ao exibido pela MIA |  |  |  |
| 9.1 | Áudio dizendo: "O que devo produzir hoje?" | Transcreve e responde igual ao caso 1.1 da Sprint 1, incluindo as quantidades recomendadas |  |  |  |
| 9.2 | Áudio dizendo: "Quantas unidades devo produzir amanhã na padaria?" | Resolve "amanhã" e o setor a partir da fala; resposta com nome e quantidade |  |  |  |
| 9.3 | Áudio dizendo: "Quanto de coxinha devo fazer amanhã?" em ambiente com ruído | Transcrição aceitável; se não entender, pede para repetir, sem inventar resposta |  |  |  |
| 9.4 | Áudio vazio ou só com silêncio | Mensagem amigável pedindo para enviar novamente, sem travar o bot |  |  |  |
| 9.5 | Áudio dizendo: "Qual é a capital da França?" | Agente Roteador identifica `INVALIDO`; mesma recusa padrão do texto |  |  |  |
| 9.6 | Enviar a mesma pergunta digitada e depois por áudio | As duas respostas têm o mesmo conteúdo |  |  |  |
| 9.7 | Enviar uma foto | Continua respondendo a mensagem fixa de formato não suportado (o caso 0.2.4 da Sprint 1 passa a valer só para formatos que não sejam texto nem áudio) |  |  |  |
| 9.8 | Após os testes, conferir a pasta de arquivos temporários da máquina | Não restaram arquivos de áudio temporários |  |  |  |
| 9.9 | Áudio dizendo: "Quantos reais foram descartados no dia 01/10/2026 em cada setor?" | Transcreve e responde igual ao caso 6.1 (valor por setor e total geral) |  |  |  |
| 10.1 | "Quanta matéria-prima preciso deixar preparada para amanhã na padaria?" | Lista de matérias-primas da Padaria, com quantidade e unidade, baseada na previsão de produção de amanhã |  |  |  |
| 10.2 | "O que preciso separar de ingredientes para amanhã na cozinha?" | Mesmo cálculo, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta |  |  |  |
| 10.3 | "Quanto de farinha preciso para amanhã?" | Filtra uma matéria-prima e soma o consumo de todos os produtos que a usam |  |  |  |
| 10.4 | "Quanta matéria-prima preciso para amanhã?" (sem informar o setor) | Comportamento definido no Planning: todos os setores ou pedido do setor ao líder |  |  |  |
| 10.5 | "Quanta matéria-prima preciso para a padaira amanhã?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro |  |  |  |
| 10.6 | Verificação cruzada: comparar com "Quantas unidades devo produzir amanhã na padaria?" | Quantidade de matéria-prima = quantidade prevista de cada produto × consumo por unidade |  |  |  |
| 11.1 | Consultar matérias-primas disponíveis para transferir | Lista sobras positivas por ingrediente, unidade, quantidade e setor, após descontar a necessidade prevista | A MIA local listou as sobras por setor para 23/11/2026 e informou que não havia déficit compatível; portanto, não recomendou transferência. | ✅ | [resposta completa](#evidencia-111) |
| 11.2 | Consultar com setor de origem Padaria | Considera somente sobras da Padaria como fontes | Aprovado: filtro de origem considerou somente sobras da Padaria. | ✅ | [teste automatizado](#execucao-automatizada) |
| 11.3 | Estoque igual ou inferior à necessidade prevista em todos os setores | Informa que não há déficit compatível e não recomenda transferência; mantém a lista de sobras | Aprovado: no cenário controlado não houve déficit; nenhuma transferência foi recomendada e as sobras disponíveis foram mantidas na resposta. | ✅ | [teste automatizado](#execucao-automatizada) |
| 11.4 | Data sem histórico compatível | Informa que não há histórico para calcular a necessidade | Aprovado: histórico vazio retornou mensagem clara de ausência de dados. | ✅ | [teste automatizado](#execucao-automatizada) |
| 11.5 | Produto previsto sem receita cadastrada | Identifica o produto sem receita e sinaliza análise incompleta, sem inventar consumo | Aprovado: o produto sem receita foi informado e a análise sinalizada como incompleta. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.1 | Um setor tem sobra e outro tem déficit do mesmo ingrediente | Recomenda a transferência e informa quantidade, unidade, origem, destino e justificativa | Aprovado: cenário controlado recomendou 17,00 kg de Farinha da Padaria para a Cozinha. | ✅ | [resposta completa](#evidencia-121) |
| 12.2 | Sobra menor que o déficit do destino | Recomenda no máximo a sobra disponível e informa o déficit restante | Aprovado: cenário controlado recomendou 8,00 kg e informou falta residual de 9,00 kg. | ✅ | [resposta completa](#evidencia-122) |
| 12.3 | Não há déficit ou sobra compatível | Informa que nenhuma transferência foi recomendada | Aprovado: cenário sem déficit compatível não gerou recomendação. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.4 | Aplicar filtro de setor de origem | Não usa sobras de outros setores como fonte | Aprovado: filtro de origem impediu o uso de sobras dos demais setores. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.5 | Consultar com data relativa e data explícita | Resolve a data e identifica o período usado na análise | Aprovado: data explícita e referência relativa foram convertidas para dd/mm/aaaa. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.6 | Verificação antes/depois da consulta | Os dados de estoque permanecem inalterados | Aprovado: o hash do ingredientes.csv permaneceu igual antes e depois da consulta; a resposta ficou abaixo do limite do Telegram. | ✅ | [teste automatizado](#execucao-automatizada) |
| 13.1 | Enviar `/ajuda` ou `/help` | Abre menu inline com Produção, Matéria-prima, Descarte, Produtos, Vendas e áudio | Teste automatizado confirmou os comandos e as categorias. | ✅ | [teste automatizado](#execucao-automatizada) |
| 13.2 | Escolher categoria e pergunta de exemplo | Envia a pergunta ao processador da MIA e oferece navegação de retorno | Teste automatizado confirmou a chamada ao processador e o teclado de retorno. | ✅ | [teste automatizado](#execucao-automatizada) |

## Execução da Sprint 3

Os casos 11.1 a 13.2 foram verificados por 13 testes automatizados controlados. O caso 11.1 também percorreu o fluxo local da MIA usado pelo TeleBot e preservou a saída completa da tool. O envio pelo Telegram ao vivo e o áudio físico não foram executados. Consulte as seções recolhíveis abaixo para ver as respostas completas.


## Respostas completas

<details>
<summary><b>11.1</b> — Resposta da MIA a “Quais matérias-primas estão disponíveis para transferir para outros setores?”</summary>

<a id="evidencia-111"></a>

Resposta capturada pelo fluxo local `processar_mensagem`, o mesmo chamado pelo TeleBot:

```text
Análise de sobras e transferências para no dia 23/11/2026 (não alterei os estoques):

Sobras disponíveis após atender à necessidade prevista:
- Padaria: Farinha de Trigo: 648969.60 Kg; Água: 151.90 L; Sal: 11.52 Kg; Fermento: 5.45 Kg; Polvilho: 62.40 Kg; Queijo Mussarela: 46997.99 Kg; Leite: 149.43 L; Óleo de Soja: 7.80 L; Manteiga: 20.77 Kg; Açúcar: 17.02 Kg; Frango Desfiado: 15.54 Kg; Batata: 13.66 Kg; Presunto: 4.76 Kg; Cacau em Pó: 5.19 Kg; Leite Condensado: 161.03 Kg; Biscoito Maizena: 5.82 Kg; Limão: 4.26 Kg; Creme de Leite: 3.01 Kg; Ovos: 44.83 Kg; Coco Ralado: 1.97 Kg
- Cozinha: Farinha de Trigo: 45.75 Kg; Leite: 8.97 L; Óleo de Soja: 8.34 L; Manteiga: 7.73 Kg; Frango Desfiado: 11.64 Kg; Batata: 95.04 Kg; Frango Inteiro: 261.05 Un; Tempero Pronto: 12.08 Kg; Arroz Branco: 65.36 Kg; Feijão Carioca: 35.44 Kg; Carne Bovina: 106.08 Kg; Massa de Lasanha: 16.70 Kg; Carne Bovina Moída: 25.47 Kg; Queijo: 22.00 Kg; Molho Tomate: 40.04 Kg; Macarrão: 41.60 Kg; Carne: 13.58 Kg
- Peixaria: Óleo de Soja: 8.96 L; Limão: 1.79 Kg; Arroz Japonês: 61.04 Kg; Salmão: 68.14 Kg; Cream Cheese: 6.11 Kg; Atum: 6.50 Kg; Alga Nori: 3.31 Kg; Peixe Branco: 9.18 Kg; Cebola Roxa: 2.16 Kg
- Processados: Batata: 98.13 Kg; Carne Bovina: 23.85 Kg; Laranja: 801.98 Kg; Mamão: 27.99 Kg; Banana: 35.25 Kg; Maçã: 55.75 Kg; Mandioca: 43.20 Kg; Cenoura: 60.11 Kg; Chuchu: 28.72 Kg; Alface: 31.75 Kg; Rúcula: 14.79 Kg; Tomate: 13.94 Kg
- Açougue: Frango Inteiro: 122.00 Un; Tempero Pronto: 21.52 Kg; Carne Bovina: 192.34 Kg; Carne Bovina Moída: 97.86 Kg; Cebola: 11.49 Kg; Carne Suína: 81.17 Kg; Gordura Suína: 16.19 Kg; Tempero: 9.15 Kg; Hortelã: 3.76 Kg; Feijão Preto: 31.42 Kg; Carne Suína Salgada: 31.36 Kg

Nenhuma transferência foi recomendada porque não há déficit previsto compatível com as sobras disponíveis.
```

> Os valores de estoque acima são os registrados em `ingredientes.csv`. O arquivo informa 649000,47 Kg de Farinha de Trigo e 47000,25 Kg de Queijo Mussarela na Padaria; confirme esses valores e as unidades na planilha de origem. A tool usou os dados sem alterá-los.

</details>

<details>
<summary><b>12.1</b> — Saída completa no teste automatizado com transferência suficiente</summary>

<a id="evidencia-121"></a>

```text
Análise de sobras e transferências para no dia 25/10/2026 (não alterei os estoques):

Sobras disponíveis após atender à necessidade prevista:
- Padaria: Farinha: 28.00 kg

Transferências recomendadas:
- Farinha: transferir 17.00 kg de Padaria para Cozinha; após a transferência, a falta será 0.00 kg.
```

</details>

<details>
<summary><b>12.2</b> — Saída completa no teste automatizado com transferência parcial</summary>

<a id="evidencia-122"></a>

```text
Análise de sobras e transferências para no dia 25/10/2026 (não alterei os estoques):

Sobras disponíveis após atender à necessidade prevista:
- Padaria: Farinha: 8.00 kg

Transferências recomendadas:
- Farinha: transferir 8.00 kg de Padaria para Cozinha; após a transferência, a falta será 9.00 kg.
```

</details>

### Execução automatizada <a id="execucao-automatizada"></a>

`automatizar_testes_sprint3_mp.py`: **13 testes aprovados** (10 de matéria-prima e 3 do menu de ajuda). A suíte cobre comandos, exemplos e navegação do menu; filtros de origem; transferências total e parcial; ausência de histórico e receita; datas; unidades; preservação do CSV; e uma regressão adicional do filtro da US-10. Os casos 12.3 e 12.4 são cobertos pelas mesmas verificações de ausência de recomendação e filtro de origem exercitadas em 11.3 e 11.2. `validar_resposta_integrada_mp.py --captured` confirmou que a resposta local da MIA preserva os 69 itens da saída da tool. O teste isolou o fluxo de resposta; não houve chamada à API do Telegram nem gravação/transcrição de áudio.


## Limites e observações da execução

A execução foi local. Não foram realizados envio por Telegram ao vivo, teste de áudio físico ou regressão manual das Sprints 1 e 2. Os casos não executados permanecem sem status. O CSV de ingredientes contém estoques muito altos para Farinha de Trigo (649000,47 Kg) e Queijo Mussarela (47000,25 Kg) na Padaria; os valores e unidades precisam ser conferidos com a planilha de origem antes de uso operacional.
