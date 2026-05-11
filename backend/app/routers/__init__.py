from app.routers.docs import router as docs_router
from app.routers.announcements import router as announcements_router
from app.routers.auth import router as auth_router
from app.routers.sse import router as sse_router

__all__ = ["docs_router", "announcements_router", "auth_router", "sse_router"]
