from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
import uuid

from app.services import product_service
from app.dependencies.dependencies import (
    SessionDep,
    admin_required,
    get_current_token_data
)
from app.models.product_models import (
    Product,
    ProductCreate,
    ProductPublic,
    ProductUpdate,
    ProductsPublic
)
from app.schemas.schemas import Message, AuditEvent
from app.services.event_publisher_service import emit_crud_event


router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    path="",
    dependencies=[Depends(admin_required)],
    response_model=ProductPublic
)
def create_product(
    *,
    session: SessionDep,
    product_in: ProductCreate,
    token_data: dict = Depends(get_current_token_data)
) -> ProductPublic:
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
    event = AuditEvent(
        user=token_data.get("sub"),
        action="create",
        timestamp=datetime.now(timezone.utc),
        model="Product",
        record_id=product.id,
        changes=get_changes(original=None, updated=product)
    )
    emit_crud_event(event)
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
    token_data: dict = Depends(get_current_token_data)
) -> Any:
    """
    Update existing product.
    """

    db_product = session.get(Product, product_id)
    original_db_product = db_product.model_copy()
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

    original_db_product = db_product.model_copy()
    db_product = product_service.update_product(
        session=session,
        db_product=db_product,
        product_in=product_in
    )
    event = AuditEvent(
        user=token_data.get("sub"),
        action="update",
        timestamp=datetime.now(timezone.utc),
        model="Product",
        record_id=db_product.id,
        changes=get_changes(original=original_db_product, updated=db_product)
    )
    emit_crud_event(event)
    return db_product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(admin_required)],
    response_model=Message
)
def delete_product(
    session: SessionDep,
    product_id: uuid.UUID,
    token_data: dict = Depends(get_current_token_data)
) -> Message:
    """
    Delete a product.
    """

    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    original_db_product = db_product.model_copy()
    db_product = product_service.delete_product(
        session=session, db_product=db_product)

    event = AuditEvent(
        user=token_data.get("sub"),
        action="soft delete",
        timestamp=datetime.now(timezone.utc),
        model="Product",
        record_id=db_product.id,
        changes=get_changes(original=original_db_product, updated=db_product)
    )
    emit_crud_event(event)
    return Message(message="Product soft deleted successfully")


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


def get_changes(*, original: Product | None, updated: Product) -> dict:
    changes = {}
    for field, updated_value in updated.model_dump().items():
        original_value = getattr(original, field) if original else None
        changes[field] = {"old": original_value, "new": updated_value}
    return changes
