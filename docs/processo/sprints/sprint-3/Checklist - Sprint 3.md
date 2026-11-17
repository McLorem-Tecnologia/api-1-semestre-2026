# Checklist de DoR e DoD — Sprint 3

A Sprint 3 reúne as histórias **US11 e US12** (meta da Sprint), que já eram desta Sprint no backlog original e não foram entregues na Sprint 2, e as **melhorias técnicas M1 a M4**, que não têm Story Points. O texto das duas User Stories não foi alterado.

Regras compartilhadas desta Sprint:

- A **US11** depende da necessidade de matéria-prima calculada na US10: o que está disponível para transferir é o estoque do setor menos a necessidade prevista para o dia seguinte. Esse cálculo fica em um **único *service***, usado pela US10 e pela US11, sem duplicar a regra de negócio.
- A **US12** consulta um registro de transferências (`dados/transferencias.csv`), com data, produto (SKU), setor de origem, setor de destino e motivo.
- Pela **M1**, toda resposta que lista produtos ou matérias-primas traz a quantidade e os setores separados, mesmo quando a pergunta cita um único setor. As perguntas "quais" e "quantos" têm a mesma resposta, e a **US01** deixa de ter um tratamento separado no código.
- Em todas as histórias, a MIA deve informar quando não houver registro, em vez de inventar uma resposta.
- A forma de entrada por áudio (US09) vale para todas as perguntas: a resposta a um áudio é igual à resposta ao texto.
- Cada tarefa é desenvolvida em uma branch própria, com Pull Request revisado antes do merge, conforme a [Estratégia de Branch](../../Estratégia%20de%20Branch.md).

---

## US11 — Matérias-primas disponíveis para transferir (líder)
> *"Eu, como líder, quero saber quais matérias-primas estão disponíveis para transferir a outros setores, a fim de reaproveitar recursos parados e evitar compras desnecessárias."*

**Previsto em:** novo *service* de matéria-prima (`services.materia_prima`), que calcula a necessidade do dia seguinte (receita × previsão de produção da Sprint 1) e a compara com o estoque de cada setor (`ingredientes.csv`), e nova tool na categoria `PRODUCAO`.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (líder)
- [x] Está definida a origem do estoque atual de matéria-prima por setor (coluna `Estoque Atual` de `ingredientes.csv`, por ingrediente e setor)
- [x] Está definida a regra de "disponível para transferir" (estoque do setor menos a necessidade prevista da US10; só entra o que tem sobra maior que zero)
- [x] Está definido que, sem data, a necessidade considerada é a do dia seguinte, e que o parâmetro `data` aceita "amanhã" e demais datas relativas
- [x] Está definido que o setor é opcional (sem setor, a MIA traz todos) e que o erro de digitação é corrigido por `normalizar_setor`
- [x] Está definido que a pergunta pode citar uma matéria-prima específica (parâmetro `ingrediente` opcional)
- [x] Está definido como o resultado será apresentado (setores separados, com cada matéria-prima, a quantidade disponível e a unidade de medida)
- [x] Exemplos reais de frases estão mapeados ("quais matérias-primas posso transferir?", "o que sobra de ingrediente na padaria?")
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas (US10 e M4)

