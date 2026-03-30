from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from health import health_router
from orden.router_orden import router_orden

from core.database import create_database_and_table
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicio (startup)
    create_database_and_table()  # Crear la base de datos y tablas al iniciar la aplicación
    yield
    # Código de finalización (shutdown)
    print("✓ Aplicación finalizada")

app = FastAPI(title="API con integracion de Mercado Pago CheckOut Pro", lifespan=lifespan)

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


app.include_router(router=health_router.router_health, prefix="/health", tags=["health"])
app.include_router(router_orden, prefix="/orden",tags=["Orden"])
