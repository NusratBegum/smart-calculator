from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    calculations = relationship(
        "CalculationHistory", back_populates="user", cascade="all, delete-orphan"
    )


class CalculationHistory(Base):
    __tablename__ = "calculation_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expression = Column(String(100), nullable=False)
    result = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User", back_populates="calculations")