### DoD
- [ ] O líder consegue consultar as matérias-primas com sobra, no seu setor ou em todos
- [ ] O sistema apresenta, por setor, cada matéria-prima com a quantidade disponível e a unidade de medida
- [ ] Nenhum item é listado como disponível quando o próprio setor precisa dele no dia seguinte (verificação cruzada com a US10: estoque menos necessidade é igual à quantidade informada)
- [ ] Quando não há sobra, a MIA informa isso, sem inventar itens
- [ ] A pergunta sobre uma matéria-prima específica mostra a quantidade disponível em cada setor que a possui
- [ ] O setor com erro de digitação é corrigido por `normalizar_setor`
- [ ] A resposta longa é enviada em mais de uma mensagem, sem erro no Telegram (M2)
- [ ] A funcionalidade foi testada sem erros (casos 11.1 a 11.8 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo líder ou responsável

---

## US12 — Motivo da transferência de um produto (gerente)
> *"Eu, como gerente, quero saber por que o produto X está sendo transferido de setor, a fim de identificar falhas no planejamento original da produção."*

**Previsto em:** novo *service* de transferências (`services.transferencias`), a partir de `procedures.transferencias`, que lê o registro `dados/transferencias.csv`, e nova tool na categoria `PRODUCAO`.

### DoR
- [x] Objetivo da User Story está claramente definido
- [x] Usuário da funcionalidade está identificado (gerente)
- [x] Está definido o que é uma "transferência" (um produto que sai de um setor de origem para um setor de destino)
- [x] Está definida a origem do registro de transferências (`dados/transferencias.csv`, com as colunas `Data`, `SKU`, `Setor Origem`, `Setor Destino` e `Motivo`; o nome do produto vem de `produtos.csv`)
- [x] Está definido que o produto é informado pelo nome, sem diferenciar maiúsculas e minúsculas
- [x] Está definido o comportamento quando o produto não existe ou não tem transferência registrada (a MIA informa, sem inventar um motivo)
- [x] Está definido o comportamento quando o produto tem mais de uma transferência (todas são apresentadas, da mais recente para a mais antiga)
- [x] Está definido como o resultado será apresentado (produto, data, setor de origem, setor de destino e motivo)
- [x] Exemplos reais de frases estão mapeados ("por que a coxinha está sendo transferida de setor?", "qual o motivo da transferência do pudim?")
- [x] Critérios de aceite estão definidos
- [x] Dependências necessárias estão identificadas (novo registro de transferências)

### DoD
- [ ] O gerente consegue perguntar o motivo da transferência de um produto pelo nome
- [ ] O motivo apresentado corresponde exatamente ao registro
- [ ] O sistema apresenta o setor de origem, o setor de destino e a data de cada transferência
- [ ] Produto inexistente ou sem transferência registrada recebe uma resposta clara, sem motivo inventado
- [ ] O nome do produto é reconhecido independentemente de maiúsculas e minúsculas
- [ ] Arquivo de transferências ausente, vazio ou fora do formato não derruba o bot: a MIA informa que não conseguiu consultar o registro
- [ ] A funcionalidade foi testada sem erros (casos 12.1 a 12.8 do Guia de Testes)
- [ ] Os critérios de aceite foram atendidos
- [ ] O resultado foi validado pelo gerente ou responsável

---

## M1 — Resposta padronizada por setor
> *Toda resposta que lista produtos ou informa valores descartados traz a quantidade (ou o valor) e os setores separados, mesmo quando a pergunta cita um único setor.*

**Previsto em:** formatador único de resposta por setor, usado pelas tools de produção (`tool_previsao_vendas_por_data`, `tool_meta_producao_passada`, `tool_producao_por_data`, `tool_previsao_vendas_por_periodo` e `tool_previsao_quantidade_mp`) e pela tool de desperdício.

### DoR
- [x] Comportamento esperado está claramente definido (produto, quantidade e unidade de medida, sob o título de cada setor)
- [x] Está definido que as perguntas "quais" e "quantos" recebem a mesma resposta
- [x] Está definido que, quando a pergunta cita um único setor, a resposta traz o título desse setor
- [x] Está definido que, sem setor, todos os setores aparecem separados, em ordem alfabética
- [x] Está definido que, na previsão por período, os períodos aparecem em ordem cronológica (manhã, tarde, noite) dentro de cada setor, no mesmo formato
- [x] Está definido que o valor descartado é apresentado por setor, com o total geral igual à soma dos setores
- [x] Cenários de teste estão mapeados no Guia de Testes (casos M1.1 a M1.11)

### DoD
- [ ] As perguntas "quais" e "quantos" recebem exatamente a mesma resposta
- [ ] A resposta traz o produto, a quantidade e a unidade de medida do cadastro (Kg, Un, Porção ou L)
- [ ] Com um único setor na pergunta, a resposta traz o título do setor e os produtos logo abaixo
- [ ] Sem setor, todos os setores aparecem separados, cada um com seu título
- [ ] A previsão por período usa o mesmo formato para todos os períodos
- [ ] O valor descartado é apresentado por setor e o total geral é igual à soma dos setores
- [ ] A resposta a um áudio tem o mesmo formato da resposta ao texto
- [ ] A funcionalidade foi testada sem erros (casos M1.1 a M1.11 do Guia de Testes)
- [ ] O resultado foi validado pelo Product Owner

---

## M2 — Tratamento de erros
> *O bot não fica preso quando algo falha e avisa de forma clara quando não consegue atender a pergunta.*

**Previsto em:** `bot/telegram_bot.py` (texto e voz), `ia/message.py`, `main.py` e as tools de `ia/tools/`.

### DoR
- [x] Comportamento esperado está claramente definido para cada tipo de falha (IA fora do ar, conexão com o Telegram, resposta longa, data inválida, setor inexistente, período sem histórico e arquivo de dados ausente)
- [x] Está definido o limite de uma mensagem do Telegram (4096 caracteres) e que a resposta maior é enviada em mais de uma mensagem
- [x] Está definido que a mensagem "Processando..." é sempre substituída pela resposta ou por um aviso
- [x] Cenários de teste estão mapeados no Guia de Testes (casos M2.1 a M2.9)

### DoD
- [ ] Falha ao processar texto ou voz substitui a mensagem "Processando..." por um aviso amigável
- [ ] A queda de conexão com o Telegram não derruba o bot, que volta a responder sem ser reiniciado
- [ ] Uma mesma mensagem não é respondida duas vezes
- [ ] Resposta acima do limite do Telegram é enviada em partes, sem o erro `MESSAGE_TOO_LONG` e sem cortar um item no meio
- [ ] Falha da IA (modelo indisponível ou saída inválida) gera aviso amigável, e o bot volta a funcionar quando a IA volta
- [ ] Data inválida, setor inexistente e data sem registros recebem uma resposta clara, sem inventar dados
- [ ] Período sem histórico (ex.: madrugada) informa qual período foi usado no cálculo
- [ ] Arquivo de dados ausente é apontado na inicialização, com o nome do arquivo
- [ ] Todas as tools tratam as próprias falhas e devolvem uma mensagem clara
- [ ] Os erros são registrados no terminal com a etapa em que ocorreram
- [ ] A funcionalidade foi testada sem erros (casos M2.1 a M2.9 do Guia de Testes)
- [ ] O resultado foi validado pelo Product Owner

---

## M3 — Limpeza do código
> *Remoção do que deixou de ser necessário, sem mudar o comportamento das funcionalidades já entregues.*

**Previsto em:** `ia/tools/producao_tool.py`, `ia/tools/desperdicio_tool.py`, `ia/message.py`, `ia/procedures/vendas_procedures.py`, `ia/services/producao_service.py` e novo `ia/services/desperdicio_service.py`.

### DoR
- [x] Está definido o que será removido: o parâmetro `tipo_pergunta` e a formatação separada de "quais" e "quantos", os logs de depuração e o código sem uso
- [x] Está definido que o cálculo do custo do descarte (custo dos ingredientes da receita × quantidade descartada) passa para um único *service*, e a tool apenas recebe os parâmetros e apresenta o resultado
- [x] Está definido que os valores das funcionalidades já entregues não podem mudar (verificação com os valores do Relatório de Testes da Sprint 2)
- [x] Cenários de teste estão mapeados no Guia de Testes (casos M3.1 a M3.6)

### DoD
- [ ] O parâmetro `tipo_pergunta` e a formatação separada de "quais" e "quantos" não existem mais nas tools
- [ ] A US01 não tem mais um caminho próprio: a pergunta "quais produtos devo produzir?" é respondida como a US02
- [ ] Os logs de depuração foram removidos; o terminal mostra apenas erros e o tempo de processamento
- [ ] O cálculo do custo do descarte está em `services.desperdicio`, e a tool de desperdício não lê CSV diretamente
- [ ] Não há código sem uso nem comentários desatualizados nos módulos alterados
- [ ] Os valores de descarte e de previsão de produção continuam iguais aos do Relatório de Testes da Sprint 2
- [ ] Os casos das Sprints 1 e 2 foram reexecutados sem falhas
- [ ] A funcionalidade foi testada sem erros (casos M3.1 a M3.6 do Guia de Testes)
- [ ] O resultado foi validado pelo Product Owner

---

## M4 — Correções da matéria-prima (US10)
> *Matéria-prima para o dia seguinte com quantidade e unidade corretas e resposta mais enxuta.*

**Previsto em:** `services.materia_prima` (cálculo compartilhado com a US11), `procedures.ingredientes.formatacao_pre_calculo` e `tool_previsao_quantidade_mp`.

### DoR
- [x] Está definido que a quantidade de cada ingrediente é a previsão do produto × a quantidade do ingrediente na receita
- [x] Está definido que a unidade de medida de cada ingrediente vem do cadastro (kg, L ou un) e é exibida em g ou mL quando a quantidade é menor que 1
- [x] Está definido que cada produto aparece uma única vez, com seus ingredientes listados logo abaixo
- [x] Está definido que a resposta não mostra a sobra em estoque (que passa a ser consultada na US11) e que o ingrediente com estoque insuficiente continua sinalizado
- [x] Cenários de teste estão mapeados no Guia de Testes (casos M4.1 a M4.7)

### DoD
- [ ] A quantidade de cada ingrediente é igual à previsão do produto × a quantidade na receita, inclusive para ingredientes fracionados (verificação cruzada com a US02)
- [ ] Cada quantidade vem acompanhada da unidade de medida correta, sem a palavra "unidades" no lugar da unidade
- [ ] Cada produto aparece uma única vez, com seus ingredientes logo abaixo
- [ ] A resposta não mostra a sobra em estoque
- [ ] O ingrediente com estoque insuficiente é sinalizado, com o necessário e o disponível
- [ ] Produto sem receita cadastrada é informado, sem inventar consumo
- [ ] A pergunta sobre uma matéria-prima específica soma o consumo de todos os produtos que a usam
- [ ] A funcionalidade foi testada sem erros (casos M4.1 a M4.7 do Guia de Testes)
- [ ] O resultado foi validado pelo líder ou responsável
