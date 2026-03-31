from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from preference.model_preference import MercadoPago
    from producto.model_producto import Producto


class OrdenItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    orden_id: int = Field(foreign_key="orden.id")
    producto_id: int = Field(foreign_key="producto.id")

    cantidad: int = Field(gt=0)
    precio_unitario: float = Field(gt=0)

    orden: "Orden" = Relationship(back_populates="items")
    producto: "Producto" = Relationship(back_populates="orden_items")


class Orden(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_email: str = Field(index=True)
    total: float = Field(gt=0)

    preference: Optional["MercadoPago"] = Relationship(back_populates="orden")
    items: List["OrdenItem"] = Relationship(back_populates="orden")
