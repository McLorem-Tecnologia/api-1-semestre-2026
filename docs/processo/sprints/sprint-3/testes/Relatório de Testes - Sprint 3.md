# Relatório de Testes — Sprint 3

Este documento registra a execução manual dos testes da MIA na Sprint 3: cada linha da tabela de registro mostra a mensagem enviada no Telegram e o resultado obtido. As evidências completas (respostas longas do bot) estão no final do documento.

## Identificação da execução

| Item              | Valor |
| ----------------- | ----- |
| Datas de execução |       |
| Executado por     |       |
| Modelo            |       |
| Python            |       |

## Resumo

| Total | ✅ Aprovados | ⚠️ Com ressalva | ❌ Reprovados |
| :---: | :---------: | :-------------: | :----------: |
|       |             |                 |              |

---

## Pré-requisitos antes de começar

- [ ] Ollama aberto, com o modelo `ollama pull gemma4:e2b` baixado
- [ ] Arquivo `.env` configurado em `backend/src/.env` com `TELEGRAM_BOT_KEY` válido
- [ ] `python main.py` rodando sem erros no terminal (verifique se aparece "[IA] Modelo carregado e pronto para responder.")
- [ ] Bot respondendo a `/start` no Telegram
- [ ] `dados/ingredientes.csv` com o estoque atual de cada ingrediente por setor e `dados/receitas.csv` com a receita de cada produto (definição das US10 e US11)
- [ ] `dados/transferencias.csv` com as colunas `Data`, `SKU`, `Setor Origem`, `Setor Destino` e `Motivo`, com ao menos um produto com mais de uma transferência e ao menos um produto sem transferência (definição da US12)
- [ ] Solução de transcrição de áudio instalada e funcionando localmente
- [ ] Celular com Telegram para gravar as mensagens de voz
- [ ] Acesso à pasta `dados/` para renomear um arquivo temporariamente (caso M2.7)

---

## Roteamento e comportamento social (`agentes.py`)

Continuação dos casos 0.2.1 a 0.2.6 das Sprints 1 e 2.

| ID    | Mensagem para enviar                                | Resultado esperado                                                                                                            |
| ----- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 0.2.7 | "Quais ingredientes posso passar para outro setor?" | O Agente Roteador identifica `PRODUCAO` (e não `PRODUTOS`) e aciona a tool de matéria-prima disponível para transferir (US11) |
| 0.2.8 | "Por que a coxinha foi transferida de setor?"       | O Agente Roteador identifica `PRODUCAO` e aciona a tool de transferências (US12)                                              |

---

## Formatação da resposta

Continuação dos casos 0.3.1 a 0.3.7 das Sprints 1 e 2.

| ID     | O que verificar               | Resultado esperado                                                                       |
| ------ | ----------------------------- | ---------------------------------------------------------------------------------------- |
| 0.3.8  | Resposta com mais de um setor | Cada setor aparece com título próprio, e os produtos ficam logo abaixo, listados com `•` |
| 0.3.9  | Resposta com um único setor   | Também traz o título do setor, com a quantidade e a unidade de medida de cada produto    |
| 0.3.10 | Quantidades de produto        | Sempre acompanhadas da unidade de medida do cadastro (Kg, Un, Porção ou L)               |

---

## Casos com resultado esperado atualizado

Reexecute todos os casos das Sprints 1 e 2. Os casos abaixo mudaram de resultado esperado por causa das melhorias da Sprint 3; os demais continuam como estavam.

| Caso                               | Novo resultado esperado                                                                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0.3.3 (Sprint 1)                   | Cada setor aparece com título próprio, como no caso 0.3.8                                                                                        |
| 1.1 a 1.4 (Sprint 1)               | Produto, quantidade e unidade de medida, separados por setor, como nos casos 2.1 a 2.3. A resposta a "quais" deixa de ser uma lista só com nomes |
| 2.1 a 2.3 (Sprint 1)               | Produtos separados por setor, com quantidade e unidade. No 2.2, só a coxinha, sob o setor Padaria; no 2.3, só a Padaria, com o título do setor   |
| 3.1 a 3.5 (Sprint 1)               | Total produzido, vendas e descarte de cada produto, separados por setor, inclusive quando a pergunta cita um único setor                         |
| 4.1 a 4.3 (Sprint 1)               | Meta com a quantidade de cada produto, separada por setor                                                                                        |
| 5.2 e 5.7 (Sprint 2)               | 5.2: manhã, tarde e noite no mesmo formato. 5.7: a MIA informa o período usado no cálculo (ver caso M2.5)                                        |
| 6.1, 7.3 e 9.9 (Sprint 2)          | Valor em R$ de cada setor e total geral igual à soma dos setores (ver caso M1.9)                                                                 |
| 9.1 (Sprint 2)                     | Igual ao caso 2.1, com as quantidades (e não mais uma lista só com nomes)                                                                        |
| 10.1, 10.2, 10.4 e 10.6 (Sprint 2) | Matéria-prima como descrito nos casos M4.1 a M4.7                                                                                                |

