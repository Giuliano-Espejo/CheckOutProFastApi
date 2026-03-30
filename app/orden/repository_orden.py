from sqlmodel import Session
from app.orden.model_orden import Orden
from typing import Optional, List


class OrdenRepository:
    """
    Clase de repositorio para manejar las operaciones de la Base de Datos
    relacionadas con el modelo Orden.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Orden]:
        """Recupera todas las categorías."""
        return self.db.query(Orden).all()

    def create(self, orden: Orden) -> Orden:
        """
        Crea y persiste una nueva Orden en la base de datos.
        """
        self.db.add(orden)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def get_orden_by_id(self, orden_id: int) -> Optional[Orden]:
        """
        Obtiene una orden por su ID.
    
        """
        return self.db.query(Orden).filter(Orden.id == orden_id).first()
    
