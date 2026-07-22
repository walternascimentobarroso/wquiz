# WQuiz

Plataforma de quizzes com API REST (HATEOAS), frontend do usuário e painel administrativo.

## Stack

| App | Tecnologia |
|-----|------------|
| API | FastAPI, SQLAlchemy, SQLite, JWT, Swagger |
| Usuário | React, Vite, TypeScript, Nginx |
| Admin | React, Vite, TypeScript, Nginx |

## Modos de estudo

- **Teste prático** — resultado só no final
- **Estudo** — explicação após cada resposta
- **Flashcards** — revisão estilo Anki (SRS)

## Docker (recomendado)

```bash
make help    # lista targets
make build   # build + sobe tudo
make up      # sobe containers
make logs    # logs do backend
make stop    # para containers
make destroy # remove containers e volumes
```

URLs após `make build`:

| App | URL |
|-----|-----|
| API / Swagger | http://localhost:8000/docs |
| Frontend | http://localhost:5173 |
| Admin | http://localhost:5174 |

Admin padrão: `admin@example.com` / `admin123`

Variáveis em `.env` (criado automaticamente a partir de `.env.example`).

## Desenvolvimento local (sem Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend usuário

```bash
cd frontend
npm install
npm run dev
```

### Frontend admin

```bash
cd admin
npm install
npm run dev
```

## Estrutura

```
wquiz/
├── backend/            # API FastAPI + HATEOAS
├── frontend/           # App do usuário
├── admin/              # Painel administrativo
├── docker-compose.yml
├── Makefile
└── .env.example
```
