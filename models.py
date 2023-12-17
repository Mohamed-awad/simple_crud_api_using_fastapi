from pydantic import BaseModel, conint
from typing import Optional


class Product(BaseModel):
    """
    product model to represent products.
    """
    id: Optional[conint(ge=1)] = None
    name: str
    description: str
    price: float
