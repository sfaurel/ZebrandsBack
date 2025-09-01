from sqlmodel import Session, select

from app.models.product_analytics_models import ProductAnalyticsCreate, ProductAnalytics
from datetime import datetime, timezone
import uuid


def init_product_analytics(
    *,
    session: Session,
    product_id: str
) -> ProductAnalytics:
    db_obj = ProductAnalytics.model_validate(
        ProductAnalyticsCreate(product_id=product_id, query_count=0))
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def increment_anonymous_query_count(
    *,
    session: Session,
    product_id: uuid.UUID
) -> None:
    statement = select(ProductAnalytics).where(
        ProductAnalytics.product_id == product_id)
    product_analytics = session.exec(statement).first()
    if product_analytics:
        new_count = product_analytics.query_count + 1
        product_analytics.sqlmodel_update(
            {"query_count": new_count, "last_queried_at": datetime.now(timezone.utc)})
        session.add(product_analytics)
        session.commit()
        session.refresh(product_analytics)
    else:
        init_product_analytics(session=session, product_id=product_id)


def get_product_analytics_by_product_id(*, session: Session, product_id: uuid.UUID) -> ProductAnalytics | None:
    statement = select(ProductAnalytics).where(
        ProductAnalytics.product_id == product_id)
    product_analytics = session.exec(statement).first()
    return product_analytics
