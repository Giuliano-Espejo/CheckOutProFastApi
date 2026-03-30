from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from ..orden.model_orden import OrderItem

class MercadoPago(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    preference_id: Optional[str] = None
    payment_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None

    # relación
    items: List["OrderItem"] = Relationship(back_populates="order")