---

## US11 — Matérias-primas disponíveis para transferir (líder)

*Os nomes das matérias-primas e dos setores são exemplos: ajuste aos nomes reais da planilha.*

| ID   | Mensagem para enviar                                                                                                                           | Resultado esperado                                                                                                                                            |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 11.1 | "Quais matérias-primas estão disponíveis para transferir para outros setores?"                                                                 | Matérias-primas com sobra (estoque menos a necessidade de amanhã) de todos os setores, separadas por setor, com a quantidade disponível e a unidade de medida |
| 11.2 | "O que tenho sobrando de ingredientes na padaria para transferir?"                                                                             | Só as matérias-primas com sobra da Padaria, sob o título do setor; fraseado diferente do caso 11.1                                                            |
| 11.3 | "Quais ingredientes posso passar para outro setor na cozinha?"                                                                                 | Só a Cozinha/Rotisseria; sem data, a necessidade considerada é a de amanhã                                                                                    |
| 11.4 | "O que sobra de ingredientes na padaira para transferir?" (erro de digitação proposital)                                                       | `normalizar_setor` deve corrigir para "Padaria" mesmo com o erro                                                                                              |
| 11.5 | "Quanto de farinha de trigo está disponível para transferir?"                                                                                  | Filtra uma matéria-prima e mostra a quantidade disponível em cada setor que a possui                                                                          |
| 11.6 | Verificação cruzada: para um ingrediente do caso 11.2, calcular à mão o estoque (`ingredientes.csv`) menos a necessidade de amanhã (caso M4.1) | O valor calculado é igual ao informado pela MIA                                                                                                               |
| 11.7 | Setor ou ingrediente cujo estoque é todo necessário no dia seguinte                                                                            | Não aparece como disponível; se nenhum item tiver sobra, a MIA informa que não há matéria-prima disponível para transferir                                    |
| 11.8 | Áudio dizendo: "Quais matérias-primas posso transferir para outros setores?"                                                                   | Transcreve e responde igual ao caso 11.1                                                                                                                      |

---

## US12 — Motivo da transferência de um produto (gerente)

*Os produtos acima são exemplos: ajuste aos produtos que constam em `transferencias.csv`.*

| ID   | Mensagem para enviar                                                                                 | Resultado esperado                                                                                                        |
| ---- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 12.1 | "Por que a coxinha está sendo transferida de setor?"                                                 | Motivo registrado da transferência, com setor de origem, setor de destino e data                                          |
| 12.2 | "Qual o motivo da transferência do pudim?"                                                           | Mesmo resultado, fraseado diferente: verifica se o Agente Roteador entende variações de pergunta                          |
| 12.3 | "Por que o PÃO FRANCÊS foi transferido?" (maiúsculas proposital)                                     | O nome do produto é reconhecido independentemente de maiúsculas e minúsculas                                              |
| 12.4 | "Por que a lasanha foi transferida?" (produto sem transferência registrada)                          | A MIA informa que não encontrou registro de transferência para o produto, sem inventar um motivo                          |
| 12.5 | "Por que o produto xyz foi transferido?" (produto inexistente)                                       | A MIA informa que não encontrou o produto, sem inventar um motivo                                                         |
| 12.6 | Produto com mais de uma transferência registrada                                                     | Todas as transferências são apresentadas, da mais recente para a mais antiga, cada uma com data, origem, destino e motivo |
| 12.7 | Verificação cruzada: comparar a resposta do caso 12.1 com a linha do produto em `transferencias.csv` | Motivo, setores e data são exatamente os do registro                                                                      |
| 12.8 | Áudio dizendo: "Por que a coxinha está sendo transferida de setor?"                                  | Transcreve e responde igual ao caso 12.1                                                                                  |

---

## M1 — Resposta padronizada por setor

