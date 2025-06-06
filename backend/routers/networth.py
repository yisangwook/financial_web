# routers/networth.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test():
    return {"message": "It works!"}

__all__ = ["router"]
