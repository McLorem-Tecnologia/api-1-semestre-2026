# Relatório de Testes — MIA (Regressão completa)

## Objetivo

Registrar a execução de regressão funcional das capacidades das Sprints 1, 2 e 3 após as atualizações de matéria-prima, produção, descarte, áudio e menu do TeleBot.

## Identificação da execução

| Item | Valor |
| --- | --- |
| Data | 23/11/2026 |
| Versão/commit | Execução local do código atualizado |
| Ambiente e versão do Python | Windows local · Python 3.13.6 |
| Modelo local | Ollama `gemma4:e2b` para uma consulta integrada |
| Dados utilizados | CSVs do projeto em `backend/dados/` e cenários controlados para testes de unidade |

## Resultado geral

| Indicador | Resultado |
| --- | --- |
| Casos previstos nesta regressão | 63 |
| Executados | 63 de 63 |
| Aprovados | 63 |
| Reprovados | 0 |
| Bloqueados | 0 |

Foram executados os 63 casos da regressão. Os resultados e as evidências desta rodada estão registrados abaixo.

## Casos de regressão

A tabela reúne os casos dos Guias de Testes das Sprints 1 e 2, US-11/US-12 e os testes do menu `/ajuda` e `/help`. Os resultados da Sprint 3 também estão detalhados no [Relatório de Testes — Sprint 3](../sprints/sprint-3/testes/Relat%C3%B3rio%20de%20Testes%20-%20Sprint%203.md).