| ID    | Mensagem para enviar                                            | Resultado esperado                                                                                               |
| ----- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| M1.1  | "Quais produtos devo produzir hoje?"                            | Produtos de todos os setores, separados por setor, cada um com a quantidade e a unidade de medida                |
| M1.2  | "Quantos produtos devo produzir hoje?"                          | Exatamente a mesma resposta do caso M1.1: as perguntas "quais" e "quantos" não mudam o formato                   |
| M1.3  | "Quais produtos devo produzir hoje na padaria?"                 | Título "Padaria" e os 10 produtos do setor, cada um com a quantidade e a unidade de medida (e não só os nomes)   |
| M1.4  | "Quanto de coxinha devo fazer amanhã?"                          | Somente a coxinha, com a quantidade e a unidade de medida, sob o título do setor Padaria                         |
| M1.5  | "O que deveria ter sido produzido ontem na padaria?"            | Meta da Padaria, com a quantidade de cada produto, sob o título do setor                                         |
| M1.6  | "O que foi produzido ontem?"                                    | Total produzido, vendas e descarte de cada produto, separados por setor, sem precisar pedir "separe por setores" |
| M1.7  | "O que devo produzir de manhã?"                                 | Produtos de todos os setores no período da manhã, separados por setor, com quantidade e unidade de medida        |
| M1.8  | "O que produzir em cada período do dia na padaria?"             | Manhã, tarde e noite no mesmo formato, em ordem cronológica, sob o título do setor Padaria                       |
| M1.9  | "Quantos reais foram descartados no dia 01/10/2026?"            | Valor em R$ de cada setor e total geral igual à soma dos setores (R$ 482,01, como no caso 6.5 da Sprint 2)       |
| M1.10 | "Quantos reais foram descartados no dia 01/10/2026 na padaria?" | Valor em R$ só da Padaria, sob o título do setor (R$ 97,69, como no caso 6.2 da Sprint 2)                        |
| M1.11 | Áudio dizendo: "O que devo produzir hoje na padaria?"           | Transcreve e responde igual ao caso M1.3                                                                         |

---

## M2 — Tratamento de erros

| ID   | Mensagem para enviar                                                   | Resultado esperado                                                                                                                           |
| ---- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| M2.1 | Fechar o Ollama e enviar "O que devo produzir hoje?"                   | A mensagem "Processando sua solicitação..." é substituída por um aviso amigável de falha; ao abrir o Ollama de novo, o bot volta a responder |
| M2.2 | "Quanta matéria-prima preciso para amanhã?" (sem informar o setor)     | Resposta enviada em mais de uma mensagem quando passa de 4096 caracteres, sem o erro `MESSAGE_TOO_LONG` e sem cortar um item no meio         |
| M2.3 | Desconectar a internet por alguns segundos durante o uso e reconectar  | O bot volta a responder sem ser reiniciado, e nenhuma mensagem é respondida duas vezes                                                       |
| M2.4 | "Quanto devo produzir em 31/02/2026?" (data inválida)                  | A MIA avisa que não entendeu a data e pede para informá-la de novo, sem mensagem técnica                                                     |
| M2.5 | "O que devo produzir de madrugada na padaria?" (período sem histórico) | A MIA informa que não há vendas na madrugada e que usou o período da noite, o mais próximo                                                   |
| M2.6 | "O que devo produzir hoje na floricultura?" (setor inexistente)        | A MIA informa que não encontrou o setor, sem inventar produtos                                                                               |
| M2.7 | Renomear temporariamente um CSV da pasta `dados/` e iniciar o bot      | O terminal informa qual arquivo não foi encontrado. Depois do teste, devolver o nome original ao arquivo                                     |
| M2.8 | "Quantos reais foram descartados em 01/01/2020?" (data sem registros)  | A MIA informa que não há registros de descarte nessa data                                                                                    |
| M2.9 | Áudio dizendo: "Quanta matéria-prima preciso para amanhã?"             | Resposta em partes, igual ao caso M2.2                                                                                                       |

---

## M3 — Limpeza do código

| ID   | Mensagem para enviar                                                   | Resultado esperado                                                                                                                                                                                                                |
| ---- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M3.1 | Verificação no código: buscar `tipo_pergunta` na pasta `ia/`           | Nenhuma ocorrência; as tools de produção usam uma única forma de formatar a lista de produtos                                                                                                                                     |
| M3.2 | Verificação no terminal durante uma pergunta                           | Sem logs de depuração (`[DEBUG]` e histórico do DSPy); aparecem só os erros e o tempo de processamento                                                                                                                            |
| M3.3 | "Quantos reais foram descartados em 07/04/2026 na empresa toda?"       | Total de R$ 543,59, igual ao do caso 7.1 da Sprint 2, agora calculado em `services.desperdicio`                                                                                                                                   |
| M3.4 | "Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?" | R$ 806,36, igual ao do caso 6.3 da Sprint 2                                                                                                                                                                                       |
| M3.5 | "Qual foi o custo total de desperdício em setembro?"                   | R$ 17.094,53, igual ao do caso 7.2 da Sprint 2                                                                                                                                                                                    |
| M3.6 | "Quantos produtos devo produzir no dia 26/10/2026 na padaria?"         | Mesmas quantidades do caso 9.2 da Sprint 2 (Pão Francês 134, Pão de queijo 20, Croissant 9, Coxinha 172, Enroladinho 132, Bolo de chocolate 9, Torta de limão 5, Pudim 43, Brigadeiro 5 e Beijinho 5), agora no formato por setor |

