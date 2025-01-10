from fastapi import APIRouter, HTTPException
from utils.database import Database

router = APIRouter(prefix="/health", tags=["health"])

# Health check endpoint
@router.get("/health")
def health_check():
    try:
        with Database.get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}