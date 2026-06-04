# Smart Calculator — Asana Project Plan

**Project name:** Smart Calculator — Cloud Native
**Start:** 2026-05-24 (Sat)
**Deadline:** 2026-05-30 (Fri) — 7 days
**Owner:** you

## How to use this file
1. Create new Asana project: blank, list view
2. Add the 6 sections below as Asana sections
3. For each task: copy title + paste, set due date + priority
4. Subtasks → add via Asana subtask feature
5. Or import as CSV (Asana → Project → ⋯ → Import → CSV) — bottom of file has CSV-ready table

---

## Timeline overview

| Day | Date | Focus | Phases |
|-----|------|-------|--------|
| Sat | May 24 | DB wrap + Backend kickoff | 2 wrap → 3a-3c |
| Sun | May 25 | Backend core | 3d-3f |
| Mon | May 26 | Backend auth + endpoints | 3g-3i |
| Tue | May 27 | Frontend Streamlit | 4 full |
| Wed | May 28 | Dockerize all 3 tiers | 5 full |
| Thu | May 29 | CI/CD + Azure deploy | 6 full |
| Fri | May 30 | Buffer / polish / README / demo | finalize |

**Risk:** Phase 6 (Azure) is biggest unknown. If slipping, deploy backend+frontend separately and skip CI/CD on first pass — manual deploy still scores.

---

## SECTION 1 — Phase 2: Database (Sat May 24) ✅ MOSTLY DONE

**Done already:**
- ✅ Postgres container running (`calc-db`)
- ✅ `database/schema.sql` written + applied
- ✅ Tables verified (users, calculation_history)
- ✅ FK + CASCADE proven via manual inserts

**Remaining tasks today:**

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 1.1 | Clean DB state | `TRUNCATE TABLE calculation_history, users RESTART IDENTITY CASCADE;` | 5 min | Low |
| 1.2 | Write `database/test.sql` | 6 tests (insert user, FK guard, CASCADE proof), self-documenting comments | 30 min | Med |
| 1.3 | Git init + first commit | `git init`, `.gitignore` (venv, `.env`, `__pycache__`, `.DS_Store`, `*.pyc`), commit Phase 1+2 artifacts | 15 min | High |
| 1.4 | Create GitHub repo + push | Public or private repo, push main | 10 min | High |

---


## SECTION 2 — Phase 3: Backend FastAPI (Sat–Mon May 24–26)

### Sat May 24 evening — Setup + Scaffold

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 2.1 | Folder scaffold | `backend/app/`, `backend/app/routes/`, all `__init__.py` files, empty `main.py` | 10 min | High |
| 2.2 | Python venv | `python -m venv venv`, activate, document command in README | 10 min | High |
| 2.3 | `requirements.txt` | fastapi, uvicorn[standard], sqlalchemy, psycopg2-binary, pydantic, passlib[bcrypt], python-jose[cryptography], python-dotenv | 15 min | High |
| 2.4 | `.env` + `.env.example` | DB_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MIN. Add `.env` to gitignore. Commit `.env.example` template | 15 min | High |

### Sun May 25 — DB + Models + OOP Calculator

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 3.1 | `database.py` | SQLAlchemy engine, sessionmaker, Base, get_db() dependency | 30 min | High |
| 3.2 | `models.py` | User class (matches users table), CalculationHistory class (matches calculation_history), relationship() back-populates | 45 min | High |
| 3.3 | `schemas.py` | Pydantic: UserCreate, UserOut, UserLogin, Token, CalculateRequest, CalculateResponse, HistoryItem | 45 min | High |
| 3.4 | `calculator.py` | OOP Calculator class. evaluate() method. Custom CalculationError exception. NO eval() — research ast/simpleeval | 90 min | High |
| 3.5 | Unit test calculator | `tests/test_calculator.py` with pytest. Cover add, sub, mul, div, div-by-zero, invalid expression | 45 min | Med |

