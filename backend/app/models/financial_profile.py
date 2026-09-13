from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    age = Column(Integer, nullable=True)
    risk_tolerance = Column(String(50), nullable=False, default="Moderate")
    investment_horizon = Column(String(50), nullable=False, default="5–10 years")
    financial_goal = Column(String(100), nullable=False, default="Wealth creation")
    emergency_fund = Column(Float, nullable=False, default=0.0)
    risk_behavior = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship(
        "User",
        back_populates="financial_profile"
    )
