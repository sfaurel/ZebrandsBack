from fastapi import FastAPI

from app.routers.v1 import products

app = FastAPI(title="Products API")

app.include_router(products.router, prefix="/api/v1")
