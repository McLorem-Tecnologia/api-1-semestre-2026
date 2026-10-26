# Checklist de DoR e DoD — Sprint 2

A Sprint 2 reúne as histórias **US05 a US08** (meta da Sprint) e as **US09 a US12** (previsão, sem compromisso de entrega), vindas da Sprint 3. As **US09** e **US10** foram entregues; as **US11** e **US12** não foram entregues e passam para a Sprint 3. Em relação à versão anterior, o texto da **US05** e o da **US06** foram alterados; as **US07** e **US08** continuam como estavam.

|  US   | De                                                                                                                              | Para                                                                                                                                           |
| :---: | :------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------- |
|  05   | "...quero saber quais produtos me trazem mais lucro, a fim de otimizar o tempo dos colaboradores."                              | "...quero saber quais produtos devo produzir em cada período do dia, a fim de otimizar o tempo dos colaboradores."                             |
|  06   | "Eu, como líder, quero saber quantos reais foram descartados, a fim de monitorar o impacto financeiro das perdas do meu setor." | "Eu, como gerente, quero saber quantos reais foram descartados em cada setor, a fim de monitorar o impacto financeiro das perdas dos setores." |

Regras compartilhadas desta Sprint:

- As **US06 e US07** compartilham o mesmo cálculo de valor descartado (custo dos ingredientes da receita × quantidade descartada): a US06 mostra o valor de cada setor e a US07 mostra o total da empresa. O cálculo deve ficar em um **único *service***, sem duplicar a regra de negócio.
- O lucro (US08) usa preço de venda e custo unitário e fica em um *service* próprio. A US05 deixou de tratar de lucro.
- A pergunta em **unidades** ("quantas unidades foram descartadas") continua respondida em unidades. Só a pergunta em **reais** responde em R$.
- Em todas as histórias, a MIA deve informar quando não houver registro, em vez de inventar uma resposta.
- A US09 adiciona uma nova **forma de entrada** (voz) e vale para todas as demais perguntas.
- A US10 reaproveita a previsão de produção da Sprint 1, e a US11 depende da necessidade calculada na US10.

---

## US05 — O que produzir em cada período do dia (líder)
> *"Eu, como líder, quero saber quais produtos devo produzir em cada período do dia, a fim de otimizar o tempo dos colaboradores."*

**Previsto em:** previsão de produção da Sprint 1 (média de dias similares + 30%) com um novo recorte por período. A confirmar no Planning.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (líder)
- [x] Está definido como o setor do líder é informado (parâmetro `setor`, com correção ortográfica via `normalizar_setor`)
- [x] Os períodos do dia estão definidos (a definir; proposta: manhã, tarde e noite, com faixas de horário)
- [x] Está definida a origem do horário de cada venda (coluna de hora nos CSV `vendas_supermercado_<mês>_<ano>.csv` ou regra para derivar o período)
- [x] Está definido o que acontece quando a base não tem horário (a definir)
- [x] Está definido como a previsão por período se relaciona com a previsão do dia da Sprint 1, sem duplicar regra
- [x] Está definido o que acontece quando o líder não informa o período (a definir; proposta: mostrar todos os períodos)
- [x] Está definido como o resultado será apresentado (período, produto e quantidade a produzir)
- [x] Exemplos reais de frases estão mapeados ("o que produzo de manhã?", "o que fazer à tarde?")
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas (previsão da Sprint 1)

