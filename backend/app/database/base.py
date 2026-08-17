"""
Import all models here so SQLAlchemy can discover them.
"""

from app.models.user import User
from app.models.user import User
from app.models.income import Income

__all__ = ["User", "Income"]
