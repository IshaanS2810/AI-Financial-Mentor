from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    amount = Column(Float, nullable=False)
    source = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(255), nullable=True)

    user = relationship(
        "User",
        back_populates="income"
    )