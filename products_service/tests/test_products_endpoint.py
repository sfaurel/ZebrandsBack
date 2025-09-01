from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.services.product_service import create_product
from app.models.product_models import Product, ProductCreate


def test_create_product_existing_sku(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
    db: Session
) -> None:
    sku = "repeated_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    product_in = ProductCreate(sku=sku, name=name, price=price, brand=brand)
    create_product(session=db, product_create=product_in)
    data = {"sku": sku, "name": name, "price": price, "brand": brand}
    response = client.post(
        "/api/v1/products",
        headers=admin_account_token_headers,
        json=data,
    )
    created_product = response.json()
    assert response.status_code == 400
    assert "id" not in created_product


def test_create_product_success(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
) -> None:
    sku = "unique_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    data = {"sku": sku, "name": name, "price": price, "brand": brand}
    response = client.post(
        "/api/v1/products",
        headers=admin_account_token_headers,
        json=data,
    )
    created_product = response.json()
    assert response.status_code == 200
    assert created_product["sku"] == sku
    assert created_product["name"] == name
    assert created_product["price"] == price
    assert created_product["brand"] == brand
    assert "id" in created_product


def test_create_product_unauthorized(
    client: TestClient,
    normal_account_token_headers: dict[str, str],
) -> None:
    sku = "another_unique_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    data = {"sku": sku, "name": name, "price": price, "brand": brand}
    response = client.post(
        "/api/v1/products",
        headers=normal_account_token_headers,
        json=data,
    )
    created_product = response.json()
    assert response.status_code == 403
    assert "id" not in created_product


def test_create_product_no_auth(
    client: TestClient,
) -> None:
    sku = "yet_another_unique_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    data = {"sku": sku, "name": name, "price": price, "brand": brand}
    response = client.post(
        "/api/v1/products",
        json=data,
    )
    created_product = response.json()
    assert response.status_code == 403
    assert "id" not in created_product


def test_update_product_success(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
    db: Session
) -> None:
    sku = "update_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    product_in = ProductCreate(sku=sku, name=name, price=price, brand=brand)
    product = create_product(session=db, product_create=product_in)
    new_name = "new product name"
    new_price = 20.0
    data = {"name": new_name, "price": new_price}
    response = client.patch(
        f"/api/v1/products/{product.id}",
        headers=admin_account_token_headers,
        json=data,
    )
    updated_product = response.json()
    assert response.status_code == 200
    assert updated_product["id"] == str(product.id)
    assert updated_product["sku"] == sku
    assert updated_product["name"] == new_name
    assert updated_product["price"] == new_price
    assert updated_product["brand"] == brand


def test_update_product_not_found(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
) -> None:
    non_existent_product_id = "123e4567-e89b-12d3-a456-426614174000"
    new_name = "new product name"
    new_price = 20.0
    data = {"name": new_name, "price": new_price}
    response = client.patch(
        f"/api/v1/products/{non_existent_product_id}",
        headers=admin_account_token_headers,
        json=data,
    )
    updated_product = response.json()
    assert response.status_code == 404
    assert "id" not in updated_product


def test_update_product_unauthorized(
    client: TestClient,
    normal_account_token_headers: dict[str, str],
    db: Session
) -> None:
    sku = "update_unauth_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    product_in = ProductCreate(sku=sku, name=name, price=price, brand=brand)
    product = create_product(session=db, product_create=product_in)
    new_name = "new product name"
    new_price = 20.0
    data = {"name": new_name, "price": new_price}
    response = client.patch(
        f"/api/v1/products/{product.id}",
        headers=normal_account_token_headers,
        json=data,
    )
    updated_product = response.json()
    assert response.status_code == 403
    assert "id" not in updated_product


def test_update_product_no_auth(
    client: TestClient,
    db: Session
) -> None:
    sku = "update_no_auth_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    product_in = ProductCreate(sku=sku, name=name, price=price, brand=brand)
    product = create_product(session=db, product_create=product_in)
    new_name = "new product name"
    new_price = 20.0
    data = {"name": new_name, "price": new_price}
    response = client.patch(
        f"/api/v1/products/{product.id}",
        json=data,
    )
    updated_product = response.json()
    assert response.status_code == 403
    assert "id" not in updated_product


def test_delete_product_success(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
    db: Session
) -> None:
    sku = "delete_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    product_in = ProductCreate(sku=sku, name=name, price=price, brand=brand)
    product = create_product(session=db, product_create=product_in)
    product_id = product.id

    response = client.delete(
        f"/api/v1/products/{product.id}",
        headers=admin_account_token_headers,
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["message"] == "Product soft deleted successfully"
    result = db.exec(select(Product).where(Product.id == product_id)).first()
    assert result.is_discontinued is True


def test_delete_product_not_found(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
) -> None:
    non_existent_product_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.delete(
        f"/api/v1/products/{non_existent_product_id}",
        headers=admin_account_token_headers,
    )
    response_json = response.json()
    assert response.status_code == 404
    assert response_json["detail"] == "Product not found"


def test_delete_product_unauthorized(
    client: TestClient,
    normal_account_token_headers: dict[str, str],
    db: Session
) -> None:
    sku = "delete_unauth_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    product_in = ProductCreate(sku=sku, name=name, price=price, brand=brand)
    product = create_product(session=db, product_create=product_in)
    response = client.delete(
        f"/api/v1/products/{product.id}",
        headers=normal_account_token_headers,
    )
    response_json = response.json()
    assert response.status_code == 403
    assert response_json["detail"] == "The account doesn't have enough privileges"


def test_delete_product_no_auth(
    client: TestClient,
    db: Session
) -> None:
    sku = "delete_no_auth_sku"
    name = "product name"
    price = 10.5
    brand = "brand name"
    product_in = ProductCreate(sku=sku, name=name, price=price, brand=brand)
    product = create_product(session=db, product_create=product_in)
    response = client.delete(
        f"/api/v1/products/{product.id}",
    )
    response_json = response.json()
    assert response.status_code == 403
    assert response_json["detail"] == "Not authenticated"
