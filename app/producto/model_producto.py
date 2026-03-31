from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from orden.model_orden import OrdenItem


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str = Field(index=True)
    descripcion: Optional[str] = None
    precio: float = Field(gt=0)

    orden_items: List["OrdenItem"] = Relationship(back_populates="producto")
