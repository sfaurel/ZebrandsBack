from typing import Any
from fastapi import APIRouter, HTTPException, Depends
import uuid

from app.models.product_analytics_models import ProductAnalyticsPublic
from app.services import product_analytics_service
from app.dependencies.dependencies import (
    SessionDep,
    admin_required
)


router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "/{product_id}/analytics",
    response_model=ProductAnalyticsPublic,
    dependencies=[Depends(admin_required)]
)
def get_product_analytics(
    *,
    session: SessionDep,
    product_id: uuid.UUID
) -> Any:
    """
    Get product analytics by ID.
    """

    product_analytics = product_analytics_service.get_product_analytics_by_product_id(
        session=session,
        product_id=product_id
    )
    if not product_analytics:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_analytics
