from sqlmodel import Session, select, func
import pytest

from app.services.product_service import (
    create_product,
    update_product,
    delete_product
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


def test_update_product(db: Session) -> None:
    name = "Update Product"
    description = "This product will be updated"
    price = 49.99
    brand = "BrandE"
    sku = "SKU11111"

    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        brand=brand,
        sku=sku
    )

    product = create_product(session=db, product_create=product_in)

    new_name = "Updated Product"
    new_description = "This product has been updated"
    new_price = 59.99
    new_brand = "BrandF"
    new_sku = "SKU22222"

    product_update = ProductCreate(
        name=new_name,
        description=new_description,
        price=new_price,
        brand=new_brand,
        sku=new_sku
    )

    updated_product = update_product(
        session=db,
        db_product=product,
        product_in=product_update
    )
    assert updated_product.name == new_name
    assert updated_product.description == new_description
    assert updated_product.price == new_price
    assert updated_product.brand == new_brand
    assert updated_product.sku == new_sku
    assert updated_product.id == product.id


def test_update_product_invalid_price(db: Session) -> None:
    name = "Product to Update"
    description = "This product will attempt an invalid update"
    price = 69.99
    brand = "BrandG"
    sku = "SKU33333"

    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        brand=brand,
        sku=sku
    )

    product = create_product(session=db, product_create=product_in)

    new_price = -20.00

    actual_products = db.exec(select(func.count()).select_from(Product)).one()
    with pytest.raises(ValueError) as exc_info:
        product_update = ProductCreate(
            name=name,
            description=description,
            price=new_price,
            brand=brand,
            sku=sku
        )
        update_product(
            session=db,
            db_product=product,
            product_in=product_update
        )

    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products
    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('price',)
    assert errors[0]['type'] == 'greater_than'


def test_update_product_missing_name(db: Session) -> None:
    name = "Another Product to Update"
    description = "This product will attempt an invalid update"
    price = 79.99
    brand = "BrandH"
    sku = "SKU44444"

    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        brand=brand,
        sku=sku
    )

    product = create_product(session=db, product_create=product_in)

    actual_products = db.exec(select(func.count()).select_from(Product)).one()
    with pytest.raises(ValueError) as exc_info:
        product_update = ProductCreate(
            name="",
            description=description,
            price=price,
            brand=brand,
            sku=sku
        )
        update_product(
            session=db,
            db_product=product,
            product_in=product_update
        )

    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products
    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('name',)
    assert errors[0]['type'] == 'string_too_short'


def test_update_product_missing_sku(db: Session) -> None:
    name = "Yet Another Product to Update"
    description = "This product will attempt an invalid update"
    price = 89.99
    brand = "BrandI"
    sku = "SKU55555"

    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        brand=brand,
        sku=sku
    )
    product = create_product(session=db, product_create=product_in)
    actual_products = db.exec(select(func.count()).select_from(Product)).one()
    with pytest.raises(ValueError) as exc_info:
        product_update = ProductCreate(
            name=name,
            description=description,
            price=price,
            brand=brand,
            sku=""
        )
        update_product(
            session=db,
            db_product=product,
            product_in=product_update
        )
    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products
    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('sku',)
    assert errors[0]['type'] == 'string_too_short'


def test_delete_product(db: Session) -> None:
    name = "Product to Delete"
    description = "This product will be deleted"
    price = 99.99
    brand = "BrandJ"
    sku = "SKU66666"

    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        brand=brand,
        sku=sku
    )

    product = create_product(session=db, product_create=product_in)
    assert product.is_discontinued is False
    actual_products = db.exec(select(func.count()).select_from(Product)).one()

    deleted_product = delete_product(session=db, db_product=product)
    assert deleted_product.is_discontinued is True
    assert deleted_product.id == product.id
    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products


def test_delete_already_discontinued_product(db: Session) -> None:
    name = "Already Discontinued Product"
    description = "This product is already discontinued"
    price = 109.99
    brand = "BrandK"
    sku = "SKU77777"

    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        brand=brand,
        sku=sku
    )

    product = create_product(session=db, product_create=product_in)
    product.is_discontinued = True
    delete_product(session=db, db_product=product)
    assert product.is_discontinued is True
    actual_products = db.exec(select(func.count()).select_from(Product)).one()

    deleted_product = delete_product(session=db, db_product=product)
    assert deleted_product.is_discontinued is True
    assert deleted_product.id == product.id
    assert db.exec(select(func.count()).select_from(
        Product)).one() == actual_products
