from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.income import Income
from app.models.expense import Expense
from app.models.chat_history import ChatHistory
from app.models.financial_profile import FinancialProfile


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    income = relationship(
        "Income",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    expenses = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    chat_history = relationship(
        "ChatHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    financial_profile = relationship(
        "FinancialProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )