# Smart Calculator

[![CI](https://github.com/NusratBegum/smart-calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/NusratBegum/smart-calculator/actions/workflows/ci.yml)

A three-tier web app where each user signs up, evaluates arithmetic expressions, and keeps a private calculation history. The whole stack starts with one `docker compose up`.

**Live demo:** https://smart-calculator-api.vercel.app · **API docs:** https://smart-calculator-api.vercel.app/docs

![Web client](docs/web-client.png)

**Stack:** FastAPI · Pydantic · SQLAlchemy 2.0 · PostgreSQL 16 · JWT (OAuth2 password bearer) · bcrypt · Streamlit · Docker Compose · pytest · GitHub Actions

## Architecture

```
┌─────────────┐   HTTP + JWT   ┌──────────────┐   SQLAlchemy   ┌──────────────┐
│  Streamlit  │ ─────────────▶ │   FastAPI    │ ─────────────▶ │ PostgreSQL 16│
│  frontend   │                │   backend    │                │              │
│  :8501      │ ◀───────────── │   :8000      │ ◀───────────── │  :5432       │
└─────────────┘      JSON      └──────────────┘                └──────────────┘
```

- **Frontend** (`frontend/`): Streamlit UI with login, register, calculate and history views. The backend also serves a small HTML/JS client at `/`, which is what the live demo shows.
- **Backend** (`backend/`): FastAPI app. Routes in `app/routes/`, ORM models in `app/models.py`, request and response schemas in `app/schemas.py`, auth in `app/auth.py`.
- **Database** (`database/schema.sql`): `users` and `calculation_history` tables, one-to-many with `ON DELETE CASCADE`. Applied automatically on first start.

## Features

- Register and log in; passwords are hashed with bcrypt, sessions use signed JWT access tokens.
- Each calculation is stored against the signed-in user, and `/history` returns only that user's rows, newest first.
- Expressions are parsed with Python's `ast` module and only numbers, `+ - * /` and unary signs are evaluated, so arbitrary code cannot run. Invalid input and division by zero return `400`.
- Usernames (3–50 characters) and passwords (8–72 characters) are validated by Pydantic before they reach the database.
- The database container has a health check, and the backend waits for it before starting. `/health` reports API status.

## API

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/register` | – | Create a user (`201`) |
| `POST` | `/login` | – | Return a bearer token |
| `POST` | `/calculate` | Bearer | Evaluate an expression and save it |
| `GET` | `/history` | Bearer | List the current user's calculations |
| `GET` | `/health` | – | Liveness check |

Interactive docs are at `http://localhost:8000/docs` once the stack is running.

## Run locally

Requires Docker with Compose.

```bash
cp .env.example .env          # then set real values, e.g. a JWT_SECRET from:
python -c "import secrets; print(secrets.token_urlsafe(64))"
docker compose up --build
```

- Frontend: http://localhost:8501
- API docs: http://localhost:8000/docs

## Deployment

The live demo runs the same FastAPI app as a Vercel Python function (`backend/` is the project root). With no `DATABASE_URL` set it falls back to SQLite, so demo accounts and history can be reset when the function restarts. Point `DATABASE_URL` at a hosted PostgreSQL database to make it persistent; the tables are created on startup if they don't exist.

## Tests

The suite covers the expression evaluator and the HTTP API (registration, validation, login, JWT protection, per-user history isolation, unsafe input) against a temporary SQLite database.

```bash
cd backend
pip install -r requirements.txt
python -m pytest -v
```

The suite covers the calculation engine: the four operators, unary minus, precedence and parentheses, and the error cases (division by zero, invalid syntax, disallowed expressions). GitHub Actions runs it on every push and pull request, then builds all Docker images.

## Project structure

```
smart-calculator/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app and router wiring
│   │   ├── auth.py          # bcrypt hashing, JWT create/verify, current-user dependency
│   │   ├── calculator.py    # AST-based safe evaluator
│   │   ├── database.py      # engine and session
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── routes/          # users.py, calc.py
│   ├── tests/
│   └── Dockerfile
├── frontend/                # Streamlit app + Dockerfile
├── database/schema.sql
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Roadmap

- Integration tests for the API against a real PostgreSQL service in CI
- Alembic migrations in place of the init script
- Cloud deployment

## Author

Nusrat Begum · [nusratbegum.dev](https://nusratbegum.dev) · [LinkedIn](https://www.linkedin.com/in/nusrat-begum)
