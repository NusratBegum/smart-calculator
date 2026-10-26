from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app import models  # noqa: F401  (registers tables on Base.metadata)
from app.database import Base, engine
from app.routes import calc, users

STATIC_DIR = Path(__file__).parent / "static"

# Runs at import so serverless hosts that skip lifespan events still get the
# tables. A no-op on PostgreSQL, where database/schema.sql already created them.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Smart Calculator API",
    description="Register, log in with a JWT, evaluate arithmetic safely and keep a private history.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, tags=["users"])
app.include_router(calc.router, tags=["calculator"])


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
