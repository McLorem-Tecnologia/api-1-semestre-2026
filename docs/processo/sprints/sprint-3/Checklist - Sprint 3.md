# Checklist de Regressão — Sprint 3

Este checklist reúne os critérios de DoR e DoD das User Stories 01 a 10 das Sprints 1 e 2 e das US-11 e US-12 da Sprint 3. Os itens de execução foram reiniciados para esta rodada de regressão.

---

## US01 — Quais produtos devem ser produzidos
> *"Eu, como líder, quero saber quais produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto."*

**Implementado em:** `tool_previsao_vendas_por_data(tipo_pergunta="quais")` → `utils.classificar_dia`, `procedures.vendas.dataframe_vendas_similares`, `procedures.vendas.media_vendas_produtos.`

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (líder)
- [ ] Os produtos estão bem definidos no arquivo csv `produtos_mercado.csv`
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas
- [ ] Serão utilizados os csv `vendas_supermercado_<mês>_<ano>.csv` e `descartes_supermercado_<mês>_<ano>.csv`
- [ ] Método de cálculo será realizado baseado nas vendas anteriores e no dia do mês

### DoD
- [ ] Sistema identifica os produtos que precisam ser produzidos
- [ ] Histórico de vendas é considerado
- [ ] Recomendações são apresentadas de forma clara ao líder
- [ ] Fatores como **feriados** e **finais de semana** são considerados em `classificar_dia`.
- [ ] Funcionalidade foi testada sem erros
- [ ] Resultado foi validado pelo responsável

---

## US02 — Quantos produtos produzir
> *"Eu, como líder, quero saber quantos produtos precisam ser produzidos, a fim de reduzir o desperdício de tempo e produto."*

**Implementado em:** `tool_previsao_vendas_por_data(tipo_pergunta="quanto")` (mesma tool da US01, parâmetro diferente).

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado
- [ ] Os produtos estão bem definidos no csv `produtos_mercado.csv`
- [ ] Está definido como a quantidade recomendada será apresentada ao líder
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas
- [ ] Serão utilizados os csv `vendas_supermercado_<mês>_<ano>.csv` e `descartes_supermercado_<mês>_<ano>.csv`
- [ ] Método de cálculo baseado em vendas e dia do mês

### DoD
- [ ] O sistema calcula a quantidade recomendada de produção para cada produto
- [ ] O cálculo utiliza os dados de vendas definidos no projeto
- [ ] O sistema apresenta claramente o nome do produto e a quantidade recomendada
- [ ] Produtos sem necessidade de produção não são indevidamente recomendados (`media_vendas_produtos` só retorna produtos com histórico de vendas no perfil de dia filtrado)
- [ ] O cálculo considera dia de pagamento (dia 20 e 5º dia útil), sexta a domingo e feriados (BR/SP).
- [ ] A funcionalidade foi testada com diferentes cenários de demanda
- [ ] Os critérios de aceite foram atendidos
- [ ] O líder ou responsável pelo projeto validou o resultado

---

## US03 — O que foi produzido
> *"Eu, como gerente, quero saber o que foi produzido no dia X pelo setor Y, a fim de verificar a produtividade do setor Y."*

**Implementado em:** `tool_producao_por_data` → procedures.producao.calcular_producao_data.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (gerente)
- [ ] Os setores que serão consultados estão definidos (`produtos_mercado.csv`, coluna Setor)
- [ ] A informação de data está definida como parâmetro de consulta
- [ ] Os produtos estão bem definidos no csv `produtos_mercado.csv`
- [ ] Serão utilizados os csv `produtos_mercado.csv`, `vendas_supermercado_<mês>_<ano>.csv` e `descartes_supermercado_<mês>_<ano>.csv`
- [ ] Os registros de produção estão relacionados ao respectivo setor
- [ ] Está definido como os resultados serão apresentados ao gerente
- [ ] Critérios de aceite estão definidos
- [ ] Dependências identificadas

### DoD
- [ ] O gerente consegue informar o dia X (parâmetro `data`)
- [ ] O gerente consegue selecionar o setor Y (parâmetro `setor`, com correção ortográfica via `normalizar_setor`)
- [ ] O sistema apresenta os produtos produzidos pelo setor no dia selecionado
- [ ] O sistema apresenta a quantidade produzida de cada produto (Total Produzido, Vendas, Descarte por item)
- [ ] Os dados apresentados correspondem aos registros de produção do setor e da data selecionados
- [ ] O sistema permite identificar o total produzido pelo setor no período consultado
- [ ] A consulta funciona corretamente para diferentes datas e setores (casos 3.1 a 3.6 do Relatório de Testes)
- [ ] A funcionalidade foi testada com diferentes cenários
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gerente ou responsável

