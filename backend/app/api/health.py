from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.db.session import get_db
from app.core.config import settings

router = APIRouter()


def check_database(db: Session) -> Dict[str, Any]:
    """Check database connection"""
    try:
        db.execute("SELECT 1")
        return {"database": "ok"}
    except Exception as e:
        return {"database": f"error: {str(e)}"}


def check_redis() -> Dict[str, str]:
    """Check Redis connection"""
    # TODO: Implement Redis health check if you're using Redis
    return {"redis": "not_configured"}


def check_services() -> Dict[str, Any]:
    """Check external services"""
    # TODO: Add checks for other external services
    return {
        "kite_connect": "ok" if settings.KITE_API_KEY and settings.KITE_API_SECRET else "not_configured"
    }


@router.get("/health", response_model=Dict[str, Any])
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies the status of the application and its dependencies.
    Returns a 200 status code if all dependencies are healthy, or a 503 if any are not.
    """
    checks = {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        **check_database(db),
        **check_redis(),
        **check_services(),
    }

    # Check if any service is not healthy
    if any(isinstance(status, str) and status.startswith("error:") for status in checks.values()):
        checks["status"] = "unhealthy"
        return JSONResponse(
            status_code=503,
            content=checks,
            headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"},
        )

    return JSONResponse(
        status_code=200,
        content=checks,
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"},
    )
