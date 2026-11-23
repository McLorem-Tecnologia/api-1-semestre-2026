# Relatório de Testes — Sprint 3

Este relatório registra os testes das US-11 e US-12 e do menu de ajuda após as atualizações das ferramentas de matéria-prima.

## Identificação da execução

| Item | Valor |
| --- | --- |
| Data dos testes | 23/11/2026 |
| Ambiente e versão do Python | Windows local · Python 3.13.6 |
| Modelo | Ollama `gemma4:e2b` na consulta integrada da MIA |
| Dados de matéria-prima e vendas | CSVs do projeto em `backend/dados/` |
| Fluxo integrado | Processador local utilizado pelo TeleBot |

## Resultado geral

| Verificações | Executadas | Aprovadas | Reprovadas | Bloqueadas |
| ---: | ---: | ---: | ---: | ---: |
| 13 | 13 | 13 | 0 | 0 |

## Escopo

- **US-11:** identificar matérias-primas disponíveis para transferência, considerando o estoque acima da necessidade prevista por setor.
- **US-12:** recomendar transferências para cobrir déficits, preservando a necessidade do setor de origem.
- As recomendações são informativas e não alteram os estoques.
- **Menu de ajuda:** apresentar categorias e permitir navegação pelas perguntas de exemplo.

## Casos de teste

| Caso | User Story | Entrada/condição | Resultado esperado | Resultado observado | Status | Evidência |
| --- | --- | --- | --- | --- | :---: | --- |
| 11.1 | US-11 | Consultar matérias-primas disponíveis para transferir | Lista sobras por ingrediente, unidade, quantidade e setor após descontar a necessidade prevista | A MIA listou 69 itens de sobra por setor para 24/11/2026 e não recomendou transferência sem falta compatível. | ✅ | [resposta completa](#evidencia-111) |
| 11.2 | US-11 | Consultar com setor de origem Padaria | Considera somente sobras da Padaria como fonte | O filtro de origem foi aplicado e não utilizou sobras dos demais setores. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 11.3 | US-11 | Estoque igual ou inferior à necessidade prevista | Informa ausência de transferência compatível e preserva a lista de sobras | As sobras foram mantidas na resposta e nenhuma transferência foi recomendada sem déficit compatível. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 11.4 | US-11 | Data sem histórico compatível | Informa que não há histórico para calcular a necessidade | O cenário sem histórico retornou mensagem clara de ausência de dados. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 11.5 | US-11 | Produto previsto sem receita cadastrada | Identifica o produto e sinaliza análise incompleta, sem inventar consumo | O produto sem receita foi identificado e a análise foi sinalizada como incompleta. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 12.1 | US-12 | Um setor tem sobra e outro tem déficit do mesmo ingrediente | Recomenda transferência com quantidade, unidade, origem, destino e justificativa | Foram recomendados 17,00 kg de Farinha da Padaria para a Cozinha; a falta residual ficou em 0,00 kg. | ✅ | [resposta completa](#evidencia-121) |
| 12.2 | US-12 | Sobra menor que o déficit do destino | Limita a transferência à sobra disponível e informa o déficit restante | Foram recomendados 8,00 kg de Farinha; a falta residual ficou em 9,00 kg. | ✅ | [resposta completa](#evidencia-122) |
| 12.3 | US-12 | Não há déficit ou sobra compatível | Informa que nenhuma transferência foi recomendada | Nenhuma transferência foi recomendada sem falta compatível. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 12.4 | US-12 | Aplicar filtro de setor de origem | Não usa sobras de outros setores como fonte | O filtro limitou a origem ao setor informado. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 12.5 | US-12 | Consultar com data relativa e data explícita | Resolve a data e identifica o período da análise | Datas explícitas e relativas foram resolvidas no formato dd/mm/aaaa. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 12.6 | US-12 | Verificação antes/depois da consulta | Mantém os dados de estoque inalterados e respeita o limite da mensagem | O arquivo de estoque permaneceu inalterado e a resposta ficou abaixo do limite do Telegram. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 13.1 | Menu | Enviar `/ajuda` ou `/help` | Abre menu inline com Produção, Matéria-prima, Descarte, Produtos, Vendas e áudio | Os comandos /ajuda e /help abriram o menu com as categorias previstas. | ✅ | [verificações executadas](#verificacoes-executadas) |
| 13.2 | Menu | Selecionar categoria e pergunta de exemplo | Encaminha a pergunta à MIA e oferece navegação de retorno | A pergunta de exemplo foi encaminhada à MIA e o menu de navegação foi reapresentado. | ✅ | [verificações executadas](#verificacoes-executadas) |

## Registro de falhas

Não houve falhas nas verificações concluídas.

## Respostas completas

<details>
<summary><b>11.1</b> — Resposta da MIA a “Quais matérias-primas estão disponíveis para transferir para outros setores?”</summary>

<a id="evidencia-111"></a>

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

### Verificações executadas <a id="verificacoes-executadas"></a>

As 13 verificações previstas foram executadas e aprovadas. A cobertura inclui as respostas integradas das US-11 e US-12, cenários de estoque controlados, histórico ausente, produto sem receita, filtro de origem, transferência total e parcial, preservação do arquivo e navegação do menu.

## Limites da execução

A execução ocorreu no ambiente local. O handler do Telegram foi exercitado localmente, sem conexão com a API do Telegram.
