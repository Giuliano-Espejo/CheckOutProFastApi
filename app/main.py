from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import create_database_and_table

from health.health_router import router_health
from producto.router_producto import router_producto
from orden.router_orden import router_orden
from preference.router_preference import router_preference


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_and_table()
    yield
    print("✓ Aplicación finalizada")


app = FastAPI(
    title="API con integración de Mercado Pago CheckOut Pro",
    description="API para gestión de productos, órdenes y pagos con MercadoPago",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_health, tags=["Health"])
app.include_router(router_producto, prefix="/api")
app.include_router(router_orden, prefix="/api")
app.include_router(router_preference, prefix="/api")
