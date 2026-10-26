from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, CalculationHistory
from app.schemas import CalculateRequest, CalculateResponse, HistoryItem
from app.auth import get_current_user
from app.calculator import Calculator, CalculationError

router = APIRouter()


@router.post("/calculate", response_model=CalculateResponse)
def calculate(
    request: CalculateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calc = Calculator()
    try:
        result = calc.evaluate(request.expression)
    except CalculationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    row = CalculationHistory(
        user_id=current_user.id,
        expression=request.expression,
        result=result,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return CalculateResponse(expression=row.expression, result=row.result)


@router.get("/history", response_model=List[HistoryItem])
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(CalculationHistory)
        .filter(CalculationHistory.user_id == current_user.id)
        .order_by(CalculationHistory.created_at.desc(), CalculationHistory.id.desc())
        .all()
    )
    return rows
