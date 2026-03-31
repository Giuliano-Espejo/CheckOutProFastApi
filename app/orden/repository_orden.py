from sqlmodel import Session, select
from orden.model_orden import Orden, OrdenItem
from typing import Optional, List


class OrdenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Orden]:
        return self.db.exec(select(Orden)).all()

    def get_orden_by_id(self, orden_id: int) -> Optional[Orden]:
        return self.db.get(Orden, orden_id)

    def get_items_by_orden_id(self, orden_id: int) -> List[OrdenItem]:
        return self.db.exec(
            select(OrdenItem).where(OrdenItem.orden_id == orden_id)
        ).all()

    def create(self, orden: Orden) -> Orden:
        self.db.add(orden)
        self.db.flush()   # obtiene el id sin commitear todavía
        return orden