### DoD
- [x] O líder consegue consultar o que produzir em um período específico ou em todos
- [x] O sistema apresenta, por período, os produtos e as quantidades
- [x] Os valores de cada período são coerentes com a previsão do dia da Sprint 1 (verificação cruzada; a soma dos períodos pode divergir, pois cada período é projetado separadamente)
- [x] O setor com erro de digitação é corrigido por `normalizar_setor`
- [ ] Período sem histórico ou inexistente na base (ex.: madrugada) recebe resposta clara: a MIA informa o período usado em vez de substituí-lo em silêncio, e não inventa produto
- [x] A pergunta de produção do dia (Sprint 1) continua funcionando e não é confundida com a nova
- [ ] A funcionalidade foi testada sem erros (casos 5.1 a 5.8 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [x] O resultado foi validado pelo líder ou responsável

> **Pendências dos testes (5.2, 5.7 e 5.8):** a resposta com todos os períodos não é única e precisa de melhoria no formatador final; "madrugada" é convertida em "noite" sem avisar o usuário; o caso 5.8 ainda não foi concluído.

---

## US06 — Reais descartados em cada setor (gerente)
> *"Eu, como gerente, quero saber quantos reais foram descartados em cada setor, a fim de monitorar o impacto financeiro das perdas dos setores."*

**Previsto em:** `tool_buscar_por_intervalo` (categoria `DESPERDICIO`), a partir de `procedures.descarte` + custo dos ingredientes. A mesma tool é reaproveitada pela US07. A confirmar no Planning.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (gerente)
- [ ] Está definido que, sem setor, a tool devolve o total da empresa e que, para ver cada setor, a MIA consulta setor a setor (Padaria, Cozinha, Peixaria, Açougue e Processados)
- [x] Está definido se o gerente pode pedir um setor específico (parâmetro `setor` opcional)
- [x] Está definido se o líder ainda poderá consultar o próprio setor (a definir; hoje a história é do gerente)
- [x] Fórmula do valor descartado está definida (custo dos ingredientes da receita × quantidade descartada, usando o preço de custo histórico até a data do descarte)
- [x] Origem dos custos está definida (`historico_ingredientes.csv` e as receitas dos produtos)
- [x] Período de análise está definido (dia, semana ou mês) e o que acontece quando não é informado
- [x] Serão utilizados os CSV de descartes, `produtos.csv` e `historico_ingredientes.csv`
- [ ] Está definido como o resultado será apresentado (valor em R$ de cada setor e, se houver, o total geral)
- [x] O Agente Roteador distingue "quantos reais" de "quantas unidades"
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas (custo dos ingredientes, compartilhado com as US07 e US08)

### DoD
- [x] O gerente consegue consultar o valor descartado de cada setor em um dia ou período
- [ ] O sistema apresenta o valor em R$ de cada setor e, se apresentar um total geral, ele é igual à soma dos setores
- [ ] A soma dos valores por setor é igual ao total geral (verificação cruzada)
- [x] O valor em R$ é coerente com as unidades descartadas exibidas na Sprint 1
- [x] A pergunta em unidades continua respondida em unidades, sem virar R$
- [x] O setor com erro de digitação é corrigido por `normalizar_setor`
- [x] Setor sem descarte no período aparece com R$ 0,00 ou é informado, sem quebrar o total
- [ ] A funcionalidade foi testada sem erros (casos 6.1 a 6.6 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [x] O resultado foi validado pelo gerente ou responsável

> **Pendências dos testes (6.1, 6.3 e 6.6):** a tool de desperdício devolve só o total; o detalhamento por setor (valor de cada setor e total geral) ainda não é feito. Os casos 6.3 e 6.6 ainda não foram concluídos.

---

## US07 — Reais descartados na empresa (gerente)
> *"Eu, como gerente, quero saber quantos reais foram descartados, a fim de avaliar o custo global de desperdício da empresa."*

**Previsto em:** mesmo *service* da US06, sem filtro de setor. A confirmar no Planning.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (gerente)
- [x] Está definido que o escopo é a empresa inteira (todos os setores)
- [x] Está definido que o cálculo é o mesmo da US06, sem duplicar regra de negócio
- [x] Período de análise está definido (dia, semana ou mês)
- [x] Serão utilizados os CSV de descartes, `produtos.csv` e `historico_ingredientes.csv`
- [ ] Está definido como o resultado será apresentado (total geral e, quando solicitado, separado por setor)
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas (US06)

### DoD
- [x] O gerente consegue consultar o valor total descartado pela empresa em um dia ou período
- [ ] O sistema apresenta o total geral em R$ e, quando solicitado, o valor de cada setor
- [ ] A soma dos valores por setor é igual ao total geral (verificação cruzada com a US06)
- [x] A pergunta em unidades continua respondida em unidades, sem virar R$
- [ ] A funcionalidade foi testada sem erros (casos 7.1 a 7.3 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [x] O resultado foi validado pelo gerente ou responsável

> **Pendência do teste 7.3:** o total da empresa funciona (7.1 e 7.2), mas a separação por setor não é fornecida pela tool.

---

## US08 — Produtos mais lucrativos na empresa (gerente)
> *"Eu, como gerente, quero saber quais produtos me trazem mais lucro, a fim de orientar estrategicamente os setores."*

**Previsto em:** categoria `VENDAS` do Agente Roteador (já reconhecida, ainda sem tools registradas) + novo *service* de lucro. A confirmar no Planning.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (gerente)
- [x] Está definido que o escopo é a empresa inteira (todos os setores)
- [x] Fórmula de lucro está definida (a definir; proposta: (preço de venda − custo unitário) × quantidade vendida) e se o custo do descarte entra no cálculo
- [x] Origem do preço de venda e do custo unitário está definida (o código atual não usa essas colunas: confirmar se já existem nos CSV ou se serão adicionadas)
- [x] Está definido se o ranking pode ser agrupado por setor e limitado a um número de itens (ex.: "os 5 mais lucrativos")
- [x] Período de análise está definido (dia, semana ou mês) e o que acontece quando o período não é informado
- [x] Serão utilizados os CSV `produtos_mercado.csv` e `vendas_supermercado_<mês>_<ano>.csv`
- [x] Está definido como o ranking será apresentado (ordem decrescente, valores em R$, com o setor de cada produto)
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas (custo unitário compartilhado com as US06 e US07)

### DoD
- [x] O gerente consegue consultar o ranking de lucro de todos os produtos da empresa
- [x] O sistema apresenta os produtos do mais para o menos lucrativo, com o lucro de cada item em R$ e o setor
- [x] O sistema permite comparar os setores (ranking agrupado por setor)
- [x] Os valores conferem com o cálculo manual feito sobre uma amostra dos CSV (verificação cruzada)
- [x] Produtos sem vendas no período não distorcem o ranking
- [x] A funcionalidade foi testada sem erros (casos 8.1 a 8.4 do Guia de Testes)
- [x] Os critérios de aceite foram atendidos
- [x] O resultado foi validado pelo gerente ou responsável

---

## US09 — Perguntas por áudio (gestor)
> *"Eu, como gestor, quero interagir com o assistente de análise de dados enviando perguntas por áudio, a fim de obter insights das planilhas de forma fluida e sem contato manual (semelhante a uma Alexa)."*

**Previsto em:** `bot/telegram_bot.py` (hoje a mensagem de voz recebe a resposta de formato não suportado) + etapa de transcrição antes do `processar_mensagem`. A confirmar no Planning.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (gestor)
- [x] Solução de transcrição escolhida e executada **localmente** (restrição do projeto: sem APIs externas de terceiros)
- [x] Idioma (pt-BR), formato do áudio do Telegram e duração máxima estão definidos
- [x] Está definido se a resposta será em texto, em voz ou em ambos (a definir)
- [x] Está definido o comportamento quando a transcrição falha (áudio vazio, ruído ou longo demais)
- [x] Exemplos de perguntas faladas estão mapeados (as mesmas das histórias anteriores, ditas em voz alta, incluindo as novas US05 e US06)
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas

### DoD
- [x] O gestor envia um áudio e recebe a resposta correta, sem digitar nada
- [x] A resposta ao áudio tem o mesmo conteúdo da resposta à pergunta digitada
- [x] Áudio vazio, com ruído ou acima do limite recebe uma mensagem amigável, sem travar o bot
- [x] Mensagens de texto continuam funcionando; formatos não suportados (ex.: foto) continuam recusados
- [x] A transcrição funciona sem nenhuma API externa de terceiros
- [x] Arquivos de áudio temporários são apagados após o uso
- [x] O fluxo de áudio foi documentado no `arquitetura.md`
- [x] A funcionalidade foi testada sem erros (casos 9.1 a 9.9 do Guia de Testes)
- [x] Os critérios de aceite foram atendidos
- [x] O resultado foi validado pelo gestor ou responsável

---

## US10 — Matéria-prima para o dia seguinte (líder)
> *"Eu, como líder, quero saber quanta matéria-prima eu preciso deixar preparada para o dia seguinte, a fim de otimizar o tempo e reduzir o desperdício de matéria-prima."*

**Previsto em:** `services.producao` (previsão do dia, US01/US02) × consumo de matéria-prima por produto (novo CSV). A confirmar no Planning.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (líder)
- [x] Está definida a origem do consumo de matéria-prima por unidade de cada produto (receita; ainda inexistente na base)
- [x] Está definida a unidade de medida de cada matéria-prima (kg, L, unidade)
- [x] Está definido que a data alvo é o dia seguinte e que o parâmetro `data` aceita "amanhã"
- [x] Está definido que a necessidade parte da previsão de produção já existente (média de dias similares + 30%)
- [x] Está definido como o resultado será apresentado (matéria-prima, quantidade e unidade, por setor)
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas (previsão de produção da Sprint 1)

### DoD
- [x] O líder consegue consultar a matéria-prima necessária para amanhã no seu setor
- [ ] O sistema apresenta cada matéria-prima com quantidade e unidade
- [x] A mesma matéria-prima usada por vários produtos aparece somada
- [ ] A quantidade é coerente com a previsão de produção do mesmo dia (verificação cruzada)
- [x] O setor com erro de digitação é corrigido por `normalizar_setor`
- [x] Produto sem receita cadastrada é informado, sem inventar consumo
- [ ] A funcionalidade foi testada sem erros (casos 10.1 a 10.6 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [x] O resultado foi validado pelo líder ou responsável

> **Pendências dos testes (10.1, 10.2, 10.4 e 10.6):** o nome do produto se repete para cada matéria-prima; ingredientes com fração (ex.: `0.1` kg) são calculados errado; a unidade aparece como `unidades` em vez de kg ou L; respostas longas geram o erro `MESSAGE_TOO_LONG` no Telegram.

---

## US11 — Matérias-primas disponíveis para transferir (líder)
> *"Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias."*

> **Não entregue na Sprint 2:** história da previsão (sem compromisso de entrega) que passa para a Sprint 3. Os itens abaixo seguem pendentes.

**Previsto em:** novo *service* de estoque de matéria-prima, usando a necessidade calculada na US10. A confirmar no Planning.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (líder)
- [ ] Está definida a origem do estoque atual de matéria-prima por setor (ainda inexistente na base)
- [ ] Está definida a regra de "disponível para transferir" (a definir; proposta: estoque menos a necessidade prevista da US10)
- [ ] Está definido como o resultado será apresentado (matéria-prima, quantidade e setor que a possui)
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas (US10)

### DoD
- [ ] O líder consegue consultar as matérias-primas com sobra
- [ ] O sistema apresenta quantidade e setor de cada item disponível
- [ ] Nenhum item é listado como disponível quando o próprio setor precisa dele no dia seguinte (verificação cruzada com a US10)
- [ ] Quando não há sobra, a MIA informa isso, sem inventar itens
- [ ] A funcionalidade foi testada sem erros (casos 11.1 a 11.5 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo líder ou responsável

---
---

## US12 — Motivo da transferência de um produto (gerente)
> *"Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção."*

> **Não entregue na Sprint 2:** história da previsão (sem compromisso de entrega) que passa para a Sprint 3. Os itens abaixo seguem pendentes.

**Previsto em:** novo *service* de transferências, a partir de um registro com data, produto, setor de origem, setor de destino e motivo. A confirmar no Planning.

### DoR
- [ ] Objetivo da User Story está claramente definido
- [ ] Usuário da funcionalidade está identificado (gerente)
- [ ] Está definido o que é uma "transferência" (produto que muda de setor ou matéria-prima enviada a outro setor)
- [ ] Está definida a origem do registro de transferências, com o campo de **motivo** (ainda inexistente na base)
- [ ] Está definido o comportamento quando o produto não existe ou não tem transferência registrada
- [ ] Está definido como o resultado será apresentado (motivo, setor de origem, setor de destino e data)
- [ ] Critérios de aceite estão definidos
- [ ] Dependências necessárias estão identificadas

### DoD
- [ ] O gerente consegue perguntar o motivo da transferência de um produto pelo nome
- [ ] O motivo apresentado corresponde exatamente ao registro
- [ ] Produto inexistente ou sem transferência registrada recebe uma resposta clara, sem motivo inventado
- [ ] O nome do produto é reconhecido independentemente de maiúsculas e minúsculas
- [ ] A funcionalidade foi testada sem erros (casos 12.1 a 12.5 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gerente ou responsável
