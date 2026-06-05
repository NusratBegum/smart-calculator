
#step 1: imports
from pydantic import BaseModel, ConfigDict
from datetime import datetime

#step 2: UserCreate (reg input)class
class UserCreate(BaseModel):
    username: str
    password: str

 #step 3: UserLogin(login input)
class UserLogin(BaseModel):
    username: str
    password: str

#step 4: UserOut
class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

#step 5: Token(Login response)

class Token(BaseModel):
    access_token: str
    token_type: str

#step 6: CalculateRequest + CalculateResponse
class CalculateRequest(BaseModel):
    expression: str


class CalculateResponse(BaseModel):
    expression: str
    result: float

#step 7: HistoryItem
class HistoryItem(BaseModel):
    id: int
    expression: str
    result: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
