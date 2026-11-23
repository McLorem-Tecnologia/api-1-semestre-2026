# Relatório de Testes — Sprint 3

Este relatório registra a nova execução das US-11 e US-12 após as mudanças na análise de necessidade, disponibilidade e transferência de matéria-prima. Os resultados abaixo refletem 13 testes automatizados do menu e das ferramentas, além de uma consulta integrada pelo fluxo local da MIA. A integração com o Telegram ao vivo e o teste de áudio físico não foram executados.

## Identificação da execução

| Item | Valor |
| --- | --- |
| Data dos testes | 22/11/2026 |
| Ambiente e versão do Python | Windows local · Python 3.13.6 |
| Modelo | Ollama `gemma4:e2b` para a consulta integrada · tools com testes automatizados |
| Dados de matéria-prima e vendas | CSVs em `backend/dados/` |
| Responsável | Execução automatizada local |

## Resultado geral

| Verificações | Executadas | Aprovadas | Reprovadas | Bloqueadas |
| ---: | ---: | ---: | ---: | ---: |
| 13 | 13 | 13 | 0 | 0 |

## Escopo

- **US-11:** identificar matérias-primas disponíveis para transferência, considerando o estoque acima da necessidade prevista por setor.
- **US-12:** recomendar transferências de matérias-primas para cobrir déficits, preservando a necessidade do setor de origem.
- As recomendações são informativas e não alteram os estoques.

## Casos de teste

| Caso | User Story | Entrada/condição | Resultado esperado | Resultado observado | Status | Evidência/observações |
| --- | --- | --- | --- | --- | :---: | --- |
| 11.1 | US-11 | Consultar matérias-primas disponíveis para transferir | Lista ingredientes com sobra positiva, unidade, quantidade e setor de origem após descontar a necessidade prevista | A MIA local listou as sobras por setor para 23/11/2026 e informou que não havia déficit compatível; portanto, não recomendou transferência. | ✅ | [resposta completa](#evidencia-111) |
| 11.2 | US-11 | Consultar com setor de origem Padaria | Considera somente sobras da Padaria como fonte | Aprovado: filtro de origem considerou somente sobras da Padaria. | ✅ | [teste automatizado](#execucao-automatizada) |
| 11.3 | US-11 | Estoque igual ou inferior à necessidade prevista em todos os setores | Informa que não há déficit compatível e não recomenda transferência; mantém a lista de sobras | Aprovado: no cenário controlado não houve déficit; nenhuma transferência foi recomendada e as sobras disponíveis foram mantidas na resposta. | ✅ | [teste automatizado](#execucao-automatizada) |
| 11.4 | US-11 | Data sem histórico compatível | Informa que não há histórico para calcular a necessidade | Aprovado: histórico vazio retornou mensagem clara de ausência de dados. | ✅ | [teste automatizado](#execucao-automatizada) |
| 11.5 | US-11 | Produto previsto sem receita cadastrada | Identifica o produto sem receita e sinaliza que a análise pode estar incompleta, sem inventar consumo | Aprovado: o produto sem receita foi informado e a análise sinalizada como incompleta. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.1 | US-12 | Um setor tem sobra e outro tem déficit do mesmo ingrediente | Recomenda a transferência, informando quantidade, unidade, origem, destino e justificativa | Aprovado: cenário controlado recomendou 17,00 kg de Farinha da Padaria para a Cozinha. | ✅ | [resposta completa](#evidencia-121) |
| 12.2 | US-12 | Sobra menor que o déficit do destino | Recomenda no máximo a sobra disponível e informa o déficit restante | Aprovado: cenário controlado recomendou 8,00 kg e informou falta residual de 9,00 kg. | ✅ | [resposta completa](#evidencia-122) |
| 12.3 | US-12 | Não há déficit ou sobra compatível | Informa que nenhuma transferência foi recomendada | Aprovado: cenário sem déficit compatível não gerou recomendação. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.4 | US-12 | Aplicar filtro de setor de origem | Não usa sobras de outros setores como fonte | Aprovado: filtro de origem impediu o uso de sobras dos demais setores. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.5 | US-12 | Consultar com data relativa e data explícita | Resolve a data e identifica o período usado na análise | Aprovado: data explícita e referência relativa foram convertidas para dd/mm/aaaa. | ✅ | [teste automatizado](#execucao-automatizada) |
| 12.6 | US-12 | Verificação antes/depois da consulta | Os dados de estoque permanecem inalterados | Aprovado: o hash do ingredientes.csv permaneceu igual antes e depois da consulta; a resposta ficou abaixo do limite do Telegram. | ✅ | [teste automatizado](#execucao-automatizada) |
| 13.1 | Menu | Enviar `/ajuda` ou `/help` | Abre menu inline com Produção, Matéria-prima, Descarte, Produtos, Vendas e áudio | Aprovado: teste automatizado confirmou comandos e categorias. | ✅ | [teste automatizado](#execucao-automatizada) |
| 13.2 | Menu | Selecionar categoria e pergunta de exemplo | Executa a pergunta pelo fluxo MIA e mostra navegação de retorno | Aprovado: teste automatizado confirmou envio ao processador e teclado de retorno. | ✅ | [teste automatizado](#execucao-automatizada) |

## Registro de falhas

| ID | Caso relacionado | Descrição | Severidade | Status | Evidência |
| --- | --- | --- | :---: | :---: | --- |

## Reteste de correções

| ID da falha | Caso de reteste | Resultado observado | Status | Evidência |
| --- | --- | --- | :---: | --- |


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


## Limites da execução

Execução local: sem Telegram ao vivo e sem áudio físico. A resposta integrada usou dados reais do projeto e modelo local; os demais cenários automatizados usaram fixtures controladas. Os estoques de Farinha de Trigo (649000,47 Kg) e Queijo Mussarela (47000,25 Kg) da Padaria no CSV precisam ser conferidos com a fonte antes de uso operacional.