---

## M4 — Correções da matéria-prima (US10)

| ID   | Mensagem para enviar                                                                                               | Resultado esperado                                                                                                                                                                    |
| ---- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M4.1 | "Quanta matéria-prima preciso deixar preparada para amanhã na padaria?"                                            | Cada produto da Padaria aparece uma única vez, com os ingredientes logo abaixo, cada um com a quantidade e a unidade de medida correta (kg ou g, L ou mL, un), sem a sobra em estoque |
| M4.2 | Mesma pergunta do caso M4.1, olhando os ingredientes de quantidade pequena (ex.: Batata e Óleo de Soja da Coxinha) | Quantidades fracionadas calculadas corretamente e exibidas em g ou mL, sem arredondar para zero                                                                                       |
| M4.3 | Verificação cruzada: comparar com "Quantas unidades devo produzir amanhã na padaria?"                              | Quantidade de cada ingrediente = quantidade prevista do produto × quantidade do ingrediente na receita, inclusive para ingredientes com fração (ex.: 0,1 kg por unidade)              |
| M4.4 | "O que preciso separar de ingredientes para amanhã na cozinha?"                                                    | Mesma estrutura do caso M4.1 para a Cozinha/Rotisseria, sem a sobra em estoque                                                                                                        |
| M4.5 | "Quanto de farinha preciso para amanhã?"                                                                           | Soma do consumo de todos os produtos que usam farinha, com a unidade de medida correta                                                                                                |
| M4.6 | Produto da previsão sem receita cadastrada                                                                         | A MIA informa quais produtos ficaram sem receita, sem inventar o consumo                                                                                                              |
| M4.7 | Ingrediente cujo estoque não cobre a necessidade (ajuste ao dado real da planilha)                                 | O ingrediente é sinalizado como insuficiente, com a quantidade necessária e a disponível, cada uma com a unidade de medida                                                            |

---

## Tabela de Registro dos Testes

