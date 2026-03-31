from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from core.database import get_session
from orden.schema_orden import OrderCreate, OrderResponse
from orden.service_orden import OrdenService

router_orden = APIRouter(prefix="/ordenes", tags=["Ordenes"])


def get_service(db: Session = Depends(get_session)) -> OrdenService:
    return OrdenService(db)


@router_orden.get("/", response_model=List[OrderResponse])
def get_ordenes(service: OrdenService = Depends(get_service)):
    """Retorna todas las órdenes con sus items."""
    return service.get_all()


@router_orden.get("/{orden_id}", response_model=OrderResponse)
def get_orden(orden_id: int, service: OrdenService = Depends(get_service)):
    """Retorna una orden por su ID."""
    return service.get_by_id(orden_id)


@router_orden.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_orden(data: OrderCreate, service: OrdenService = Depends(get_service)):
    """
    Crea una nueva orden.

    - Valida que cada producto exista.
    - Calcula el total automáticamente usando el precio actual de cada producto.
    - Retorna la orden con sus items y el total.
    """
    return service.create(data)
