from fastapi import FastAPI

from app.database.database import Base, engine
from app.database import base

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Financial Mentor API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Financial Mentor API!"
    }