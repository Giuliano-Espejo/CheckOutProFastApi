import os
import mercadopago
from fastapi import HTTPException, status
from sqlmodel import Session
from datetime import datetime

from orden.repository_orden import OrdenRepository
from preference.model_preference import MercadoPago
from preference.repository_preference import MercadoPagoRepository
from preference.schema_preference import PaymentResponse


class MercadoPagoService:
    def __init__(self, db: Session):
        self.db = db
        self.orden_repo = OrdenRepository(db)
        self.mp_repo = MercadoPagoRepository(db)
        self.sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_ACCESS_TOKEN", ""))

    def create_preference(self, orden_id: int) -> PaymentResponse:
        # 1. Verificar que la orden exista
        orden = self.orden_repo.get_orden_by_id(orden_id)
        if not orden:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Orden con id {orden_id} no encontrada",
            )

        # 2. Verificar que no tenga ya una preferencia activa
        existing = self.mp_repo.get_by_orden_id(orden_id)
        if existing and existing.preference_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta orden ya tiene una preferencia de pago creada",
            )

        # 3. Construir items para MercadoPago
        items_db = self.orden_repo.get_items_by_orden_id(orden_id)
        if not items_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La orden no tiene items",
            )

        mp_items = [
            {
                "title": f"Producto #{oi.producto_id}",
                "quantity": oi.cantidad,
                "unit_price": oi.precio_unitario,
                "currency_id": "ARS",
            }
            for oi in items_db
        ]

        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

        preference_data = {
            "items": mp_items,
            "payer": {"email": orden.user_email},
            "back_urls": {
                "success": f"{frontend_url}/checkout/success",
                "failure": f"{frontend_url}/checkout/failure",
                "pending": f"{frontend_url}/checkout/pending",
            },
            "external_reference": str(orden.id),
            #Excluimos el efectivo
            "payment_methods": {
                "excluded_payment_types": [
                    {"id": "ticket"}
                ]
            },
        }

        # 4. Llamar a la API de MercadoPago
        result = self.sdk.preference().create(preference_data)
        response = result.get("response", {})

        if result.get("status") not in (200, 201):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error al crear preferencia en MercadoPago: {response}",
            )

        # 5. Persistir el registro
        mp_record = MercadoPago(
            orden_id=orden.id,
            preference_id=response["id"],
            created_at=datetime.now(),
        )
        self.mp_repo.create(mp_record)

        return PaymentResponse(
            order_id=orden.id,
            preference_id=response["id"],
            payment_url=response["init_point"],
            sandbox_payment_url=response.get("sandbox_init_point"),
        )


