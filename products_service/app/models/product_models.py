import uuid
from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    sku: str = Field(min_length=1, max_length=100, index=True, unique=True)
    price: float = Field(gt=0)
    brand: str = Field(min_length=1, max_length=100)
    is_discontinued: bool = Field(default=False)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    sku: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    brand: str | None = Field(default=None, min_length=1, max_length=100)
    is_discontinued: bool | None = Field(default=None)


class ProductPublic(ProductBase):
    id: uuid.UUID


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int


class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
