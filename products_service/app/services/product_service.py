from sqlmodel import Session

from app.models.product_models import ProductCreate, Product


def create_product(
    *,
    session: Session,
    product_create: ProductCreate
) -> Product:

    db_obj = Product.model_validate(product_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
