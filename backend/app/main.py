from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import base
from app.routers import auth
from app.config import APP_NAME, APP_VERSION
from app.routers import income

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)
app.include_router(auth.router)
app.include_router(income.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Financial Mentor API!"
    }