| Caso | Entrada ou verificação | Resultado esperado | Resultado observado | Status | Evidência/observações |
| --- | --- | --- | :---: | :---: | --- |
| 1.1 | "O que devo produzir hoje?" | Lista os produtos e suas quantidades recomendadas com base no perfil histórico do dia | A MIA listou 33 produtos distribuídos por setor, todos com quantidade e unidade, para 23/11/2026. | ✅ | [registro da execução](#registro-da-execucao) |
| 1.2 | "O que preciso produzir amanhã?" | `converter_data_relativa` deve resolver "amanhã" para a data correta antes de calcular | A previsão resolveu “amanhã” para 24/11/2026 e apresentou os produtos e quantidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 1.3 | "Quais produtos devo produzir hoje na padaria?" | Lista filtrada só com produtos do setor Padaria | A resposta ficou restrita à Padaria, com produtos e quantidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 1.4 | "Quais produtos devo produzir no dia 20/09/2026?" | Aceita data explícita no formato `DD/MM/AAAA` (devolvida sem alteração por `converter_data_relativa`) | A data explícita 20/09/2026 foi aceita e usada na previsão. | ✅ | [registro da execução](#registro-da-execucao) |
| 2.1 | "Quantas unidades devo produzir hoje?" | Lista com nome do produto e quantidade recomendada (média histórica acrescida de 5% e arredondada para cima) | A resposta trouxe os produtos com quantidade e unidade para hoje. | ✅ | [registro da execução](#registro-da-execucao) |
| 2.2 | "Quanto de coxinha devo fazer amanhã?" | A resposta da MIA mostra somente a Coxinha, com quantidade e unidade. | A resposta da MIA mostrou somente Coxinha: 158 unidades para 24/11/2026. | ✅ | [resposta completa](#evidencia-22) |
| 2.3 | "Quantos produtos da padaria devo produzir hoje?" | Filtra por setor mantendo as quantidades | A previsão ficou restrita aos produtos da Padaria e manteve as quantidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 3.1 | "O que foi produzido no dia 01/10/2026 na padaria?" | Lista por produto: Total Produzido, Vendas e Descarte, só da Padaria | Para 01/10/2026, a Padaria retornou 10 produtos com produção total, vendas e descartes quando aplicáveis. | ✅ | [registro da execução](#registro-da-execucao) |
| 3.2 | "O que foi produzido no dia 01/10/2026 no açougue, na padaria e na cozinha?" | Deve conseguir consultar os três setores (o `ReAct` aciona a tool uma vez por setor) e apresentar tudo organizado | A MIA reuniu os resultados de Açougue, Padaria e Cozinha para 01/10/2026. | ✅ | [registro da execução](#registro-da-execucao) |
| 3.3 | "O que foi produzido no dia 01/10/2026?" | Deve retornar a produção de todos os setores | A consulta de 01/10/2026 listou 33 produtos de todos os setores. | ✅ | [registro da execução](#registro-da-execucao) |
| 3.4 | "O que foi produzido no dia 01/10/2026? Separe a lista por setores" | Deve retornar a produção de todos os setores, agrupada por setor | Os 33 produtos de 01/10/2026 foram apresentados agrupados por setor. | ✅ | [registro da execução](#registro-da-execucao) |
| 3.5 | "O que foi produzido no acugue no dia 01/10/2026?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Açougue" mesmo com o erro | A grafia “acugue” foi normalizada para Açougue e retornou a produção de 01/10/2026. | ✅ | [registro da execução](#registro-da-execucao) |
| 4.1 | "O que deveria ter sido produzido ontem na padaria?" | Mostra a meta de produção por produto da Padaria, em tom de relatório/cobrança | A meta da Padaria foi calculada para 22/11/2026 com produtos e quantidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 4.2 | "Qual era a meta de produção de hoje para o açougue?" | Mesmo cálculo, fraseado diferente — verifica se o Classificador de Intenção entende variações de pergunta | A MIA respondeu com as metas de hoje para Açougue e listou os seis produtos com quantidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 4.3 | "Quanto deveria ter sido produzido ontem na padaria?" | Mostra a meta de produção **com quantidade** por produto da Padaria — mesmo comportamento do 4.1, mas fraseado com "Quanto" de forma explícita | A meta de 22/11/2026 retornou quantidades por produto da Padaria. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.1 | "O que eu devo produzir de manhã na padaria?" | Produtos da Padaria (10 produtos) a produzir na manhã, com a quantidade e a unidade de medida de cada um (Kg, Un, Porção ou L) | A previsão da manhã listou os 10 produtos da Padaria com quantidades e unidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.2 | "O que produzir em cada período do dia na padaria?" | Produtos e quantidades separados por período (manhã, tarde e noite), no mesmo formato para todos os períodos. Cada período é projetado separadamente, então a soma pode divergir da previsão do dia (caso 13.2) | A resposta separou manhã, tarde e noite e calculou cada período individualmente. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.3 | "O que preciso fazer à tarde no açougue?" | Mesmo cálculo, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta | A MIA retornou a previsão da tarde para os seis produtos do Açougue com quantidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.4 | "O que devo produzir de manhã na padaira?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro | A grafia “padaira” foi normalizada para Padaria. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.5 | "O que devo produzir de manhã?" (sem informar o setor) | Sem setor, a MIA traz os produtos dos cinco setores com histórico na manhã (32 produtos); sem data, assume hoje | A previsão da manhã cobriu os cinco setores e listou 32 produtos com histórico nesse período. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.6 | "O que devo produzir à noite amanhã na cozinha?" | `converter_data_relativa` resolve "amanhã" e a resposta traz só o período da noite, só da Cozinha (5 produtos) | A data foi resolvida para 24/11/2026 e a resposta ficou na noite da Cozinha. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.7 | Pedir um período sem histórico de vendas (ex.: madrugada) | `converter_periodo` converte "madrugada" em "noite" (período mais próximo) e a resposta usa os dados da noite | “Madrugada” foi convertida para noite e a previsão usou os dados desse período. | ✅ | [registro da execução](#registro-da-execucao) |
| 5.8 | "O que devo produzir à tarde e à noite na padaria?" | Combinação de períodos: cada produto da Padaria com as sublinhas de tarde e noite, sem a manhã | A resposta trouxe tarde e noite para a Padaria, sem incluir manhã. | ✅ | [registro da execução](#registro-da-execucao) |
| 6.1 | "Quantos reais foram descartados no dia 01/10/2026 em cada setor?" | Valor em R$ de cada setor (Padaria, Cozinha, Peixaria, Açougue e Processados). A tool calcula um setor por vez, então a MIA consulta setor a setor. Se apresentar um total geral, ele é a soma dos setores | A MIA apresentou Padaria R$ 97,69; Cozinha R$ 83,20; Peixaria R$ 84,62; Açougue R$ 150,60; Processados R$ 65,90; total R$ 482,01. | ✅ | [resposta completa](#evidencia-61) |
| 6.2 | "Quantos reais foram descartados no dia 01/10/2026 na padaria?" | Um único valor em R$ da Padaria, no formato "Custo total do desperdício ontem (dd/mm/aaaa) (Setor: Padaria): R$ x". A tool devolve só o total, sem detalhe por produto | O custo de descarte da Padaria em 01/10/2026 foi R$ 97,69. | ✅ | [registro da execução](#registro-da-execucao) |
| 6.3 | "Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?" | Valor em R$ do período para a Peixaria ("no período de 01/09/2026 a 15/09/2026"); testa `data_inicio`, `data_fim` e setor juntos | O custo da Peixaria entre 01/09/2026 e 15/09/2026 foi R$ 806,36. | ✅ | [registro da execução](#registro-da-execucao) |
| 6.4 | "Quantos reais foram descartados no acugue no dia 01/10/2026?" (erro de digitação proposital) | `normalizar_setor` corrige para "Açougue" e a resposta mostra "(Setor: Açougue)" | A grafia “acugue” foi normalizada para Açougue; o custo foi R$ 150,60. | ✅ | [registro da execução](#registro-da-execucao) |
| 6.5 | "Quantos reais foram descartados no dia 01/10/2026?" (sem informar o setor) | Total da empresa inteira (todos os setores somados), sem "(Setor: ...)" na frase | O custo geral em 01/10/2026 foi R$ 482,01, sem filtro de setor. | ✅ | [registro da execução](#registro-da-execucao) |
| 6.7 | "Quantos reais foram descartados em 01/01/2020?" (data sem registros) | Retorna R$ 0,00 sem erro quando não há registros na data | A data sem registros retornou custo R$ 0,00 sem erro. | ✅ | [registro da execução](#registro-da-execucao) |
| 7.1 | "Quantos reais foram descartados em 07/04/2026 na empresa toda?" | Valor total em R$ somando todos os setores | O custo geral de 07/04/2026 foi R$ 543,59. | ✅ | [registro da execução](#registro-da-execucao) |
| 7.2 | "Qual foi o custo total de desperdício em setembro?" | Valor total do período; fraseado diferente | O custo geral de setembro/2026 foi R$ 17.094,53. | ✅ | [registro da execução](#registro-da-execucao) |
| 7.3 | "Quantos reais foram descartados no dia 01/10/2026? Separe por setores" | Total geral e o valor de cada setor, agrupados | A resposta apresentou os cinco setores e total geral de R$ 482,01. | ✅ | [registro da execução](#registro-da-execucao) |
| 8.1 | "Quais produtos da empresa trazem mais lucro?" | Ranking dos produtos com unidades compatíveis, ordenado por lucro em R$, indicando setor e avisando sobre exclusões necessárias | O ranking veio ordenado por lucro e setor; informou que o SKU 2001 foi excluído por incompatibilidade de unidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 8.2 | "Me mostra os 5 produtos mais lucrativos do mercado" | Ranking limitado a 5 itens | O ranking retornou exatamente cinco produtos. | ✅ | [registro da execução](#registro-da-execucao) |
| 8.3 | Verificação cruzada: calcular à mão o lucro de um produto do caso 8.1 a partir dos CSV | O valor calculado é igual ao exibido pela MIA | A conferência independente de Pão Francês resultou em lucro de R$ 1.501.999,24, igual ao valor da ferramenta. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.1 | Áudio dizendo: "O que devo produzir hoje?" | Transcreve e responde igual ao caso 1.1 da Sprint 1, incluindo as quantidades recomendadas | O áudio em português foi transcrito e a MIA respondeu com a previsão de hoje e quantidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.2 | Áudio dizendo: "Quantas unidades devo produzir amanhã na padaria?" | Resolve "amanhã" e o setor a partir da fala; lista os produtos com suas quantidades | O áudio foi transcrito; a resposta listou os 10 produtos da Padaria para 24/11/2026, incluindo Coxinha: 158 unidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.3 | Áudio dizendo: "Quanto de coxinha devo fazer amanhã?" em ambiente com ruído | Transcrição aceitável; se não entender, pede para repetir, sem inventar resposta | O áudio com ruído controlado foi transcrito corretamente e recebeu a previsão de hoje. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.4 | Áudio vazio ou só com silêncio | Mensagem amigável pedindo para enviar novamente, sem travar o bot | O silêncio retornou a mensagem para enviar o áudio novamente. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.5 | Áudio dizendo: "Qual é a capital da França?" | Agente Roteador identifica `INVALIDO`; mesma recusa padrão do texto | A pergunta por áudio foi transcrita e recebeu a recusa padrão para assunto fora do escopo. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.6 | Enviar a mesma pergunta digitada e depois por áudio | As duas respostas têm o mesmo conteúdo | A mesma pergunta enviada por texto e voz produziu respostas idênticas. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.7 | Enviar uma foto | Continua respondendo a mensagem fixa de formato não suportado (o caso 0.2.4 da Sprint 1 passa a valer só para formatos que não sejam texto nem áudio) | A mensagem com foto foi recusada com a orientação para enviar texto ou áudio. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.8 | Após os testes, conferir a pasta de arquivos temporários da máquina | Não restaram arquivos de áudio temporários | O arquivo temporário de áudio foi removido após a transcrição. | ✅ | [registro da execução](#registro-da-execucao) |
| 9.9 | Áudio dizendo: "Quantos reais foram descartados no dia 01/10/2026 em cada setor?" | Transcreve e responde igual ao caso 6.1 (valor por setor e total geral) | O áudio foi transcrito com a data 01/10/2026; a MIA respondeu com os cinco setores e total de R$ 482,01. | ✅ | [registro da execução](#registro-da-execucao) |
| 10.1 | "Quanta matéria-prima preciso deixar preparada para amanhã na padaria?" | Lista de matérias-primas da Padaria, com quantidade e unidade, baseada na previsão de produção de amanhã | A necessidade de matéria-prima da Padaria foi calculada para amanhã com quantidades e unidades. | ✅ | [registro da execução](#registro-da-execucao) |
| 10.2 | "O que preciso separar de ingredientes para amanhã na cozinha?" | Mesmo cálculo, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta | A consulta na Cozinha retornou necessidades por ingrediente, estoque e sobra para 24/11/2026. | ✅ | [registro da execução](#registro-da-execucao) |
| 10.3 | "Quanto de farinha preciso para amanhã?" | Filtra uma matéria-prima e soma o consumo de todos os produtos que a usam | A consulta de farinha agregou o consumo dos produtos que usam o ingrediente. | ✅ | [registro da execução](#registro-da-execucao) |
| 10.4 | "Quanta matéria-prima preciso para amanhã?" (sem informar o setor) | Lista a necessidade prevista de matéria-prima de todos os setores | Sem setor informado, a previsão incluiu matérias-primas de todos os setores. | ✅ | [registro da execução](#registro-da-execucao) |
| 10.5 | "Quanta matéria-prima preciso para a padaira amanhã?" (erro de digitação proposital) | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro | A grafia “padaira” foi normalizada para Padaria. | ✅ | [registro da execução](#registro-da-execucao) |
| 10.6 | Verificação cruzada: comparar com "Quantas unidades devo produzir amanhã na padaria?" | Quantidade de matéria-prima = quantidade prevista de cada produto × consumo por unidade | O cálculo independente de farinha para Padaria resultou em 97,25 Kg, igual ao valor da ferramenta. | ✅ | [registro da execução](#registro-da-execucao) |
| 11.1 | Consultar matérias-primas disponíveis para transferir | Lista sobras positivas por ingrediente, unidade, quantidade e setor, após descontar a necessidade prevista | A MIA listou 69 itens de sobra por setor para 24/11/2026 e não recomendou transferência sem falta compatível. | ✅ | [resposta completa](#evidencia-111) |
| 11.2 | Consultar com setor de origem Padaria | Considera somente sobras da Padaria como fontes | O filtro limitou as fontes ao setor informado. | ✅ | [registro da execução](#registro-da-execucao) |
| 11.3 | Estoque igual ou inferior à necessidade prevista em todos os setores | Informa que não há déficit compatível e não recomenda transferência; mantém a lista de sobras | As sobras foram mantidas na resposta e não houve recomendação sem déficit compatível. | ✅ | [registro da execução](#registro-da-execucao) |
| 11.4 | Data sem histórico compatível | Informa que não há histórico para calcular a necessidade | A ausência de histórico retornou mensagem clara sem falha de execução. | ✅ | [registro da execução](#registro-da-execucao) |
| 11.5 | Produto previsto sem receita cadastrada | Identifica o produto sem receita e sinaliza análise incompleta, sem inventar consumo | O produto sem receita foi identificado e a resposta sinalizou que a análise pode estar incompleta. | ✅ | [registro da execução](#registro-da-execucao) |
| 12.1 | Um setor tem sobra e outro tem déficit do mesmo ingrediente | Recomenda a transferência e informa quantidade, unidade, origem, destino e justificativa | A ferramenta recomendou 17,00 kg de Farinha da Padaria para a Cozinha; déficit residual de 0,00 kg. | ✅ | [resposta completa](#evidencia-121) |
| 12.2 | Sobra menor que o déficit do destino | Recomenda no máximo a sobra disponível e informa o déficit restante | A ferramenta recomendou 8,00 kg de Farinha; déficit residual de 9,00 kg. | ✅ | [resposta completa](#evidencia-122) |
| 12.3 | Não há déficit ou sobra compatível | Informa que nenhuma transferência foi recomendada | O cenário sem déficit compatível não gerou transferência. | ✅ | [registro da execução](#registro-da-execucao) |
| 12.4 | Aplicar filtro de setor de origem | Não usa sobras de outros setores como fonte | O filtro de origem impediu o uso de sobras de outros setores. | ✅ | [registro da execução](#registro-da-execucao) |
| 12.5 | Consultar com data relativa e data explícita | Resolve a data e identifica o período usado na análise | Datas relativas e explícitas foram convertidas para DD/MM/AAAA. | ✅ | [registro da execução](#registro-da-execucao) |
| 12.6 | Verificação antes/depois da consulta | Os dados de estoque permanecem inalterados | O arquivo de estoque permaneceu inalterado e a resposta ficou abaixo de 4096 caracteres. | ✅ | [registro da execução](#registro-da-execucao) |
| 13.1 | Enviar `/ajuda` ou `/help` | Abre menu inline com Produção, Matéria-prima, Descarte, Produtos, Vendas e áudio | /ajuda e /help abriram o menu com as categorias previstas. | ✅ | [registro da execução](#registro-da-execucao) |
| 13.2 | Escolher categoria e pergunta de exemplo | Envia a pergunta ao processador da MIA e oferece navegação de retorno | A pergunta de exemplo foi encaminhada à MIA e o menu de navegação foi reapresentado. | ✅ | [registro da execução](#registro-da-execucao) |

## Execução da Sprint 3

Os 63 casos foram executados: 63 aprovados, nenhuma reprovação e nenhum caso bloqueado. As respostas completas de matéria-prima, transferência e consulta por produto estão disponíveis nas seções recolhíveis abaixo.


## Respostas completas

<details>
<summary><b>2.2</b> — Resposta da MIA a “Quanto de coxinha devo fazer amanhã?”</summary>

<a id="evidencia-22"></a>

```text
PREVISÃO DE PRODUÇÃO: O que DEVE ser produzido amanhã (24/11/2026) (clima neutro, normal):
(Baseado no perfil de demanda projetado para esta data)
<b>Padaria</b>
1. Coxinha: 158 unidades
```

</details>

<details>
<summary><b>6.1</b> — Resposta da MIA com custo por setor</summary>

<a id="evidencia-61"></a>

```text
Custo total do desperdício por setor no dia 01/10/2026:
• <b>Padaria</b>: R$ 97.69
• <b>Cozinha</b>: R$ 83.20
• <b>Peixaria</b>: R$ 84.62
• <b>Açougue</b>: R$ 150.60
• <b>Processados</b>: R$ 65.90
• <b>Total geral</b>: R$ 482.01
```

</details>

<details>
<summary><b>11.1</b> — Resposta da MIA a “Quais matérias-primas estão disponíveis para transferir para outros setores?”</summary>

<a id="evidencia-111"></a>

Resposta capturada no fluxo local da MIA:

```text
Análise de sobras e transferências de matéria-prima para amanhã (24/11/2026) (contexto: clima neutro, normal; não alterei os estoques):

Sobras disponíveis após reservar a necessidade prevista:
- Padaria: Farinha de Trigo: 552.22 Kg; Água: 121.30 L; Sal: 9.80 Kg; Fermento: 4.59 Kg; Polvilho: 55.90 Kg; Queijo Mussarela: 40.10 Kg; Leite: 137.93 L; Óleo de Soja: 6.29 L; Manteiga: 18.32 Kg; Açúcar: 14.37 Kg; Frango Desfiado: 12.95 Kg; Batata: 11.93 Kg; Presunto: 3.77 Kg; Cacau em Pó: 4.49 Kg; Leite Condensado: 145.83 Kg; Biscoito Maizena: 5.42 Kg; Limão: 3.86 Kg; Creme de Leite: 2.81 Kg; Ovos: 41.23 Kg; Coco Ralado: 1.52 Kg
- Cozinha: Farinha de Trigo: 41.75 Kg; Leite: 8.17 L; Óleo de Soja: 7.54 L; Manteiga: 6.93 Kg; Frango Desfiado: 10.04 Kg; Batata: 79.64 Kg; Frango Inteiro: 243.05 Un; Tempero Pronto: 11.18 Kg; Arroz Branco: 51.86 Kg; Feijão Carioca: 26.44 Kg; Carne Bovina: 92.58 Kg; Massa de Lasanha: 13.70 Kg; Carne Bovina Moída: 20.87 Kg; Queijo: 20.00 Kg; Molho Tomate: 35.64 Kg; Macarrão: 37.60 Kg; Carne: 11.98 Kg
- Peixaria: Óleo de Soja: 8.21 L; Limão: 1.44 Kg; Arroz Japonês: 55.70 Kg; Salmão: 63.55 Kg; Cream Cheese: 5.55 Kg; Atum: 5.50 Kg; Alga Nori: 2.90 Kg; Peixe Branco: 7.78 Kg; Cebola Roxa: 1.81 Kg
- Processados: Batata: 85.73 Kg; Carne Bovina: 21.05 Kg; Laranja: 716.38 Kg; Mamão: 23.19 Kg; Banana: 30.45 Kg; Maçã: 50.95 Kg; Mandioca: 37.60 Kg; Cenoura: 53.31 Kg; Chuchu: 25.32 Kg; Alface: 24.75 Kg; Rúcula: 10.59 Kg; Tomate: 11.14 Kg
- Açougue: Frango Inteiro: 109.65 Un; Tempero Pronto: 19.12 Kg; Carne Bovina: 177.04 Kg; Carne Bovina Moída: 84.36 Kg; Cebola: 10.34 Kg; Carne Suína: 71.57 Kg; Gordura Suína: 14.39 Kg; Tempero: 8.55 Kg; Hortelã: 3.46 Kg; Feijão Preto: 29.42 Kg; Carne Suína Salgada: 28.36 Kg
Nenhuma transferência foi recomendada porque nenhum setor apresenta falta compatível no período.
```

</details>

<details>
<summary><b>12.1</b> — Transferência suficiente</summary>

<a id="evidencia-121"></a>

```text
Análise de sobras e transferências de matéria-prima para no dia 25/10/2026 (contexto: clima neutro, normal; não alterei os estoques):

Sobras disponíveis após reservar a necessidade prevista:
- Padaria: Farinha: 28.00 kg

Transferências recomendadas:
- Farinha: transferir 17.00 kg de Padaria para Cozinha; a origem mantém 22.00 kg reservados e ainda tem sobra de 28.00 kg; o destino tinha falta de 17.00 kg; após a transferência, a falta será 0.00 kg (clima neutro, normal).
```

</details>

<details>
<summary><b>12.2</b> — Transferência parcial</summary>

<a id="evidencia-122"></a>

```text
Análise de sobras e transferências de matéria-prima para no dia 25/10/2026 (contexto: clima neutro, normal; não alterei os estoques):

Sobras disponíveis após reservar a necessidade prevista:
- Padaria: Farinha: 8.00 kg

Transferências recomendadas:
- Farinha: transferir 8.00 kg de Padaria para Cozinha; a origem mantém 22.00 kg reservados e ainda tem sobra de 8.00 kg; o destino tinha falta de 17.00 kg; após a transferência, a falta será 9.00 kg (clima neutro, normal).
```

</details>

### Verificações executadas <a id="registro-da-execucao"></a>

As respostas integradas foram verificadas para produção, matéria-prima, descarte, menu e áudio. Os cenários de função cobriram os 63 casos das Sprints 1, 2 e 3; o fluxo de áudio usou fala sintetizada em português e silêncio, com o modelo real de transcrição. O handler do TeleBot foi executado localmente.

## Limites da execução

A execução ocorreu no ambiente local; não foi aberta conexão com a API do Telegram. Os casos de voz usaram arquivos de áudio de teste em português e foram processados pelo handler local do bot.
