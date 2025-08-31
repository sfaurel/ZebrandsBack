from typing import Any
from fastapi import APIRouter, Depends, HTTPException
import uuid

from app.services import product_service
from app.dependencies.dependencies import (
    SessionDep,
    admin_required
)
from app.models.product_models import (
    Product,
    ProductCreate,
    ProductPublic,
    ProductUpdate,
    ProductsPublic
)
from app.schemas.schemas import Message


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

    product = product_service.get_product_by_sku(
        session=session,
        sku=product_in.sku
    )
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


@router.patch(
    "/{product_id}",
    dependencies=[Depends(admin_required)],
    response_model=ProductPublic,
)
def update_product(
    *,
    session: SessionDep,
    product_id: uuid.UUID,
    product_in: ProductUpdate,
) -> Any:
    """
    Update existing product.
    """

    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="The product with this id does not exist in the system",
        )
    if product_in.sku:
        existing_product = product_service.get_product_by_sku(
            session=session,
            sku=product_in.sku
        )
        if existing_product and existing_product.id != product_id:
            raise HTTPException(
                status_code=409,
                detail="Product with this sku already exists"
            )

    db_product = product_service.update_product(
        session=session,
        db_product=db_product,
        product_in=product_in
    )
    return db_product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(admin_required)],
    response_model=Message
)
def delete_product(
    session: SessionDep, product_id: uuid.UUID
) -> Message:
    """
    Delete a product.
    """

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_service.delete_product(session=session, db_product=product)
    return Message(message="Product deleted successfully")


@router.get(
    "",
    response_model=ProductsPublic
)
def list_products(*, session: SessionDep) -> Any:
    """
    Retrieve products.
    """

    products = product_service.get_products(session=session)
    return ProductsPublic(data=products, count=len(products))


@router.get(
    "/{product_id}",
    response_model=ProductPublic
)
def get_product(*, session: SessionDep, product_id: uuid.UUID) -> Any:
    """
    Get product by ID.
    """

    product = product_service.get_product_by_id(
        session=session,
        product_id=product_id
    )
    if not product or product.is_discontinued:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
