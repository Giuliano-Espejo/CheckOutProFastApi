# CheckOutPro FastAPI 🛒

API REST construida con **FastAPI** y **SQLModel** para gestión de productos, órdenes de compra y pagos integrados con **MercadoPago Checkout Pro**.

---

## Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) — framework web
- [SQLModel](https://sqlmodel.tiangolo.com/) — ORM (basado en SQLAlchemy + Pydantic)
- [PostgreSQL](https://www.postgresql.org/) — base de datos
- [MercadoPago SDK](https://github.com/mercadopago/sdk-python) — integración de pagos
- [python-dotenv](https://github.com/theskumar/python-dotenv) — variables de entorno

---

## Instalación y configuración

### 1. Clonar el repositorio y crear el entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crear (o editar) el archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost #local
DB_PORT=5432
DB_NAME=nombre_de_tu_db

# MercadoPago
MERCADOPAGO_ACCESS_TOKEN=tu_access_token

# Frontend (usado en las back_urls de MP)
FRONTEND_URL=http://localhost:5173
```

> ⚠️ Guardar el `.env`.

### 4. Levantar el servidor

```bash
python -m fastapi dev app/main.py
```

La API queda disponible en `http://localhost:8000`.  
La documentación interactiva en `http://localhost:8000/docs`.

---

## Endpoints

### Health
| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Estado del servidor |

### Productos
| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/productos` | Listar todos los productos |
| `GET` | `/api/productos/{id}` | Obtener producto por ID |
| `POST` | `/api/productos` | Crear producto |
| `PATCH` | `/api/productos/{id}` | Actualizar producto (parcial) |
| `DELETE` | `/api/productos/{id}` | Eliminar producto |

### Órdenes
| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/ordenes` | Listar todas las órdenes |
| `GET` | `/api/ordenes/{id}` | Obtener orden por ID |
| `POST` | `/api/ordenes` | Crear orden |

### Pagos — MercadoPago
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/ordenes/{id}/preference` | Crear preferencia de pago en MP |

---

## Flujo de uso

```
1. Crear productos         →  POST /api/productos
2. Crear una orden         →  POST /api/ordenes
3. Generar preferencia MP  →  POST /api/ordenes/{id}/preference
                                 └─ retorna init_point (URL de pago)
4. Usuario paga en MP      →  MercadoPago redirige al frontend
```

### Ejemplo: Crear una orden

```json
POST /api/ordenes
{
  "user_email": "cliente@ejemplo.com",
  "items": [
    { "producto_id": 1, "cantidad": 2 },
    { "producto_id": 3, "cantidad": 1 }
  ]
}
```

El servicio valida que cada producto exista, calcula el total automáticamente y devuelve la orden completa con sus items.

### Ejemplo: Crear preferencia de pago

```json
POST /api/ordenes/1/preference

// Respuesta:
{
  "order_id": 1,
  "preference_id": "123456789-abc...",
  "payment_url": "https://www.mercadopago.com.ar/checkout/v1/redirect?...",
  "sandbox_payment_url": "https://sandbox.mercadopago.com.ar/checkout/..."
}
```

---

## Notas

- Las tablas se crean automáticamente al iniciar la aplicación si no existen.
- En desarrollo, usar el `sandbox_payment_url` para probar pagos sin dinero real.