| Caso   | Mensagem enviada                                                                                                                               | Resultado obtido | Status | Observações |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | :----: | ----------- |
| 0.2.7  | Quais ingredientes posso passar para outro setor?                                                                                              |                  |        |             |
| 0.2.8  | Por que a coxinha foi transferida de setor?                                                                                                    |                  |        |             |
| 0.3.8  | Resposta com mais de um setor                                                                                                                  |                  |        |             |
| 0.3.9  | Resposta com um único setor                                                                                                                    |                  |        |             |
| 0.3.10 | Quantidades de produto                                                                                                                         |                  |        |             |
| 11.1   | Quais matérias-primas estão disponíveis para transferir para outros setores?                                                                   |                  |        |             |
| 11.2   | O que tenho sobrando de ingredientes na padaria para transferir?                                                                               |                  |        |             |
| 11.3   | Quais ingredientes posso passar para outro setor na cozinha?                                                                                   |                  |        |             |
| 11.4   | O que sobra de ingredientes na padaira para transferir? (erro de digitação proposital)                                                         |                  |        |             |
| 11.5   | Quanto de farinha de trigo está disponível para transferir?                                                                                    |                  |        |             |
| 11.6   | Verificação cruzada: para um ingrediente do caso 11.2, calcular à mão o estoque (`ingredientes.csv`) menos a necessidade de amanhã (caso M4.1) |                  |        |             |
| 11.7   | Setor ou ingrediente cujo estoque é todo necessário no dia seguinte                                                                            |                  |        |             |
| 11.8   | Áudio dizendo: Quais matérias-primas posso transferir para outros setores?                                                                     |                  |        |             |
| 12.1   | Por que a coxinha está sendo transferida de setor?                                                                                             |                  |        |             |
| 12.2   | Qual o motivo da transferência do pudim?                                                                                                       |                  |        |             |
| 12.3   | Por que o PÃO FRANCÊS foi transferido? (maiúsculas proposital)                                                                                 |                  |        |             |
| 12.4   | Por que a lasanha foi transferida? (produto sem transferência registrada)                                                                      |                  |        |             |
| 12.5   | Por que o produto xyz foi transferido? (produto inexistente)                                                                                   |                  |        |             |
| 12.6   | Produto com mais de uma transferência registrada                                                                                               |                  |        |             |
| 12.7   | Verificação cruzada: comparar a resposta do caso 12.1 com a linha do produto em `transferencias.csv`                                           |                  |        |             |
| 12.8   | Áudio dizendo: Por que a coxinha está sendo transferida de setor?                                                                              |                  |        |             |
| M1.1   | Quais produtos devo produzir hoje?                                                                                                             |                  |        |             |
| M1.2   | Quantos produtos devo produzir hoje?                                                                                                           |                  |        |             |
| M1.3   | Quais produtos devo produzir hoje na padaria?                                                                                                  |                  |        |             |
| M1.4   | Quanto de coxinha devo fazer amanhã?                                                                                                           |                  |        |             |
| M1.5   | O que deveria ter sido produzido ontem na padaria?                                                                                             |                  |        |             |
| M1.6   | O que foi produzido ontem?                                                                                                                     |                  |        |             |
| M1.7   | O que devo produzir de manhã?                                                                                                                  |                  |        |             |
| M1.8   | O que produzir em cada período do dia na padaria?                                                                                              |                  |        |             |
| M1.9   | Quantos reais foram descartados no dia 01/10/2026?                                                                                             |                  |        |             |
| M1.10  | Quantos reais foram descartados no dia 01/10/2026 na padaria?                                                                                  |                  |        |             |
| M1.11  | Áudio dizendo: O que devo produzir hoje na padaria?                                                                                            |                  |        |             |
| M2.1   | Fechar o Ollama e enviar O que devo produzir hoje?                                                                                             |                  |        |             |
| M2.2   | Quanta matéria-prima preciso para amanhã? (sem informar o setor)                                                                               |                  |        |             |
| M2.3   | Desconectar a internet por alguns segundos durante o uso e reconectar                                                                          |                  |        |             |
| M2.4   | Quanto devo produzir em 31/02/2026? (data inválida)                                                                                            |                  |        |             |
| M2.5   | O que devo produzir de madrugada na padaria? (período sem histórico)                                                                           |                  |        |             |
| M2.6   | O que devo produzir hoje na floricultura? (setor inexistente)                                                                                  |                  |        |             |
| M2.7   | Renomear temporariamente um CSV da pasta `dados/` e iniciar o bot                                                                              |                  |        |             |
| M2.8   | Quantos reais foram descartados em 01/01/2020? (data sem registros)                                                                            |                  |        |             |
| M2.9   | Áudio dizendo: Quanta matéria-prima preciso para amanhã?                                                                                       |                  |        |             |
| M3.1   | Verificação no código: buscar `tipo_pergunta` na pasta `ia/`                                                                                   |                  |        |             |
| M3.2   | Verificação no terminal durante uma pergunta                                                                                                   |                  |        |             |
| M3.3   | Quantos reais foram descartados em 07/04/2026 na empresa toda?                                                                                 |                  |        |             |
| M3.4   | Quanto perdemos com descarte da peixaria de 01/09/2026 a 15/09/2026?                                                                           |                  |        |             |
| M3.5   | Qual foi o custo total de desperdício em setembro?                                                                                             |                  |        |             |
| M3.6   | Quantos produtos devo produzir no dia 26/10/2026 na padaria?                                                                                   |                  |        |             |
| M4.1   | Quanta matéria-prima preciso deixar preparada para amanhã na padaria?                                                                          |                  |        |             |
| M4.2   | Mesma pergunta do caso M4.1, olhando os ingredientes de quantidade pequena (ex.: Batata e Óleo de Soja da Coxinha)                             |                  |        |             |
| M4.3   | Verificação cruzada: comparar com Quantas unidades devo produzir amanhã na padaria?                                                            |                  |        |             |
| M4.4   | O que preciso separar de ingredientes para amanhã na cozinha?                                                                                  |                  |        |             |
| M4.5   | Quanto de farinha preciso para amanhã?                                                                                                         |                  |        |             |
| M4.6   | Produto da previsão sem receita cadastrada                                                                                                     |                  |        |             |
| M4.7   | Ingrediente cujo estoque não cobre a necessidade (ajuste ao dado real da planilha)                                                             |                  |        |             |

---

## Evidências Completas

Respostas longas do bot (que não cabem na tabela) ficam guardadas aqui, uma por caso de teste, dentro de um bloco recolhível.

<!--
<details>
<summary><b>ID do caso</b> — "mensagem enviada"</summary>
<a id="evidencia-ID"></a>

```
resposta do bot
```

</details>
-->
