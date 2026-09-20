# Deploy 24/7 com Oracle Cloud e Gemini

Este documento registra o planejamento, as decisões técnicas, a configuração e os procedimentos relacionados à execução contínua do bot Telegram do projeto.

O projeto é um assistente de análise de dados para supermercados. Ele usa Python, Pandas, DSPy, Telegram e arquivos CSV para responder perguntas sobre vendas, produtos, regras, ingredientes e descartes.

> Este documento é específico para a preparação do deploy com Oracle Cloud e Gemini. O `README.md` principal não deve ser alterado para documentar este trabalho.

## Objetivo

Executar o bot continuamente em uma VM gratuita da Oracle Cloud, usando o plano Always Free, com:

- bot Telegram ativo 24 horas por dia;
- modelo Gemini acessado por API externa;
- dados CSV mantidos junto com a aplicação;
- inicialização automática após reinicialização da VM;
- reinício automático em caso de falha;
- credenciais fora do Git;
- logs consultáveis pelo `journalctl`;
- nenhuma porta HTTP pública necessária, pois o bot usa `infinity_polling`.

## Decisões do projeto

- Provedor de hospedagem: Oracle Cloud Infrastructure, plano Always Free.
- Sistema operacional planejado: Ubuntu Server.
- Provedor de IA inicial: Google AI Studio, usando um modelo Gemini Flash disponível na conta.
- Integração de IA: endpoint compatível com OpenAI configurado no DSPy.
- Transporte do bot: long polling do Telegram.
- Gerenciamento do processo: serviço `systemd`.
- Segredos: variáveis de ambiente ou arquivo de ambiente protegido na VM; nenhuma chave deve ser commitada.
- Documentação deste deploy: este arquivo `readme-gemini.md`.

## Estado atual

A implementação está sendo preparada em uma branch própria de deploy. Não fazer commit dessas alterações diretamente na `main`.

Checklist geral:

- [ ] Criar ou confirmar a branch de deploy.
- [ ] Revisar as alterações locais existentes antes do commit.
- [x] Configurar o DSPy para o Gemini externo.
- [ ] Remover instalação automática de pacotes durante a importação da configuração.
- [ ] Criar o arquivo de dependências.
- [ ] Tornar os caminhos dos CSVs independentes do diretório de execução.
- [ ] Testar o bot localmente com variáveis de ambiente.
- [ ] Criar a conta e a VM Always Free na Oracle Cloud.
- [ ] Instalar Python e preparar a virtualenv na VM.
- [ ] Copiar o projeto e os dados para a VM.
- [ ] Configurar o arquivo de ambiente protegido.
- [ ] Instalar e habilitar o serviço `systemd`.
- [ ] Validar reinício automático e recuperação após falha.
- [ ] Documentar os comandos reais usados e os resultados dos testes.

## Branch e versionamento

Antes de criar commits para este trabalho:

```powershell
git status --short --branch
git switch -c deploy-oracle-gemini
```

O nome da branch pode ser ajustado conforme a convenção do grupo. Antes do commit, conferir se não há chaves, tokens, arquivos `.env` ou alterações não relacionadas.

Arquivos de segredo devem estar no `.gitignore`, por exemplo:

```gitignore
.env
.env.*
!.env.example
```

O arquivo `.env.example` pode conter apenas nomes de variáveis e valores fictícios, nunca credenciais reais.

## Variáveis de ambiente

A aplicação recebe as credenciais e configurações por ambiente. Os nomes atualmente usados são:

```dotenv
TELEGRAM_BOT_FATEC1_KEY=coloque_o_token_do_bot
GEMINI_API_FATEC1_KEY=coloque_a_chave_do_google_ai_studio
GEMINI_MODEL=nome_do_modelo_flash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

`GEMINI_MODEL` e `GEMINI_BASE_URL` são opcionais: o código usa `gemini-2.5-flash` e o endpoint OpenAI-compatible padrão do Google quando não forem definidos. A chave do Telegram e a chave do Gemini nunca devem aparecer no código, nos commits, nos logs ou nesta documentação.

## Configuração do Gemini no DSPy

A configuração deverá:

1. Ler `GEMINI_API_FATEC1_KEY`, `GEMINI_MODEL` e `GEMINI_BASE_URL` do ambiente.
2. Usar inicialmente um modelo Gemini Flash disponível no Google AI Studio.
3. Remover as URLs locais do Ollama, incluindo referências a `http://localhost:11434`.
4. Manter o fluxo `ReAct` e as ferramentas atuais.
5. Validar se o function calling das ferramentas funciona corretamente com o modelo escolhido.
6. Desativar `dspy.inspect_history()` em produção para evitar exposição de dados e geração de logs desnecessários.
7. Definir timeouts e tratamento para falhas temporárias da API.

