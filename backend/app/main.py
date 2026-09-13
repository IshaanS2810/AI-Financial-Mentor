from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine
from app.database import base
from app.config import APP_NAME, APP_VERSION
from app.routers import (
    auth,
    income,
    expense,
    dashboard,
    chatbot,
    profile,
    recommendations,
)

# Create all database tables (safely creates missing tables without dropping existing ones)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router)
app.include_router(income.router)
app.include_router(expense.router)
app.include_router(dashboard.router)
app.include_router(chatbot.router)
app.include_router(profile.router)
app.include_router(recommendations.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Financial Mentor API!"
    }