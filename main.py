from fastapi import FastAPI, HTTPException, Request
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from models import Product

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# In-memory data store for
products_list = []

# auto generate id
next_id = 1


@app.get("/products")
@limiter.limit("15/minute")
async def list_products(request: Request, skip: int = 0, limit: int = 10):
    """endpoint for list products."""
    return {
        "skip": skip,
        "limit": limit,
        "total": len(products_list),
        "products": products_list[skip:skip + limit]
    }


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """endpoint for retrieve product."""
    for product in products_list:
        if product.id == product_id:
            return {"product": product.dict()}
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
async def create_product(product: Product):
    """endpoint for create new product."""
    global next_id
    product.id = next_id
    # increment next_id
    next_id += 1
    products_list.append(product)
    return {"message": "Product created successfully", "product": product.model_dump()}


@app.put("/products/{product_id}/update")
async def update_product(product_id: int, updated_product: Product):
    """endpoint for update product."""
    for index, product in enumerate(products_list):
        if product.id == product_id:
            products_list[index] = updated_product
            return {"message": "Product updated successfully", "product": updated_product.model_dump()}
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}/delete")
async def delete_product(product_id: int):
    """endpoint for delete product."""
    for index, product in enumerate(products_list):
        if product.id == product_id:
            deleted_product = products_list.pop(index)
            return {"message": "Product deleted successfully", "deleted_product": deleted_product.dict()}
    raise HTTPException(status_code=404, detail="Product not found")

