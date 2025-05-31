# Import health router to make it available when importing from app.api
from .health import router as health_router

__all__ = ["health_router"]
