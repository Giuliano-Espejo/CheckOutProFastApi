from sqlmodel import Session, select
from producto.model_producto import Producto
from typing import Optional, List


class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Producto]:
        return self.db.exec(select(Producto)).all()

    def get_producto_by_id(self, producto_id: int) -> Optional[Producto]:
        return self.db.get(Producto, producto_id)

    def create(self, producto: Producto) -> Producto:
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def update(self, producto: Producto) -> Producto:
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def delete(self, producto: Producto) -> None:
        self.db.delete(producto)
        self.db.commit()
