"""Entry point for the AI Financial Mentor FastAPI application."""

from fastapi import FastAPI

app = FastAPI(title="AI Financial Mentor API", version="1.0.0")


@app.get("/")
def root() -> dict[str, str]:
    """Return a basic welcome message for the API root."""
    return {"message": "Welcome to AI Financial Mentor API"}


# Future application startup configuration will be added here.
# Future routers will be registered here.
