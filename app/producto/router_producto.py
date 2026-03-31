from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from core.database import get_session
from producto.model_producto import Producto
from producto.schema_producto import ProductCreate, ProductUpdate
from producto.service_producto import ProductoService

router_producto = APIRouter(prefix="/productos", tags=["Productos"])


def get_service(db: Session = Depends(get_session)) -> ProductoService:
    return ProductoService(db)


@router_producto.get("/", response_model=List[Producto])
def get_productos(service: ProductoService = Depends(get_service)):
    """Retorna todos los productos disponibles."""
    return service.get_all()


@router_producto.get("/{producto_id}", response_model=Producto)
def get_producto(producto_id: int, service: ProductoService = Depends(get_service)):
    """Retorna un producto por su ID."""
    return service.get_by_id(producto_id)


@router_producto.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED)
def create_producto(data: ProductCreate, service: ProductoService = Depends(get_service)):
    """Crea un nuevo producto."""
    return service.create(data)


@router_producto.patch("/{producto_id}", response_model=Producto)
def update_producto(
    producto_id: int,
    data: ProductUpdate,
    service: ProductoService = Depends(get_service),
):
    """Actualiza parcialmente un producto."""
    return service.update(producto_id, data)


@router_producto.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def delete_producto(producto_id: int, service: ProductoService = Depends(get_service)):
    """Elimina un producto."""
    return service.delete(producto_id)
