from sqlmodel import Session
from model_producto import Producto 
from typing import Optional, List


class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Producto]:
        return self.db.query(Producto).all()

    def create(self, producto: Producto) -> Producto:

        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def get_orden_by_id(self, producto_id: int) -> Optional[Producto]:

        return self.db.query(Producto).filter(Producto.id == producto_id).first()