---

## US04 — O que deveria ter sido produzido
> *"Eu, como gerente, quero saber o que deveria ter sido produzido no dia X pelo setor Y, a fim de consultar a meta ideal."*

**Implementado em:** `tool_meta_producao_passada` → reaproveita `classificar_dia` + `dataframe_vendas_similares` + `media_vendas_produtos` (mesmo cálculo da US01/US02).

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário identificado como gerente
- [ ] Setores e produtos por setor definidos
- [ ] Data definida como parâmetro
- [ ] Unidade de medida da meta definida (unidades)
- [ ] Está definido que a produção real virá da análise de vendas e descartes
- [ ] Critérios de aceite estão definidos
- [ ] Fontes de dados e dependências identificadas
- [ ] Está definido que a meta é a média histórica de dias com o mesmo perfil (+5% de margem), com o mesmo cálculo da US01/US02

### DoD
- [ ] O gerente consegue selecionar o dia X e o setor Y
- [ ] O sistema apresenta a meta de produção prevista para o dia e setor selecionados
- [ ] A funcionalidade foi testada
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gerente ou responsável


---

---

## US05 — O que produzir em cada período do dia (líder)
> *"Eu, como líder, quero saber quais produtos devo produzir em cada período do dia, a fim de otimizar o tempo dos colaboradores."*

**Previsto em:** previsão de produção da Sprint 1 (média de dias similares + 5%) com um novo recorte por período.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (líder)
- [ ] Está definido como o setor do líder é informado (parâmetro `setor`, com correção ortográfica via `normalizar_setor`)
- [ ] Os períodos do dia estão definidos (a definir; proposta: manhã, tarde e noite, com faixas de horário)
- [ ] Está definida a origem do horário de cada venda (coluna de hora nos CSV `vendas_supermercado_<mês>_<ano>.csv` ou regra para derivar o período)
- [ ] Está definido o que acontece quando a base não tem horário (a definir)
- [ ] Está definido como a previsão por período se relaciona com a previsão do dia da Sprint 1, sem duplicar regra
- [ ] Está definido o que acontece quando o líder não informa o período (a definir; proposta: mostrar todos os períodos)
- [ ] Está definido como o resultado será apresentado (período, produto e quantidade a produzir)
- [ ] Exemplos reais de frases estão mapeados ("o que produzo de manhã?", "o que fazer à tarde?")
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas (previsão da Sprint 1)

