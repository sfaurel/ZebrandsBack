from fastapi import FastAPI
from app.routers.v1 import auth


app = FastAPI(title="Accounts API")

app.include_router(auth.router, prefix="/api/v1")
