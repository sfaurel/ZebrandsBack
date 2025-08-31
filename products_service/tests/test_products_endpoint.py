from fastapi.testclient import TestClient
from sqlmodel import Session

from app.services.product_service import create_product
from app.models.product_models import ProductCreate


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
