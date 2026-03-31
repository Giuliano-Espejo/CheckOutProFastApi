import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

from orden.model_orden import Orden
from preference.model_preference import MercadoPago
from producto.model_producto import Producto

# FIX: forzar encoding UTF-8 al leer el .env (evita UnicodeDecodeError en Windows)
load_dotenv(encoding="utf-8")

DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "")

# FIX: quote_plus en usuario y contraseña por si contienen caracteres especiales (@, #, ó, etc.)
DATABASE_URL = (
    f"postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True)


def create_database_and_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
