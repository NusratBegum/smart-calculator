from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, calc

app = FastAPI(title="Smart Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, tags=["users"])
app.include_router(calc.router, tags=["calculator"])
