from pydantic import BaseModel
from typing import Optional, List


class OrderItemCreate(BaseModel):
    producto_id: int
    cantidad: int


class OrderCreate(BaseModel):
    user_email: str
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    producto_id: int
    producto_nombre: str
    cantidad: int
    precio_unitario: float


class OrderResponse(BaseModel):
    id: int
    user_email: str
    total: float
    preference_id: Optional[str]
    items: List[OrderItemResponse]