"""
Import all models here so SQLAlchemy can discover them.
"""

from app.models.user import User
from app.models.income import Income
from app.models.expense import Expense
from app.models.chat_history import ChatHistory

__all__ = ["User", "Income", "Expense", "ChatHistory"]
