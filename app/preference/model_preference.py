from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from orden.model_orden import Orden   # FIX: era "from app.orden.model_orden import Orden"


class MercadoPago(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    preference_id: Optional[str] = None
    payment_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None

    orden_id: int = Field(foreign_key="orden.id")
    orden: Optional["Orden"] = Relationship(back_populates="preference")
