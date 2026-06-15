# Financial Assistant

Assistente financeiro com inteligencia artificial para WhatsApp. O projeto usa LangGraph para orquestrar o agente, tools para registrar e consultar gastos, Evolution API para conexao com WhatsApp e PostgreSQL para persistencia dos dados.

## Stacks Utilizadas

- Docker
- LangGraph
- Evolution API
- AI Tools
- PostgreSQL

## Estrutura De Arquivos

```txt
financial-assistant/
|-- src/
|   |-- ai/
|   |   |-- checkpointer/      # Configuracao do checkpointer do LangGraph
|   |   |-- context/           # Tipos de contexto do agente
|   |   |-- llm/               # Configuracao do modelo de IA
|   |   |-- nodes/             # Nodes e tools do agente
|   |   |-- prompts/           # Persona e instrucoes do agente
|   |   |-- state/             # Estado conversacional do grafo
|   |   |-- agent.py           # Interface principal do agente
|   |   `-- graph.py           # Montagem do grafo LangGraph
|   |-- communication/         # Integracao com Evolution API
|   |-- config/                # Configuracoes auxiliares
|   |-- core/                  # Registro de rotas e middlewares
|   |-- database/              # Conexao, models e registro das tabelas
|   |-- routes/
|   |   `-- webhook/           # Endpoints chamados pela Evolution API
|   `-- app.py                 # Aplicacao FastAPI
|-- docker-compose.yml         # Servicos da aplicacao
|-- Dockerfile                 # Imagem do backend
|-- requirements.txt           # Dependencias Python
`-- README.md
```

## Como Rodar

1. Clone o repositorio:

```bash
git clone https://github.com/hertzrafael/financial-assistant.git
cd financial-assistant
```

2. Abra o arquivo `docker-compose.yml`.

3. No servico `backend`, informe sua chave da OpenAI na variavel:

```yaml
OPENAI_API_KEY=sua-chave-aqui
```

4. Suba os containers:

```bash
docker compose up -d
```

Depois disso, os principais servicos ficam disponiveis em:

- Backend: `http://localhost:8080`
- Evolution API: `http://localhost:8081`
- Manager da Evolution API: `http://localhost:8081/manager`

## Conectando O WhatsApp

1. Acesse o manager da Evolution API:

```txt
http://localhost:8081/manager
```

2. Para realizar o login, use como **Api Key Global** o valor configurado em `AUTHENTICATION_API_KEY` no container `evolution-api` dentro do `docker-compose.yml`.

3. Apos inserir a chave, voce deve entrar no dashboard da Evolution API.

4. Quando a API inicializar, o backend ja deve criar automaticamente a instancia de conexao. Caso a instancia nao apareca, reinicie o backend:

```bash
docker compose restart backend
```

5. Acesse a instancia criada no dashboard.

6. Clique para gerar o QR Code.

7. No celular, abra o WhatsApp e va em:

```txt
Dispositivos conectados -> Adicionar dispositivo -> Ler QR Code
```

8. Leia o QR Code exibido no dashboard.

Depois da conexao, o agente ja estara funcionando. Basta enviar mensagens para o WhatsApp conectado.

## Exemplos De Uso

```txt
Gastei 35 reais no posto de gasolina, categoria transporte.
```

```txt
Me traga todos os meus gastos do mes.
```

```txt
O que posso fazer para melhorar minha vida financeira?
```

## Observacoes

- Se alterar variaveis no `docker-compose.yml`, reinicie os containers.
- O webhook do backend fica em `http://localhost:8080/api/v1/webhook`, mas dentro da rede Docker a Evolution API deve chamar o backend pelo nome do servico.
