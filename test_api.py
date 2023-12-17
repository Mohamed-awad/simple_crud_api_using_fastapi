from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_product():
    """test create product end point"""
    product_data = {
        "name": "Test Product",
        "description": "test product",
        "price": 500.5,
    }

    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Product created successfully"
    assert "product" in response.json()
    created_product = response.json()["product"]

    # Validate the created product
    assert created_product["name"] == product_data["name"]
    assert created_product["description"] == product_data["description"]
    assert created_product["price"] == product_data["price"]


def test_list_products():
    """Test the get_products endpoint"""
    # 1. create product
    product_data = {
        "name": "Test Product",
        "description": "test product",
        "price": 500.5,
    }

    client.post("/products/", json=product_data)

    response = client.get("/products/")
    assert response.status_code == 200
    assert "products" in response.json()
    products = response.json()["products"]

    # Validate the structure of the response
    assert isinstance(products, list)
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "description" in product
        assert "price" in product

    assert response.json()["skip"] == 0
    assert response.json()["limit"] == 10


def test_get_product_detail():
    """test get product detail end point"""
    product_data = {
        "name": "Test Product",
        "description": "test product",
        "price": 500.5,
    }

    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Product created successfully"
    assert "product" in response.json()
    created_product = response.json()["product"]

    response = client.get(f"/products/{created_product['id']}")
    returned_product = response.json()["product"]
    # Validate the returned product
    assert returned_product["name"] == product_data["name"]
    assert returned_product["description"] == product_data["description"]
    assert returned_product["price"] == product_data["price"]


def test_get_product_detail_not_found():
    """test get product detail end point"""

    response = client.get("/products/100")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_update_product():
    """test update product end point"""
    product_data = {
        "name": "Test Product",
        "description": "test product",
        "price": 500.5,
    }

    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Product created successfully"
    assert "product" in response.json()
    created_product = response.json()["product"]

    product_data["name"] = "updated_name"
    response = client.put(
        f"/products/{created_product['id']}/update", json=product_data
    )
    assert response.json()["message"] == "Product updated successfully"
    updated_product = response.json()["product"]
    # Validate the updated product
    assert updated_product["name"] == "updated_name"


def test_update_product_not_exist():
    """test update product not exist end point"""
    product_data = {
        "name": "Test Product",
        "description": "test product",
        "price": 500.5,
    }

    response = client.put("/products/100/update", json=product_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_delete_product():
    """test delete product end point"""
    product_data = {
        "name": "Test Product",
        "description": "test product",
        "price": 500.5,
    }

    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Product created successfully"
    assert "product" in response.json()
    created_product = response.json()["product"]

    response = client.delete(f"/products/{created_product['id']}/delete")
    assert response.json()["message"] == "Product deleted successfully"

    response = client.get(f"/products/{created_product['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_delete_product_not_exist():
    """test delete product end point"""

    response = client.delete("/products/100/delete")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
