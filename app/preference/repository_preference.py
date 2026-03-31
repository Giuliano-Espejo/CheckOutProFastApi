from sqlmodel import Session, select
from preference.model_preference import MercadoPago
from typing import Optional, List


class MercadoPagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[MercadoPago]:
        return self.db.exec(select(MercadoPago)).all()

    def get_by_orden_id(self, orden_id: int) -> Optional[MercadoPago]:
        return self.db.exec(
            select(MercadoPago).where(MercadoPago.orden_id == orden_id)
        ).first()

    def get_by_id(self, mercado_id: int) -> Optional[MercadoPago]:
        return self.db.get(MercadoPago, mercado_id)

    def create(self, mercado: MercadoPago) -> MercadoPago:
        self.db.add(mercado)
        self.db.commit()
        self.db.refresh(mercado)
        return mercado

    def update(self, mercado: MercadoPago) -> MercadoPago:
        self.db.add(mercado)
        self.db.commit()
        self.db.refresh(mercado)
        return mercado
