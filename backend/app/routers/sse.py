from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json
import asyncio

from app.database import get_db
from app.models.announcement import Announcement

router = APIRouter(prefix="/api/announcements", tags=["SSE"])


async def announcement_generator(db: Session):
    while True:
        announcements = db.query(Announcement).filter(
            Announcement.is_published == True
        ).order_by(Announcement.priority.desc(), Announcement.created_at.desc()).all()
        
        data = [{
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "type": a.type,
            "priority": a.priority,
            "created_at": a.created_at.isoformat() if a.created_at else None,
            "updated_at": a.updated_at.isoformat() if a.updated_at else None
        } for a in announcements]
        
        yield f"data: {json.dumps(data)}\n\n"
        await asyncio.sleep(30)


@router.get("/stream")
async def stream_announcements(db: Session = Depends(get_db)):
    return StreamingResponse(
        announcement_generator(db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
