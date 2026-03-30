from sqlmodel import Session
from model_preference import MercadoPago
from typing import Optional, List


class MercadoPagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[MercadoPago]:
        return self.db.query(MercadoPago).all()

    def create(self, mercado: MercadoPago) -> MercadoPago:

        self.db.add(mercado)
        self.db.commit()
        self.db.refresh(mercado)
        return mercado

    def get_orden_by_id(self, mercado_id: int) -> Optional[MercadoPago]:

        return self.db.query(MercadoPago).filter(MercadoPago.id == mercado_id).first()