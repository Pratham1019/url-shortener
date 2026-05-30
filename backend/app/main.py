from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="URL Shortener API",
    description="A simple URL shortening service.",
    version="0.1.0",
)

app.include_router(router)