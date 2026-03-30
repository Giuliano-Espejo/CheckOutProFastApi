from sqlmodel import SQLModel, Field
from typing import  Optional




class Producto(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True)
    description: Optional[str] = None
    price: float = Field(gt=0)