### Mon May 26 — Auth + Routes + Integration

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 4.1 | `auth.py` password hash | passlib CryptContext, hash_password(), verify_password() | 30 min | High |
| 4.2 | `auth.py` JWT | create_access_token(), decode_token(), get_current_user() dependency | 60 min | High |
| 4.3 | `routes/users.py` | POST /register (hash pwd, insert user, return UserOut), POST /login (verify pwd, return Token) | 60 min | High |
| 4.4 | `routes/calc.py` | POST /calculate (auth, evaluate, save row, return result). GET /history (auth, query user's rows) | 60 min | High |
| 4.5 | `main.py` wire-up | FastAPI app, include both routers, CORS for Streamlit later, Base.metadata.create_all (or skip — schema already applied via SQL) | 20 min | High |
| 4.6 | Manual test via `/docs` | Register → login → copy token → authorize → calculate → history. Verify divide-by-zero returns 400 | 45 min | High |
| 4.7 | Commit + push backend | Commit message: "feat(backend): FastAPI app with auth + calculator endpoints" | 5 min | Med |

---

## SECTION 3 — Phase 4: Frontend Streamlit (Tue May 27)

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 5.1 | `frontend/requirements.txt` | streamlit, requests, python-dotenv | 5 min | High |
| 5.2 | `frontend/.env` | API_BASE_URL=http://localhost:8000 | 5 min | High |
| 5.3 | `app.py` skeleton | Title, st.session_state init, two-view router (`if "token" in state` switch) | 30 min | High |
| 5.4 | Login + Register view | Two forms (st.form), POST to /login and /register, store token in session_state on success, st.error on failure | 60 min | High |
| 5.5 | Calculator view | Expression input, "Calculate" button, POST to /calculate with auth header, display result | 45 min | High |
| 5.6 | History view | GET /history with auth header, render as st.dataframe with columns: expression, result, created_at | 30 min | High |
| 5.7 | Logout button | Clear session_state, st.rerun() | 10 min | Med |
| 5.8 | End-to-end manual test | Fresh DB → register → login → 5 calculations → check history → logout → re-login → history still there | 30 min | High |
| 5.9 | Commit frontend | "feat(frontend): Streamlit UI with auth + history" | 5 min | Med |

---

## SECTION 4 — Phase 5: Containerize (Wed May 28)

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 6.1 | `backend/Dockerfile` | python:3.11-slim, WORKDIR, copy requirements first (cache layer), pip install, copy app, CMD uvicorn | 45 min | High |
| 6.2 | `frontend/Dockerfile` | python:3.11-slim, install deps, copy app.py, CMD streamlit run --server.address 0.0.0.0 | 30 min | High |
| 6.3 | `.dockerignore` files | One per service. Block __pycache__, .env, venv, .git, *.pyc | 15 min | High |
| 6.4 | `docker-compose.yml` | 3 services: db (postgres:16 + volume + env), backend (build, depends_on db, env DATABASE_URL pointing at `db` not `localhost`), frontend (build, depends_on backend, API_BASE_URL pointing at `backend:8000`) | 60 min | High |
| 6.5 | Mount schema.sql | Map `database/schema.sql` → `/docker-entrypoint-initdb.d/01-schema.sql` on db service so fresh container auto-creates tables | 20 min | High |
| 6.6 | Healthcheck on db | Postgres `pg_isready` healthcheck so backend waits for ACTUAL readiness, not just container start | 30 min | Med |
| 6.7 | Full bring-up test | Stop old `calc-db` container. `docker compose up --build`. Verify all 3 services healthy. Test app at localhost:8501 end-to-end | 45 min | High |
| 6.8 | Persistence test | `docker compose down` (keep volume) → `docker compose up` → previous user/history still there | 15 min | High |
| 6.9 | Commit | "feat(docker): compose orchestration for 3-tier app" | 5 min | Med |

---

## SECTION 5 — Phase 6: CI/CD + Azure (Thu May 29)

### Pre-work — Azure account

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 7.0 | Azure free account | Sign up if needed, install Azure CLI (`brew install azure-cli`), `az login` | 30 min | Blocker |

### CI pipeline

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 7.1 | Create Azure Container Registry | `az acr create`, get login server name | 20 min | High |
| 7.2 | `.github/workflows/ci.yml` | Trigger: push to main. Jobs: checkout, login to ACR, build backend image, push, build frontend image, push | 60 min | High |
| 7.3 | GitHub Secrets | AZURE_CREDENTIALS (service principal JSON), ACR_LOGIN_SERVER, ACR_USERNAME, ACR_PASSWORD | 30 min | High |
| 7.4 | Trigger first build | Push commit, watch Actions tab, fix errors, re-push | 45 min | High |

### Cloud deploy

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 8.1 | Azure Database for PostgreSQL Flexible Server | Create, set firewall rule (allow Azure services), run `database/schema.sql` against it via psql | 45 min | High |
| 8.2 | Azure Container Apps environment | Create, link to ACR | 30 min | High |
| 8.3 | Deploy backend container app | env vars: DATABASE_URL (Azure pg), JWT_SECRET, ingress=external on port 8000 | 45 min | High |
| 8.4 | Deploy frontend container app | env var: API_BASE_URL (backend container app public URL), ingress=external on 8501 | 30 min | High |
| 8.5 | Verify live | Open frontend URL in browser, register, calculate, check history works in cloud | 30 min | High |
| 8.6 | Hook deploy into CI | Add deploy step to `ci.yml` so push to main also redeploys container apps | 60 min | Med |
| 8.7 | Commit + push final | "feat(deploy): live on Azure with CI/CD pipeline" | 5 min | High |

---

## SECTION 6 — Polish + Demo (Fri May 30)

| # | Task | Subtasks | Est | Priority |
|---|------|----------|-----|----------|
| 9.1 | README.md | Architecture diagram (copy from Gemini doc), setup instructions, local run via docker-compose, env var docs, live URL | 60 min | High |
| 9.2 | Architecture diagram artifact | Export Gemini's ASCII to actual image via draw.io or Excalidraw, save in `docs/architecture.png` | 45 min | Med |
| 9.3 | Demo walkthrough | Record 2-min screen capture: register, login, calculate, history. Save to repo or YouTube unlisted | 30 min | Low |
| 9.4 | Edge case audit | Empty expression, very long expression, divide by zero, expired JWT, wrong password, duplicate username | 45 min | Med |
| 9.5 | Final commit + tag | `git tag v1.0`, push tag, link in README | 10 min | High |
| 9.6 | Buffer | Catch up on any slipped tasks from earlier days | flexible | — |

---

## Daily total estimates

| Day | Total est | Realistic 8h day? |
|-----|-----------|-------------------|
| Sat | ~2h (DB wrap) + 50 min scaffold = ~3h | Yes — lighter day, recovery |
| Sun | 4h 15min | Yes |
| Mon | 4h 40min | Yes |
| Tue | 3h 40min | Yes |
| Wed | 4h 25min | Yes |
| Thu | 7h 15min (BIG day) | Tight — buffer Fri eats overflow |
| Fri | 3h 30min + buffer | Yes |

**Total: ~30 hours over 7 days.** Feasible if uninterrupted. Cut Phase 6.6 (CI auto-deploy) + 9.3 (video) if behind.

---

## Risk register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Azure free tier limits / billing surprise | Med | Use Container Apps consumption plan (scales to 0). Stop resources after demo. |
| JWT implementation confusion | High | Budget 2h not 1h. Use FastAPI tutorial directly. |
| Docker compose networking issues (`db` vs `localhost`) | High | Test bring-up early (Wed start), not Thu morning |
| CI/CD secrets misconfigured | Med | Start with manual ACR push to verify auth, then automate |
| Schema drift between local DB + Azure DB | Med | Run same `schema.sql` against both. Mount in compose. |

---

## CSV import format (paste into Asana CSV importer)

```csv
Task Name,Section,Due Date,Priority,Estimate (minutes)
Clean DB state,Phase 2 Database,2026-05-24,Low,5
Write database/test.sql,Phase 2 Database,2026-05-24,Medium,30
Git init + first commit,Phase 2 Database,2026-05-24,High,15
Create GitHub repo + push,Phase 2 Database,2026-05-24,High,10
Folder scaffold backend,Phase 3 Backend,2026-05-24,High,10
Python venv setup,Phase 3 Backend,2026-05-24,High,10
requirements.txt,Phase 3 Backend,2026-05-24,High,15
.env + .env.example,Phase 3 Backend,2026-05-24,High,15
database.py SQLAlchemy,Phase 3 Backend,2026-05-25,High,30
models.py ORM,Phase 3 Backend,2026-05-25,High,45
schemas.py Pydantic,Phase 3 Backend,2026-05-25,High,45
calculator.py OOP,Phase 3 Backend,2026-05-25,High,90
Unit test calculator,Phase 3 Backend,2026-05-25,Medium,45
auth.py password hash,Phase 3 Backend,2026-05-26,High,30
auth.py JWT,Phase 3 Backend,2026-05-26,High,60
routes/users.py,Phase 3 Backend,2026-05-26,High,60
routes/calc.py,Phase 3 Backend,2026-05-26,High,60
main.py wire-up,Phase 3 Backend,2026-05-26,High,20
Manual test /docs,Phase 3 Backend,2026-05-26,High,45
Commit backend,Phase 3 Backend,2026-05-26,Medium,5
frontend requirements.txt,Phase 4 Frontend,2026-05-27,High,5
frontend .env,Phase 4 Frontend,2026-05-27,High,5
app.py skeleton,Phase 4 Frontend,2026-05-27,High,30
Login + Register view,Phase 4 Frontend,2026-05-27,High,60
Calculator view,Phase 4 Frontend,2026-05-27,High,45
History view,Phase 4 Frontend,2026-05-27,High,30
Logout button,Phase 4 Frontend,2026-05-27,Medium,10
End-to-end manual test,Phase 4 Frontend,2026-05-27,High,30
Commit frontend,Phase 4 Frontend,2026-05-27,Medium,5
backend Dockerfile,Phase 5 Docker,2026-05-28,High,45
frontend Dockerfile,Phase 5 Docker,2026-05-28,High,30
.dockerignore files,Phase 5 Docker,2026-05-28,High,15
docker-compose.yml,Phase 5 Docker,2026-05-28,High,60
Mount schema.sql to db init,Phase 5 Docker,2026-05-28,High,20
Healthcheck on db,Phase 5 Docker,2026-05-28,Medium,30
Full compose bring-up test,Phase 5 Docker,2026-05-28,High,45
Persistence test,Phase 5 Docker,2026-05-28,High,15
Commit docker,Phase 5 Docker,2026-05-28,Medium,5
Azure account + CLI,Phase 6 Deploy,2026-05-29,High,30
Create ACR,Phase 6 Deploy,2026-05-29,High,20
ci.yml workflow,Phase 6 Deploy,2026-05-29,High,60
GitHub Secrets,Phase 6 Deploy,2026-05-29,High,30
Trigger first CI build,Phase 6 Deploy,2026-05-29,High,45
Azure Postgres Flexible,Phase 6 Deploy,2026-05-29,High,45
Container Apps environment,Phase 6 Deploy,2026-05-29,High,30
Deploy backend container app,Phase 6 Deploy,2026-05-29,High,45
Deploy frontend container app,Phase 6 Deploy,2026-05-29,High,30
Verify live deployment,Phase 6 Deploy,2026-05-29,High,30
Hook deploy into CI,Phase 6 Deploy,2026-05-29,Medium,60
Final deploy commit,Phase 6 Deploy,2026-05-29,High,5
README.md,Phase 7 Polish,2026-05-30,High,60
Architecture diagram artifact,Phase 7 Polish,2026-05-30,Medium,45
Demo walkthrough video,Phase 7 Polish,2026-05-30,Low,30
Edge case audit,Phase 7 Polish,2026-05-30,Medium,45
Final commit + tag v1.0,Phase 7 Polish,2026-05-30,High,10
```

---

## Definition of Done

Project = done when ALL true:
- [ ] User can register + login on public Azure URL
- [ ] User can perform calculation, see result
- [ ] User can view their history (only their own)
- [ ] Divide by zero returns clean error, no crash
- [ ] All code on GitHub, main branch
- [ ] `docker compose up` works locally
- [ ] Push to main auto-deploys via Actions
- [ ] README explains setup + has live URL
- [ ] Passwords hashed, never stored plain
- [ ] JWT protecting `/calculate` + `/history`

---

# Build Guides (step-by-step teaching for each task)

Detailed teaching notes for each backend/frontend file. Appended as we work through them.

---

## Guide 3.1 — `backend/app/database.py`

**Goal:** Connect FastAPI to Postgres via SQLAlchemy. Provide `engine`, `SessionLocal`, `Base`, `get_db()` for rest of app.

### Concepts (read first)

**FastAPI** = Python web framework. Decorators turn functions into HTTP endpoints. Example shape:
```python
@app.get("/hello")
def say_hi():
    return {"message": "hi"}
```

**`.env`** = secrets file (gitignored). Code reads at runtime via `python-dotenv`:
```python
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv("DATABASE_URL")
```

**SQLAlchemy 3 pieces:**
| Piece | What | When |
|-------|------|------|
| `engine` | connection pool to Postgres | once at startup |
| `Session` | one transaction / unit of work | per HTTP request |
| `Base` | parent class for ORM models | once |

### Steps

**Step 1 — Imports (4 lines)**

| Symbol | From |
|--------|------|
| `create_engine` | `sqlalchemy` |
| `sessionmaker`, `declarative_base` | `sqlalchemy.orm` |
| `load_dotenv` | `dotenv` |
| `os` | stdlib |

Test: `python -c "import app.database"` — no error.

**Step 2 — Load .env**
```python
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
```
Test: `python -c "from app.database import DATABASE_URL; print(DATABASE_URL)"` — prints full URL.

**Step 3 — Engine**
```python
engine = create_engine(DATABASE_URL)
```
Test: `python -c "from app.database import engine; c = engine.connect(); print('connected'); c.close()"` — prints `connected`.

**Step 4 — Session factory**
```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```
- `bind=engine` → which DB sessions will use
- `autocommit=False` → must explicitly `.commit()`
- `autoflush=False` → no surprise writes mid-query

Test: `python -c "from app.database import SessionLocal; s = SessionLocal(); print(s); s.close()"`

**Step 5 — Base class**
```python
Base = declarative_base()
```
Used in `models.py`: `class User(Base): __tablename__ = "users"`.

Test: `python -c "from app.database import Base; print(Base)"`

**Step 6 — `get_db()` dependency**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Why `yield` not `return`:** FastAPI runs route → continues past `yield` after route ends → `finally` closes connection. Prevents connection leaks. Standard FastAPI pattern, memorize it.

Test: `python -c "from app.database import engine, SessionLocal, Base, get_db; print('all 4 imports work')"`

### Common mistakes
1. `load_dotenv()` called after `os.getenv` → empty value
2. `Base = declarative_base` (no parens) → reference to function, not class
3. `return db` instead of `yield db` → breaks FastAPI cleanup
4. Run from project root not `backend/` → `.env` not found
5. Missing `bind=engine` in sessionmaker → sessions don't know which DB

### Done checklist
- [ ] All 6 steps pass their individual smoke test
- [ ] Final import-all test prints `all 4 imports work`
- [ ] Commit: `feat(backend): SQLAlchemy database connection layer`
