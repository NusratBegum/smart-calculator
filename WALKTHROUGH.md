# Smart Calculator — Walkthrough (Hints Only)

3-tier Cloud-Native Smart Calculator. Build order follows architecture: **Database → Backend → Frontend → Containerize → Deploy**.

Hints, guiding questions, research pointers. **No copy-paste code answers.** Write everything yourself.

---

## Project structure (set up first)

3 tiers → 3 top-level folders:

```
smart-calculator/
├── database/        ← Tier 3 (data)
│   └── schema.sql
├── backend/         ← Tier 2 (logic, FastAPI)
├── frontend/        ← Tier 1 (UI, Streamlit)
├── docker-compose.yml   ← added in Phase 4
└── .github/workflows/   ← added in Phase 5
```

Setup:
```
mkdir -p frontend backend database
```

---

## Phase 1 — System Design (DONE)

Gemini consult completed:
- 3-tier architecture: Streamlit → FastAPI → PostgreSQL
- Schema: `users` (id, username, password_hash, created_at) + `calculation_history` (id, user_id FK, expression, result, created_at)
- One-to-many: User → Calculations

See `_Gemini - direct access to Google AI.pdf` for full ERD.

---

## Phase 2 — Database (current phase)

### 2.1 Run Postgres in Docker ✅

Container `calc-db` running on port 5432. DB `smart_calculator` exists. Owner `calc_admin`.

### 2.2 Write schema file

Location: `database/schema.sql`

For each ERD column, translate to SQL. **Don't copy — translate yourself.**

**Research targets:**
- `SERIAL PRIMARY KEY` — auto-increment ID
- `VARCHAR(n)` vs `TEXT` — bounded vs unbounded string
- `UNIQUE` constraint
- `NOT NULL` constraint
- `DEFAULT CURRENT_TIMESTAMP`
- `REFERENCES table(col)` — foreign key
- `ON DELETE CASCADE` vs `ON DELETE RESTRICT`
- Postgres FLOAT type → `DOUBLE PRECISION` or `REAL`

**Decisions to make (document with `-- comment`):**
- ON DELETE behavior for FK
- VARCHAR length choices (why 50? why 255?)

### 2.3 Apply schema

```
docker exec -i calc-db psql -U calc_admin -d smart_calculator < database/schema.sql
```

Expect 2x `CREATE TABLE` output.

### 2.4 Verify

```
docker exec -it calc-db psql -U calc_admin -d smart_calculator -c "\dt"
docker exec -it calc-db psql -U calc_admin -d smart_calculator -c "\d users"
docker exec -it calc-db psql -U calc_admin -d smart_calculator -c "\d calculation_history"
```

Confirm:
- Both tables listed
- `users.id` shows `nextval(...)` (auto-increment proven)
- `calculation_history` bottom shows `Foreign-key constraints` referencing `users(id)`

### 2.5 Test FK + data flow manually

In psql:
1. Insert fake user → `INSERT INTO users (username, password_hash) VALUES ('alice', 'fake_hash');`
2. Get her id → `SELECT id FROM users WHERE username='alice';`
3. Insert calculation → `INSERT INTO calculation_history (user_id, expression, result) VALUES (1, '5+10', 15);`
4. Read back → `SELECT * FROM calculation_history WHERE user_id=1;`
5. **Test FK guard** → try `INSERT INTO calculation_history (user_id, ...) VALUES (999, ...)` — must fail with FK violation

Why test the failure? Trusting constraints without testing = surprise bugs in prod.

### 2.6 Cleanup test data (optional)

```sql
DELETE FROM calculation_history WHERE user_id=1;
DELETE FROM users WHERE username='alice';
```

### Phase 2 done checklist
- [ ] `database/schema.sql` written + committed
- [ ] Tables created in `smart_calculator` DB
- [ ] FK constraint verified by failed insert
- [ ] Test data cleaned

---

## Phase 3 — Backend (FastAPI)

### 3.1 Folder structure inside `backend/`

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          ← FastAPI entry, mounts routes
│   ├── database.py      ← SQLAlchemy engine, session
│   ├── models.py        ← ORM classes (User, CalculationHistory)
│   ├── schemas.py       ← Pydantic request/response models
│   ├── auth.py          ← password hash + JWT helpers
│   ├── calculator.py    ← OOP Calculator class
│   └── routes/
│       ├── __init__.py
│       ├── users.py     ← /register, /login
│       └── calc.py      ← /calculate, /history
├── requirements.txt
└── .env                 ← DB creds, JWT secret (gitignored)
```

**Guiding question:** why `models.py` AND `schemas.py`?
- `models.py` = SQLAlchemy ORM (maps to DB tables)
- `schemas.py` = Pydantic (validates HTTP request/response)
- Different concerns. Don't merge.

### 3.2 Python environment

Research:
- `python -m venv venv` then `source venv/bin/activate`
- Or `pyenv` for Python version management
- `pip install -r requirements.txt`

Initial `requirements.txt` needs:
- `fastapi`
- `uvicorn[standard]` (ASGI server)
- `sqlalchemy`
- `psycopg2-binary` (Postgres driver)
- `pydantic[email]`
- `passlib[bcrypt]` (password hash)
- `python-jose[cryptography]` (JWT)
- `python-dotenv` (load .env)

### 3.3 Database connection (`database.py`)

Research:
- SQLAlchemy `create_engine`
- `sessionmaker`
- `declarative_base`
- DB URL format: `postgresql://user:pass@host:port/dbname`

