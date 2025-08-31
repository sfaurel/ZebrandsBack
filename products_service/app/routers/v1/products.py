from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from app.services import product_service
from app.dependencies.dependencies import (
    SessionDep,
    admin_required
)
from app.models.product_models import (
    Product,
    ProductCreate,
    ProductPublic,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    path="",
    dependencies=[Depends(admin_required)],
    response_model=ProductPublic
)
def create_product(*, session: SessionDep, product_in: ProductCreate) -> Any:
    """
    Create new product.
    """

    product = session.exec(select(Product).where(
        Product.sku == product_in.sku)).first()

    if product:
        raise HTTPException(
            status_code=400,
            detail="The product with this sku already exists in the system.",
        )

    product = product_service.create_product(
        session=session,
        product_create=product_in
    )
    return product
