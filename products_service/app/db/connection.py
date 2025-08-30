from sqlmodel import create_engine, SQLModel

from pydantic_core import MultiHostUrl
from dotenv import load_dotenv
import os

from app.models.product_models import Product

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = MultiHostUrl.build(
    scheme="postgresql+psycopg",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    path=DATABASE_NAME,
)

engine = create_engine(str(DATABASE_URL))


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