O modelo exato deve ser confirmado no Google AI Studio no momento da configuração, pois a disponibilidade, os nomes e os limites podem mudar.

## Preparação do projeto

### Dependências

Criar `requirements.txt` ou `pyproject.toml` com todas as dependências necessárias para execução. A instalação de pacotes não deve acontecer automaticamente dentro de `config.py` ou durante um import.

A instalação deverá ser explícita na máquina local e na VM, por exemplo:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Caminhos dos CSVs

Os procedimentos devem localizar os arquivos CSV a partir da raiz do projeto ou de um caminho configurável, e não a partir do diretório atual do shell.

O comportamento esperado é que o programa encontre os dados mesmo quando o serviço `systemd` for iniciado fora da pasta `backend`.

Os arquivos de dados envolvidos incluem:

- `backend/dados/produtos_mercado.csv`;
- `backend/dados/ingredientes_produtos.csv`;
- `backend/dados/regras_agosto_2026.csv`;
- `backend/dados/regras_setembro_2026.csv`;
- `backend/dados/vendas_supermercado_agosto_2026.csv`;
- `backend/dados/vendas_supermercado_setembro_2026.csv`;
- `backend/dados/descarte_supermercado_setembro_2026.csv`.

### Testes locais

Antes do deploy, validar:

- importação da configuração sem instalar pacotes;
- leitura de todos os CSVs;
- inicialização do bot com credenciais fornecidas por ambiente;
- perguntas que acionam cada ferramenta relevante;
- comportamento quando a API Gemini responde com erro ou limite excedido;
- ausência de segredos nos logs.

## Oracle Cloud Free Tier

A hospedagem planejada é uma VM Ubuntu Always Free na Oracle Cloud Infrastructure.

Pontos importantes:

- a criação da conta pode exigir cartão para verificação;
- a disponibilidade das VMs gratuitas depende da região e da capacidade disponível;
- o plano gratuito possui limites de recursos e pode sofrer indisponibilidade;
- não selecionar recursos pagos durante a criação da VM;
- conferir a estimativa de custo antes de concluir qualquer recurso;
- acompanhar a página de custos e limites da conta.

A configuração da VM deve usar somente recursos identificados como Always Free. Caso a região não tenha capacidade, deve-se verificar outra região permitida antes de escolher uma configuração paga.

## Instalação prevista na VM

Após criar a VM e acessar por SSH:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git
```

Em seguida, copiar o projeto para um diretório próprio, por exemplo `/opt/api-supermercado`, conferir as permissões e criar a virtualenv:

```bash
sudo mkdir -p /opt/api-supermercado
sudo chown -R "$USER":"$USER" /opt/api-supermercado
cd /opt/api-supermercado
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

O método de cópia pode ser Git, `scp` ou outro processo controlado. Os arquivos CSV necessários precisam estar presentes na VM.

## Credenciais na VM

As credenciais devem ficar em um arquivo que não pertença ao repositório, por exemplo:

```bash
sudo mkdir -p /etc/api-supermercado
sudo nano /etc/api-supermercado/app.env
sudo chmod 600 /etc/api-supermercado/app.env
```

O arquivo deve conter as variáveis reais:

```dotenv
TELEGRAM_BOT_TOKEN=valor_real
GEMINI_API_KEY=valor_real
GEMINI_MODEL=modelo_confirmado
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

Restringir o arquivo ao usuário que executará o serviço e evitar colocar seus valores em comandos compartilhados, screenshots, commits ou mensagens de log.

## Serviço systemd

O serviço deverá:

- iniciar depois da rede estar disponível;
- usar a virtualenv do projeto;
- definir o diretório de trabalho;
- carregar o arquivo de ambiente protegido;
- reiniciar sempre que o processo terminar inesperadamente;
- enviar a saída para o journal do sistema.

Modelo inicial, a ser ajustado ao caminho e ao usuário finais:

```ini
[Unit]
Description=Bot Telegram de analise de dados
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=api-bot
WorkingDirectory=/opt/api-supermercado/backend
EnvironmentFile=/etc/api-supermercado/app.env
ExecStart=/opt/api-supermercado/.venv/bin/python /opt/api-supermercado/backend/src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Instalação e ativação previstas:

