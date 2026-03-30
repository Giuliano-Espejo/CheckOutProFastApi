from fastapi import APIRouter

router_health = APIRouter()

@router_health.get("/")
def health():
    return {"status": "ok"}