### DoD
- [ ] O líder consegue consultar o que produzir em um período específico ou em todos
- [ ] O sistema apresenta, por período, os produtos e as quantidades
- [ ] Os valores de cada período são coerentes com a previsão do dia da Sprint 1 (verificação cruzada; a soma dos períodos pode divergir, pois cada período é projetado separadamente)
- [ ] O setor com erro de digitação é corrigido por `normalizar_setor`
- [ ] Período sem histórico ou inexistente na base (ex.: madrugada) recebe resposta clara: a MIA informa o período usado em vez de substituí-lo em silêncio, e não inventa produto
- [ ] A pergunta de produção do dia (Sprint 1) continua funcionando e não é confundida com a nova
- [ ] A funcionalidade foi testada sem erros (casos 5.1 a 5.8 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo líder ou responsável

> **Pendências dos testes (5.2, 5.7 e 5.8):** a resposta com todos os períodos não é única e precisa de melhoria no formatador final; "madrugada" é convertida em "noite" sem avisar o usuário; o caso 5.8 ainda não foi concluído.

---

## US06 — Reais descartados em cada setor (gerente)
> *"Eu, como gerente, quero saber quantos reais foram descartados em cada setor, a fim de monitorar o impacto financeiro das perdas dos setores."*

**Previsto em:** `tool_buscar_por_intervalo` (categoria `DESPERDICIO`), a partir de `procedures.descarte` + custo dos ingredientes. A mesma tool é reaproveitada pela US07. A confirmar no Planning.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (gerente)
- [ ] Está definido que, sem setor, a tool devolve o total da empresa e que, para ver cada setor, a MIA consulta setor a setor (Padaria, Cozinha, Peixaria, Açougue e Processados)
- [ ] Está definido se o gerente pode pedir um setor específico (parâmetro `setor` opcional)
- [ ] Está definido se o líder ainda poderá consultar o próprio setor (a definir; hoje a história é do gerente)
- [ ] Fórmula do valor descartado está definida (custo dos ingredientes da receita × quantidade descartada, usando o preço de custo histórico até a data do descarte)
- [ ] Origem dos custos está definida (`historico_ingredientes.csv` e as receitas dos produtos)
- [ ] Período de análise está definido (dia, semana ou mês) e o que acontece quando não é informado
- [ ] Serão utilizados os CSV de descartes, `produtos.csv` e `historico_ingredientes.csv`
- [ ] Está definido como o resultado será apresentado (valor em R$ de cada setor e, se houver, o total geral)
- [ ] O Agente Roteador distingue "quantos reais" de "quantas unidades"
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas (custo dos ingredientes, compartilhado com as US07 e US08)

### DoD
- [ ] O gerente consegue consultar o valor descartado de cada setor em um dia ou período
- [ ] O sistema apresenta o valor em R$ de cada setor e, se apresentar um total geral, ele é igual à soma dos setores
- [ ] A soma dos valores por setor é igual ao total geral (verificação cruzada)
- [ ] O valor em R$ é coerente com as unidades descartadas exibidas na Sprint 1
- [ ] A pergunta em unidades continua respondida em unidades, sem virar R$
- [ ] O setor com erro de digitação é corrigido por `normalizar_setor`
- [ ] Setor sem descarte no período aparece com R$ 0,00 ou é informado, sem quebrar o total
- [ ] A funcionalidade foi testada sem erros (casos 6.1 a 6.6 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gerente ou responsável

> **Pendências dos testes (6.1, 6.3 e 6.6):** a tool de desperdício devolve só o total; o detalhamento por setor (valor de cada setor e total geral) ainda não é feito. Os casos 6.3 e 6.6 ainda não foram concluídos.

---

## US07 — Reais descartados na empresa (gerente)
> *"Eu, como gerente, quero saber quantos reais foram descartados, a fim de avaliar o custo global de desperdício da empresa."*

**Previsto em:** mesmo *service* da US06, sem filtro de setor. A confirmar no Planning.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (gerente)
- [ ] Está definido que o escopo é a empresa inteira (todos os setores)
- [ ] Está definido que o cálculo é o mesmo da US06, sem duplicar regra de negócio
- [ ] Período de análise está definido (dia, semana ou mês)
- [ ] Serão utilizados os CSV de descartes, `produtos.csv` e `historico_ingredientes.csv`
- [ ] Está definido como o resultado será apresentado (total geral e, quando solicitado, separado por setor)
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas (US06)

### DoD
- [ ] O gerente consegue consultar o valor total descartado pela empresa em um dia ou período
- [ ] O sistema apresenta o total geral em R$ e, quando solicitado, o valor de cada setor
- [ ] A soma dos valores por setor é igual ao total geral (verificação cruzada com a US06)
- [ ] A pergunta em unidades continua respondida em unidades, sem virar R$
- [ ] A funcionalidade foi testada sem erros (casos 7.1 a 7.3 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gerente ou responsável

> **Pendência do teste 7.3:** o total da empresa funciona (7.1 e 7.2), mas a separação por setor não é fornecida pela tool.

---

## US08 — Produtos mais lucrativos na empresa (gerente)
> *"Eu, como gerente, quero saber quais produtos me trazem mais lucro, a fim de orientar estrategicamente os setores."*

**Previsto em:** categoria `VENDAS` do Agente Roteador (já reconhecida, ainda sem tools registradas) + novo *service* de lucro. A confirmar no Planning.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (gerente)
- [ ] Está definido que o escopo é a empresa inteira (todos os setores)
- [ ] Fórmula de lucro está definida (a definir; proposta: (preço de venda − custo unitário) × quantidade vendida) e se o custo do descarte entra no cálculo
- [ ] Origem do preço de venda e do custo unitário está definida (o código atual não usa essas colunas: confirmar se já existem nos CSV ou se serão adicionadas)
- [ ] Está definido se o ranking pode ser agrupado por setor e limitado a um número de itens (ex.: "os 5 mais lucrativos")
- [ ] Período de análise está definido (dia, semana ou mês) e o que acontece quando o período não é informado
- [ ] Serão utilizados os CSV `produtos_mercado.csv` e `vendas_supermercado_<mês>_<ano>.csv`
- [ ] Está definido como o ranking será apresentado (ordem decrescente, valores em R$, com o setor de cada produto)
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas (custo unitário compartilhado com as US06 e US07)

### DoD
- [ ] O gerente consegue consultar o ranking de lucro de todos os produtos da empresa
- [ ] O sistema apresenta os produtos do mais para o menos lucrativo, com o lucro de cada item em R$ e o setor
- [ ] O sistema permite comparar os setores (ranking agrupado por setor)
- [ ] Os valores conferem com o cálculo manual feito sobre uma amostra dos CSV (verificação cruzada)
- [ ] Produtos sem vendas no período não distorcem o ranking
- [ ] A funcionalidade foi testada sem erros (casos 8.1 a 8.4 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gerente ou responsável

---

## US09 — Perguntas por áudio (gestor)
> *"Eu, como gestor, quero interagir com o assistente de análise de dados enviando perguntas por áudio, a fim de obter insights das planilhas de forma fluida e sem contato manual (semelhante a uma Alexa)."*

**Previsto em:** `bot/telegram_bot.py` (hoje a mensagem de voz recebe a resposta de formato não suportado) + etapa de transcrição antes do `processar_mensagem`. A confirmar no Planning.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (gestor)
- [ ] Solução de transcrição escolhida e executada **localmente** (restrição do projeto: sem APIs externas de terceiros)
- [ ] Idioma (pt-BR), formato do áudio do Telegram e duração máxima estão definidos
- [ ] Está definido se a resposta será em texto, em voz ou em ambos (a definir)
- [ ] Está definido o comportamento quando a transcrição falha (áudio vazio, ruído ou longo demais)
- [ ] Exemplos de perguntas faladas estão mapeados (as mesmas das histórias anteriores, ditas em voz alta, incluindo as novas US05 e US06)
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas

### DoD
- [ ] O gestor envia um áudio e recebe a resposta correta, sem digitar nada
- [ ] A resposta ao áudio tem o mesmo conteúdo da resposta à pergunta digitada
- [ ] Áudio vazio, com ruído ou acima do limite recebe uma mensagem amigável, sem travar o bot
- [ ] Mensagens de texto continuam funcionando; formatos não suportados (ex.: foto) continuam recusados
- [ ] A transcrição funciona sem nenhuma API externa de terceiros
- [ ] Arquivos de áudio temporários são apagados após o uso
- [ ] O fluxo de áudio foi documentado no `arquitetura.md`
- [ ] A funcionalidade foi testada sem erros (casos 9.1 a 9.9 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gestor ou responsável

---

## US10 — Matéria-prima para o dia seguinte (líder)
> *"Eu, como líder, quero saber quanta matéria-prima eu preciso deixar preparada para o dia seguinte, a fim de otimizar o tempo e reduzir o desperdício de matéria-prima."*

**Previsto em:** `services.producao` (previsão do dia, US01/US02) × consumo de matéria-prima por produto (novo CSV). A confirmar no Planning.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (líder)
- [ ] Está definida a origem do consumo de matéria-prima por unidade de cada produto (receita; ainda inexistente na base)
- [ ] Está definida a unidade de medida de cada matéria-prima (kg, L, unidade)
- [ ] Está definido que a data alvo é o dia seguinte e que o parâmetro `data` aceita "amanhã"
- [ ] Está definido que a necessidade parte da previsão de produção já existente (média de dias similares + 5%)
- [ ] Está definido como o resultado será apresentado (matéria-prima, quantidade e unidade, por setor)
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas (previsão de produção da Sprint 1)

### DoD
- [ ] O líder consegue consultar a matéria-prima necessária para amanhã no seu setor
- [ ] O sistema apresenta cada matéria-prima com quantidade e unidade
- [ ] A mesma matéria-prima usada por vários produtos aparece somada
- [ ] A quantidade é coerente com a previsão de produção do mesmo dia (verificação cruzada)
- [ ] O setor com erro de digitação é corrigido por `normalizar_setor`
- [ ] Produto sem receita cadastrada é informado, sem inventar consumo
- [ ] A funcionalidade foi testada sem erros (casos 10.1 a 10.6 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo líder ou responsável

> **Pendências dos testes (10.1, 10.2, 10.4 e 10.6):** o nome do produto se repete para cada matéria-prima; ingredientes com fração (ex.: `0.1` kg) são calculados errado; a unidade aparece como `unidades` em vez de kg ou L; respostas longas geram o erro `MESSAGE_TOO_LONG` no Telegram.

---

---

## US11 — Matérias-primas disponíveis para transferir (líder)
> *"Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias."*

**Implementado em:** `ia/tools/materia_prima_tool.py` — `tool_realocacao_sobra_mp`.

### DoR
- [x] Objetivo e usuário da história estão definidos
- [x] Origem da necessidade prevista (US10), estoque e unidade dos ingredientes está identificada
- [x] Regra de sobra está definida como estoque menos necessidade prevista
- [x] Filtro opcional de setor de origem está definido
- [x] Cenários de falta de histórico, receita ausente e ausência de sobra estão definidos no BDD
- [x] Critérios de aceitação e dependências estão identificados

### DoD
- [x] A tool identifica sobras disponíveis por ingrediente e setor
- [x] A necessidade prevista do setor de origem é preservada
- [x] A resposta mostra quantidade, unidade e setor de origem
- [x] O filtro de origem limita as sobras consideradas
- [x] Ausência de sobra ou dados recebe resposta clara
- [x] Os estoques permanecem inalterados
- [x] Casos US-11 do Guia de Testes da Sprint 3 foram executados
- [x] Critérios de aceitação atendidos e resultado validado

---

## US12 — Recomendação de transferência de matéria-prima (gerente)
> *"Eu, como gerente, quero identificar transferências de matéria-prima recomendadas entre setores, a fim de cobrir déficits sem comprometer a necessidade do setor de origem."*

**Implementado em:** `ia/tools/materia_prima_tool.py` — `tool_realocacao_sobra_mp`.

### DoR
- [x] Objetivo e usuário da história estão definidos
- [x] A regra de déficit e a quantidade máxima transferível estão definidas
- [x] Ingrediente e unidade precisam coincidir entre origem e destino
- [x] A resposta deve mostrar origem, destino, quantidade, déficit residual e justificativa
- [x] Está definido que a recomendação não registra nem executa a transferência
- [x] Cenários de transferência parcial, falta inexistente e dados ausentes estão no BDD
- [x] Critérios de aceitação e dependências estão identificados

### DoD
- [x] A MIA recomenda transferências apenas para déficits do mesmo ingrediente
- [x] A recomendação não reduz o estoque da origem abaixo da necessidade prevista
- [x] Transferências parciais informam o déficit restante
- [x] Ausência de transferência recomendada recebe resposta clara
- [x] Os estoques permanecem inalterados
- [x] Casos US-12 do Guia de Testes da Sprint 3 foram executados
- [x] Critérios de aceitação atendidos e resultado validado

---

## Requisito transversal — Menu de ajuda e perguntas por voz

### DoR
- [x] Categorias do menu correspondem às tools disponíveis: Produção, Matéria-prima, Descarte, Produtos e Vendas
- [x] Os comandos `/ajuda` e `/help` estão definidos
- [x] Perguntas por voz reutilizam as mesmas intenções e tools das perguntas por texto
- [x] Perguntas de previsão com “o que” ou “quanto” retornam quantidades

### DoD
- [x] `/ajuda` e `/help` abrem o menu inline no TeleBot
- [x] Escolher categoria mostra exemplos de pergunta
- [x] Escolher uma pergunta executa o mesmo fluxo da mensagem digitada
- [x] O menu retorna uma navegação para os assuntos
- [x] Perguntas por áudio reutilizam o fluxo da mensagem de texto e não separam “o que” de “quanto”
- [x] As previsões de produção sempre apresentam quantidades, independentemente de a pergunta usar “o que” ou “quanto”
- [x] Os casos de menu foram executados

> **Limite da validação transversal:** os handlers e a navegação foram testados localmente com `BotFake`. O TeleBot ao vivo e a gravação/transcrição de áudio físico não foram executados nesta rodada; consulte os limites do [Relatório de Testes da Sprint 3](./testes/Relat%C3%B3rio%20de%20Testes%20-%20Sprint%203.md).
