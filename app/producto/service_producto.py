from fastapi import HTTPException, status
from sqlmodel import Session

from producto.model_producto import Producto
from producto.repository_producto import ProductoRepository
from producto.schema_producto import ProductCreate, ProductUpdate


class ProductoService:
    def __init__(self, db: Session):
        self.repo = ProductoRepository(db)

    def get_all(self) -> list[Producto]:
        return self.repo.get_all()

    def get_by_id(self, producto_id: int) -> Producto:
        producto = self.repo.get_producto_by_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado",
            )
        return producto

    def create(self, data: ProductCreate) -> Producto:
        producto = Producto(
            nombre=data.nombre,
            descripcion=data.descripcion,
            precio=data.precio,
        )
        return self.repo.create(producto)

    def update(self, producto_id: int, data: ProductUpdate) -> Producto:
        producto = self.get_by_id(producto_id)

        if data.nombre is not None:
            producto.nombre = data.nombre
        if data.descripcion is not None:
            producto.descripcion = data.descripcion
        if data.precio is not None:
            producto.precio = data.precio

        return self.repo.update(producto)

    def delete(self, producto_id: int) -> dict:
        producto = self.get_by_id(producto_id)
        self.repo.delete(producto)
        return {"message": f"Producto {producto_id} eliminado correctamente"}