```bash
sudo cp api-supermercado.service /etc/systemd/system/api-supermercado.service
sudo systemctl daemon-reload
sudo systemctl enable --now api-supermercado.service
sudo systemctl status api-supermercado.service
```

O nome do usuário, o caminho do projeto e o caminho do `main.py` devem ser confirmados depois que a estrutura final do deploy estiver definida.

## Diagnóstico e operação

Ver status:

```bash
sudo systemctl status api-supermercado.service
```

Acompanhar logs:

```bash
sudo journalctl -u api-supermercado.service -f
```

Ver logs recentes:

```bash
sudo journalctl -u api-supermercado.service -n 100 --no-pager
```

Reiniciar após alteração de código ou ambiente:

```bash
sudo systemctl restart api-supermercado.service
```

Verificar se o serviço inicia no boot:

```bash
systemctl is-enabled api-supermercado.service
```

Validar as últimas inicializações:

```bash
sudo journalctl -u api-supermercado.service -b --no-pager
```

## Resiliência e limites da IA

A aplicação deverá tratar pelo menos:

- timeout da API;
- resposta HTTP `429` por limite de requisições ou cota;
- indisponibilidade temporária do provedor;
- resposta inválida ou incompleta do modelo;
- falha de function calling;
- mensagens excessivamente longas.

Também deverão ser definidos limites de tamanho de mensagem, quantidade de chamadas por interação e comportamento de fallback. Um segundo provedor compatível com OpenAI poderá ser usado como contingência, mas só deve ser ativado depois que suas credenciais, custos e limites forem avaliados.

O plano gratuito do Gemini não significa disponibilidade ilimitada. É necessário acompanhar os limites atuais do Google AI Studio e evitar loops de chamadas, prompts desnecessariamente grandes e repetição automática sem limite.

## Segurança

- Nunca commitar `TELEGRAM_BOT_TOKEN` ou `GEMINI_API_KEY`.
- Não imprimir prompts completos, respostas sensíveis ou headers de autenticação nos logs.
- Não expor uma porta HTTP pública sem necessidade.
- Manter o sistema operacional atualizado.
- Usar autenticação SSH com chave e desabilitar práticas inseguras de acesso.
- Conferir permissões do arquivo de ambiente.
- Revogar e substituir chaves imediatamente se houver suspeita de exposição.
- Não escolher recursos Oracle que não estejam claramente marcados como Always Free.

## Troca de chaves

Quando uma chave precisar ser trocada:

1. Criar a nova chave no provedor correspondente.
2. Atualizar o arquivo de ambiente na VM, sem alterar o código-fonte.
3. Ajustar as permissões do arquivo.
4. Reiniciar o serviço.
5. Conferir o status e os logs sem exibir o valor da chave.
6. Revogar a chave antiga no provedor.

Exemplo:

```bash
sudo chmod 600 /etc/api-supermercado/app.env
sudo systemctl restart api-supermercado.service
sudo systemctl status api-supermercado.service
sudo journalctl -u api-supermercado.service -n 50 --no-pager
```

## Critérios de conclusão

O trabalho será considerado pronto quando:

- o código estiver em uma branch própria;
- nenhuma credencial estiver versionada;
- a aplicação instalar suas dependências de forma reproduzível;
- os CSVs forem encontrados independentemente do diretório de execução;
- o Gemini responder por API externa;
- o ReAct conseguir acionar as ferramentas esperadas;
- erros de API e limites forem tratados sem derrubar o serviço;
- a VM Oracle estiver usando somente recursos Always Free;
- o serviço `systemd` iniciar automaticamente e reiniciar após falhas;
- os logs forem consultáveis pelo `journalctl`;
- o bot for validado no Telegram após reboot da VM;
- os comandos efetivamente utilizados forem registrados neste documento.

## Registro de alterações

| Data | Alteração | Situação |
|---|---|---|
| 2026-09-19 | Criação deste documento para centralizar o deploy Oracle/Gemini | Em andamento |
| 2026-09-19 | Configuração inicial do DSPy para Gemini e atualização dos nomes das variáveis de ambiente | Concluído |
