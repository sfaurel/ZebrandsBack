from fastapi import FastAPI
import threading
from contextlib import asynccontextmanager

from app.routers import health
from app.services.notification_services import consume


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=consume, daemon=True)
    thread.start()
    print("Worker thread started")
    yield
    print("App shutting down")

app = FastAPI(
    title="Notification service",
    lifespan=lifespan
)

app.include_router(health.router, prefix="")
