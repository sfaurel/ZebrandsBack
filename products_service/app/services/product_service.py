from sqlmodel import Session, select

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


def update_product(
    *,
    session: Session,
    db_product: Product,
    product_in: ProductCreate
) -> Product:
    product_data = product_in.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def delete_product(*, session: Session, db_product: Product) -> Product:
    db_product.sqlmodel_update({"is_discontinued": True})
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def get_product_by_sku(*, session: Session, sku: str) -> Product | None:
    statement = select(Product).where(Product.sku == sku)
    session_product = session.exec(statement).first()
    return session_product


def get_products(*, session: Session) -> list[Product]:
    statement = select(Product).where(Product.is_discontinued == False)
    products = session.exec(statement).all()
    return products


def get_product_by_id(*, session: Session, product_id: str) -> Product | None:
    product = session.get(Product, product_id)
    return product