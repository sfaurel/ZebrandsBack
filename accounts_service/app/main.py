from fastapi import FastAPI
from app.routers import v1


app = FastAPI(title="Accounts API")

app.include_router(v1.router, prefix="/api/v1")
