from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.producto.model_producto import Producto

class Orden(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_email: str = Field(index=True)
    total_amount: float = Field(gt=0)

    # relación
    items: List["OrderItem"] = Relationship(back_populates="order")

    

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")

    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

    # relaciones
    order: "Orden" = Relationship(back_populates="items")
    product: "Producto" = Relationship(back_populates="order_items")