
from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(gt=0)
   


class ProductUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    