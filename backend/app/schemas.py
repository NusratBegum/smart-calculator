from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=72)  # bcrypt uses the first 72 bytes


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class CalculateRequest(BaseModel):
    expression: str = Field(min_length=1, max_length=100)


class CalculateResponse(BaseModel):
    expression: str
    result: float


class HistoryItem(BaseModel):
    id: int
    expression: str
    result: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
