from sqlmodel import Session, select, func
import pytest

from app.services.product_service import (
    create_product
)
from app.models.product_models import Product, ProductCreate


def test_create_product(db: Session) -> None:
    name = "New Product"
    description = "This is a new product"
    price = 19.99
    brand = "BrandA"
    sku = "SKU12345"

    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        brand=brand,
        sku=sku
    )

    product = create_product(session=db, product_create=product_in)
    assert product.name == name
    assert product.description == description
    assert product.price == price
    assert product.brand == brand
    assert product.sku == sku


def test_create_product_invalid_price(db: Session) -> None:
    name = "Invalid Product"
    description = "This product has an invalid price"
    price = -10.00
    brand = "BrandB"
    sku = "SKU54321"
    actual_products = db.exec(select(func.count()).select_from(Product)).one()
    with pytest.raises(ValueError) as exc_info:
        product_in = ProductCreate(
            name=name,
            description=description,
            price=price,
            brand=brand,
            sku=sku
        )
        create_product(session=db, product_create=product_in)

    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products
    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('price',)
    assert errors[0]['type'] == 'greater_than'


def test_create_product_missing_name(db: Session) -> None:
    description = "This product is missing a name"
    price = 29.99
    brand = "BrandC"
    sku = "SKU67890"

    actual_products = db.exec(select(func.count()).select_from(Product)).one()
    with pytest.raises(ValueError) as exc_info:
        product_in = ProductCreate(
            name="",
            description=description,
            price=price,
            brand=brand,
            sku=sku
        )
        create_product(session=db, product_create=product_in)

    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products
    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('name',)
    assert errors[0]['type'] == 'string_too_short'


def test_create_product_missing_sku(db: Session) -> None:
    name = "No SKU Product"
    description = "This product is missing a SKU"
    price = 39.99
    brand = "BrandD"

    actual_products = db.exec(select(func.count()).select_from(Product)).one()
    with pytest.raises(ValueError) as exc_info:
        product_in = ProductCreate(
            name=name,
            description=description,
            price=price,
            brand=brand,
            sku=""
        )
        create_product(session=db, product_create=product_in)

    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products
    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('sku',)
    assert errors[0]['type'] == 'string_too_short'
