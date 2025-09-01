import uuid
from sqlmodel import Field, SQLModel
from datetime import datetime


class ProductAnalyticsBase(SQLModel):
    product_id: uuid.UUID = Field(
        foreign_key="product.id", nullable=False, index=True)
    query_count: int = Field(default=0, nullable=False)
    last_queried_at: datetime | None = Field(default=None)


class ProductAnalyticsCreate(ProductAnalyticsBase):
    pass


class ProductAnalyticsPublic(ProductAnalyticsBase):
    id: uuid.UUID


class ProductAnalytics(ProductAnalyticsBase, table=True):
    __tablename__ = "product_query_logs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          primary_key=True, nullable=False)
