# Padrão de Commits

Os commits devem seguir o padrão **Padrão de Commits** para manter a consistência e a clareza no repositório.

## Formato do Commit:
```
<tipo> (MT-XX): <descrição em tom de ação direta>
<informações adicionais (opcional)>
```
> **Nota:** O `(MT-XX)` deve ser substituído pelo código da tarefa correspondente no Jira (ex: MT-121).

## Tipos de Commit:
- **docs** – Mudanças na documentação (como Readme). Não inclui alterações em código.
- **feat** – Inclui um novo recurso.
- **fix** – Soluciona um problema (bug fix).
- **refactor** – Refatorações que não alteram funcionalidades, como melhoria de performance ou ajustes no código sem mudar o comportamento.
- **style** – Alterações de formatação de código (ex: semicolons, trailing spaces, lint). Não inclui alterações em código.
- **test** – Alterações em testes (criação, modificação ou remoção de testes unitários).
- **chore** – Atualizações de tarefas administrativas ou configuração, como adição de pacotes no gitignore.

## Exemplos:
- **feat (MT-121)**: Adiciona função para calcular a média de vendas
- **fix (MT-45)**: Corrige bug de cálculo na função de média
- **refactor (MT-88)**: Refatora lógica de inicialização da API
- **docs (MT-12)**: Documenta o cronograma de sprints no README.md
- **style (MT-09)**: Remove espaços em branco desnecessários no utils.py
- **chore (MT-05)**: Adiciona biblioteca pandas ao .gitignore