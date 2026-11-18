from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db


router = APIRouter(tags=["Health"])


@router.get("/live")
async def liveness():

    return {
        "status": "alive",
        "service": "fundacion-madi-api",
    }


@router.get("/ready")
def readiness(db: Session = Depends(get_db)):

    db.execute(text("SELECT 1"))

    return {
        "status": "ready",
        "database": "connected",
    }