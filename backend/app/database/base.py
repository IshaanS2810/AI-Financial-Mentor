"""
Import all models here so SQLAlchemy can discover them.
"""

from app.models.user import User

__all__ = ["User"]