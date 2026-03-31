from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from core.database import get_session
from preference.schema_preference import PaymentResponse
from preference.service_preference import MercadoPagoService

router_preference = APIRouter(prefix="/ordenes", tags=["Pagos - MercadoPago"])


def get_service(db: Session = Depends(get_session)) -> MercadoPagoService:
    return MercadoPagoService(db)


@router_preference.post(
    "/{orden_id}/preference",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_preference(orden_id: int, service: MercadoPagoService = Depends(get_service)):
    """
    Crea una preferencia de pago en MercadoPago para una orden existente.

    Retorna las URLs de pago (producción y sandbox).
    """
    return service.create_preference(orden_id)

