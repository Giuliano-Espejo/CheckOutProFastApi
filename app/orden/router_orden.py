from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from core.database import get_session
from .model_orden import Orden

router_orden = APIRouter()

@router_orden.get("/ordenes", response_model=List[Orden])
def get_ordenes(session: Session = Depends(get_session)):
    ordenes = session.exec(select(Orden)).all()
    return ordenes