from fastapi import HTTPException, status
from sqlmodel import Session

from orden.model_orden import Orden, OrdenItem
from orden.repository_orden import OrdenRepository
from orden.schema_orden import OrderCreate, OrderResponse, OrderItemResponse
from producto.repository_producto import ProductoRepository


class OrdenService:
    def __init__(self, db: Session):
        self.db = db
        self.orden_repo = OrdenRepository(db)
        self.producto_repo = ProductoRepository(db)

    def get_all(self) -> list[OrderResponse]:
        ordenes = self.orden_repo.get_all()
        return [self._build_response(o) for o in ordenes]

    def get_by_id(self, orden_id: int) -> OrderResponse:
        orden = self.orden_repo.get_orden_by_id(orden_id)
        if not orden:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Orden con id {orden_id} no encontrada",
            )
        return self._build_response(orden)

    def create(self, data: OrderCreate) -> OrderResponse:
        # 1. Validar productos y calcular total
        item_data: list[tuple] = []
        total = 0.0

        for item in data.items:
            producto = self.producto_repo.get_producto_by_id(item.producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con id {item.producto_id} no encontrado",
                )
            subtotal = producto.precio * item.cantidad
            total += subtotal
            item_data.append((item, producto))

        # 2. Crear la Orden (flush para obtener el id)
        orden = Orden(
            user_email=data.user_email,
            total=round(total, 2),
        )
        self.orden_repo.create(orden)   # hace flush internamente

        # 3. Crear los OrdenItem vinculados
        orden_items: list[tuple] = []
        for item, producto in item_data:
            orden_item = OrdenItem(
                orden_id=orden.id,
                producto_id=producto.id,
                cantidad=item.cantidad,
                precio_unitario=producto.precio,
            )
            self.db.add(orden_item)
            orden_items.append((orden_item, producto))

        # 4. Commit final y refresh
        self.db.commit()
        self.db.refresh(orden)
        for orden_item, _ in orden_items:
            self.db.refresh(orden_item)

        # 5. Construir respuesta
        return OrderResponse(
            id=orden.id,
            user_email=orden.user_email,
            total=orden.total,
            preference_id=None,
            items=[
                OrderItemResponse(
                    id=oi.id,
                    producto_id=oi.producto_id,
                    producto_nombre=p.nombre,
                    cantidad=oi.cantidad,
                    precio_unitario=oi.precio_unitario,
                )
                for oi, p in orden_items
            ],
        )

    # ── helpers ────────────────────────────────────────────────────────────────
    def _build_response(self, orden: Orden) -> OrderResponse:
        """Construye un OrderResponse cargando items y productos."""
        items_db = self.orden_repo.get_items_by_orden_id(orden.id)

        item_responses: list[OrderItemResponse] = []
        for oi in items_db:
            producto = self.producto_repo.get_producto_by_id(oi.producto_id)
            item_responses.append(
                OrderItemResponse(
                    id=oi.id,
                    producto_id=oi.producto_id,
                    producto_nombre=producto.nombre if producto else "–",
                    cantidad=oi.cantidad,
                    precio_unitario=oi.precio_unitario,
                )
            )

        # buscar preference_id si existe
        from preference.repository_preference import MercadoPagoRepository
        mp = MercadoPagoRepository(self.db).get_by_orden_id(orden.id)

        return OrderResponse(
            id=orden.id,
            user_email=orden.user_email,
            total=orden.total,
            preference_id=mp.preference_id if mp else None,
            items=item_responses,
        )
