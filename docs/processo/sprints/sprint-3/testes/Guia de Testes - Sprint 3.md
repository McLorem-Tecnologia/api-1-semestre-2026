# Guia de Testes — Sprint 3

Este guia descreve os cenários de aceitação de matéria-prima e do menu do TeleBot. Os resultados e as evidências da execução estão no [Relatório de Testes da Sprint 3](./Relatório%20de%20Testes%20-%20Sprint%203.md). Os cenários 11.1 a 13.2 foram executados localmente; o envio ao Telegram ao vivo e o áudio físico não foram executados.

## Execução automatizada

No ambiente virtual do backend:

```powershell
python backend/testes/automatizar_testes_sprint3_mp.py
python backend/testes/validar_resposta_integrada_mp.py --captured
```

A primeira suíte valida a lógica das tools com dados controlados e os handlers do menu. O validador `--captured` compara uma resposta local registrada da MIA com a saída integral da tool.

## US-11 — Sobras de matéria-prima

| Caso | Condição ou pergunta | Resultado esperado |
| --- | --- | --- |
| 11.1 | Perguntar quais matérias-primas estão disponíveis para transferir | Listar as sobras por setor após reservar a necessidade prevista, com ingrediente, quantidade e unidade. |
| 11.2 | Aplicar filtro de setor de origem | Considerar apenas sobras do setor informado como origem. |
| 11.3 | Estoque sem déficit compatível | Não recomendar transferência e preservar a informação sobre sobras existentes. |
| 11.4 | Data sem histórico compatível | Informar que não foi possível calcular a necessidade por falta de histórico. |
| 11.5 | Produto previsto sem receita | Sinalizar o produto e informar que a análise pode estar incompleta, sem inventar consumo. |

## US-12 — Recomendar transferência entre setores

| Caso | Condição | Resultado esperado |
| --- | --- | --- |
| 12.1 | A sobra da origem cobre o déficit do destino para o mesmo ingrediente | Informar ingrediente, unidade, quantidade, origem, destino e falta residual zero. |
| 12.2 | A sobra da origem cobre apenas parte do déficit | Limitar a recomendação à sobra disponível e informar o déficit restante. |
| 12.3 | Não existe déficit compatível com as sobras | Informar que nenhuma transferência foi recomendada. |
| 12.4 | Informar um setor de origem | Não usar sobras de outros setores como fonte. |
| 12.5 | Informar data relativa e data explícita | Resolver e identificar o período considerado. |
| 12.6 | Conferir o estoque antes e depois da consulta | Manter os dados de estoque inalterados e a resposta dentro do limite do Telegram. |

## Menu de ajuda do TeleBot

| Caso | Ação | Resultado esperado |
| --- | --- | --- |
| 13.1 | Enviar `/ajuda` ou `/help` | Abrir o menu inline com Produção, Matéria-prima, Descarte, Produtos e Vendas. |
| 13.2 | Escolher uma categoria e uma pergunta de exemplo | Executar a pergunta pelo mesmo processador da MIA e apresentar navegação de retorno. |

## Limites registrados

Os handlers e a navegação foram exercitados com um bot falso. A integração com uma conversa real do Telegram e a gravação/transcrição de áudio não fazem parte dos resultados desta rodada. Consulte os limites e as evidências completas no relatório.