**Guiding question:** where does the URL come from? → `.env` file via `python-dotenv`. Never hardcode.

### 3.4 ORM models (`models.py`)

Match the SQL schema. Two classes: `User`, `CalculationHistory`.

Research:
- SQLAlchemy `Column`, `Integer`, `String`, `Float`, `DateTime`, `ForeignKey`
- `relationship()` for navigating from User to their calculations

**Guiding question:** ORM gives you `user.calculations` (list). How does it know? → `relationship()` declaration + back-populates.

### 3.5 Pydantic schemas (`schemas.py`)

Different shapes for different uses:
- `UserCreate` — request body for `/register` (has password)
- `UserLogin` — request body for `/login` (has password)
- `UserOut` — response (NO password)
- `Token` — response for `/login` (the JWT)
- `CalculateRequest` — has expression
- `CalculateResponse` — has result
- `HistoryItem` — one row from history table

**Guiding question:** why NEVER return password_hash? → Even hashed, leaking it = attack surface. Response schemas exist to filter.

### 3.6 Calculator class (`calculator.py`)

OOP requirement. Design choices:

**Option A** — method-per-op:
```
class Calculator:
    def add(self, a, b): ...
    def subtract(self, a, b): ...
    def divide(self, a, b): ...  # raises DivisionByZero
```

**Option B** — single evaluate:
```
class Calculator:
    def evaluate(self, expression: str) -> float: ...
```

Option B more flexible but harder (parsing). Option A simpler. Brief says expression like `"5 + 10"` so Option B closer to spec.

**Security:** NEVER use Python `eval()` on user input. Research safer alternatives:
- `ast.parse` + walk tree, allow only numbers + arithmetic ops
- Or restricted operators dict + custom parser
- Or library like `simpleeval`

Custom exception class: `class CalculationError(Exception): pass` — routes catch this → return HTTP 400.

### 3.7 Auth (`auth.py`)

**Password hashing:**
- `passlib.context.CryptContext(schemes=["bcrypt"])`
- `pwd_context.hash(plain)` on register
- `pwd_context.verify(plain, hashed)` on login

**JWT:**
- Sign token on successful login → return to client
- Client sends `Authorization: Bearer <token>` on protected requests
- FastAPI dependency `get_current_user(token: str = Depends(oauth2_scheme))` decodes + returns User
- Use `python-jose`: `jwt.encode(payload, SECRET, algorithm="HS256")`

**Secrets:**
- `JWT_SECRET` from `.env`
- Token expiry → research `exp` claim, e.g. 30 min

### 3.8 Routes

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/register` | no | create user |
| POST | `/login` | no | return JWT |
| POST | `/calculate` | yes | run math, save row |
| GET | `/history` | yes | return user's rows |

**Guiding question:** for `/calculate` and `/history`, how does route know WHICH user? → JWT contains user_id → `Depends(get_current_user)` extracts it.

### 3.9 Run + test

```
cd backend
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` → FastAPI auto-generated Swagger UI. Test each endpoint here BEFORE writing frontend.

### Phase 3 done checklist
- [ ] All 4 endpoints work in `/docs`
- [ ] Register → user row appears in DB
- [ ] Login → returns JWT
- [ ] `/calculate` with valid token → row in `calculation_history`
- [ ] `/calculate` divide by zero → HTTP 400, no crash
- [ ] `/history` without token → HTTP 401
- [ ] `/history` with token → only that user's rows

---

## Phase 4 — Frontend (Streamlit)

### 4.1 Folder

```
frontend/
├── app.py
├── requirements.txt    ← streamlit, requests, python-dotenv
└── .env                ← API_BASE_URL=http://localhost:8000
```

### 4.2 Key concept — Streamlit re-runs entire script

Every button click → script runs top to bottom. State dies unless saved in `st.session_state`.

Research: `st.session_state` (dict-like). Store JWT here after login.

### 4.3 Two views, one file

Pattern:
```
if "token" not in st.session_state:
    show_login_or_register()
else:
    show_calculator_and_history()
```

### 4.4 Talk to backend

Research `requests` library:
- `requests.post(url, json={...})` → register, login, calculate
- `requests.get(url, headers={"Authorization": f"Bearer {token}"})` → history
- Check `response.status_code` and `response.json()`

### 4.5 Display history

`st.dataframe(list_of_dicts)` or `st.table(...)`.

### 4.6 Logout

Button → `del st.session_state["token"]` → script reruns → shows login again.

### Phase 4 done checklist
- [ ] Register form works
- [ ] Login stores JWT in session_state
- [ ] Calculator submits expression, shows result
- [ ] History table shows current user's calculations
- [ ] Logout button clears session
- [ ] App refresh keeps user logged in? (NO — session_state dies on full refresh. That's OK for v1.)

---

## Phase 5 — Containerization (Docker)

### 5.1 Three Dockerfiles? No — TWO

- `backend/Dockerfile` — FastAPI app
- `frontend/Dockerfile` — Streamlit app
- `database/` — no Dockerfile needed, use official `postgres:16` image
- `docker-compose.yml` at root — orchestrates all 3

### 5.2 Backend Dockerfile

Research:
- `FROM python:3.11-slim`
- `WORKDIR /app`
- `COPY requirements.txt .` → `RUN pip install --no-cache-dir -r requirements.txt`
- `COPY . .`
- `EXPOSE 8000`
- `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`

**Guiding question:** why copy requirements.txt BEFORE source code? → Docker layer cache. Source changes more often than deps. Saves rebuild time.

### 5.3 Frontend Dockerfile

Similar pattern. `CMD` runs `streamlit run app.py --server.address 0.0.0.0 --server.port 8501`.

### 5.4 docker-compose.yml

3 services: `db`, `backend`, `frontend`.

Research:
- `services:` syntax
- `build:` (path to Dockerfile) vs `image:` (pull from registry)
- `environment:` (env vars)
- `ports:` (host:container)
- `volumes:` (named volume for DB data)
- `depends_on:` (start order)
- Default network — services reach each other by service name (`db`, not `localhost`)

**Critical traps:**
- Backend's DB URL inside compose → `postgresql://calc_admin:pass@db:5432/smart_calculator` — host is `db`, not `localhost`
- `depends_on` only waits for container START, not DB READINESS — research `healthcheck:` block
- Mount `database/schema.sql` to `/docker-entrypoint-initdb.d/` on Postgres service → auto-runs on first boot

### 5.5 `.dockerignore`

Stop these from leaking into image:
```
__pycache__
*.pyc
.env
.git
venv/
```

### 5.6 Run it all

```
docker-compose up --build
```

### Phase 5 done checklist
- [ ] `docker-compose up` brings all 3 services up
- [ ] Frontend at `http://localhost:8501` works end-to-end
- [ ] Stop with `docker-compose down`, restart — data persists (volume working)
- [ ] Schema auto-applied on fresh DB volume

---

## Phase 6 — CI/CD + Azure Deploy

### 6.1 Git + GitHub

- `git init` at project root
- `.gitignore` — must include `.env`, `__pycache__`, `venv/`, `.DS_Store`
- Create GitHub repo, push
- **Never commit `.env`**

### 6.2 GitHub Actions

File: `.github/workflows/deploy.yml`

Trigger: push to `main`.

Jobs:
1. Checkout code
2. Login to container registry (Azure Container Registry recommended, or Docker Hub)
3. Build backend image, push
4. Build frontend image, push
5. (Optional) Trigger Azure deploy

Research:
- `actions/checkout@v4`
- `docker/login-action@v3`
- `docker/build-push-action@v5`

### 6.3 GitHub Secrets

Add via repo Settings → Secrets and variables → Actions:
- `AZURE_CREDENTIALS`
- `ACR_USERNAME`, `ACR_PASSWORD` (or service principal)
- `DB_PASSWORD`
- `JWT_SECRET`

Reference in workflow as `${{ secrets.NAME }}`.

### 6.4 Azure deploy

Two options:
- **Azure Container Apps** — newer, simpler, scales to zero
- **Azure App Service for Containers** — older, well-documented

Plus:
- **Azure Database for PostgreSQL Flexible Server** — managed DB, replaces Postgres container in prod
- Update backend `DATABASE_URL` env var to point at Azure DB

**Guiding question:** still need `db` service in compose for prod? → No. Compose stays for local dev. Prod uses managed DB.

### Phase 6 done checklist
- [ ] Code on GitHub, `.env` not committed
- [ ] Push to main triggers Actions
- [ ] Images build + push successfully
- [ ] App accessible at public Azure URL
- [ ] Can register + login + calculate from public internet

---

## Cross-cutting reminders

- **Never** commit `.env` files
- **Never** use Python `eval()` on user input
- **Never** store plaintext passwords
- **Never** hardcode secrets in source
- **Always** test failure paths (divide by zero, FK violation, missing auth)
- **Always** check `response.status_code` before `response.json()`
- Commit often, small commits, clear messages

---

## Current status

✅ Phase 1 — Design (done via Gemini)
✅ Phase 2.1 — Postgres container running
⬜ Phase 2.2 — Write `database/schema.sql` ← **YOU ARE HERE**
⬜ Phase 2.3-2.6 — Apply + verify schema
⬜ Phase 3 — Backend
⬜ Phase 4 — Frontend
⬜ Phase 5 — Docker compose
⬜ Phase 6 — CI/CD + Azure
