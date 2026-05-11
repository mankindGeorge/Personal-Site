from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse

router = APIRouter(prefix="/api/announcements", tags=["公告"])


@router.get("", response_model=List[AnnouncementResponse])
def get_all_announcements(db: Session = Depends(get_db)):
    announcements = db.query(Announcement).filter(
        Announcement.is_published == True
    ).order_by(Announcement.priority.desc(), Announcement.created_at.desc()).all()
    return announcements


@router.post("", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
def create_announcement(data: AnnouncementCreate, db: Session = Depends(get_db)):
    announcement = Announcement(**data.model_dump())
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


@router.put("/{ann_id}", response_model=AnnouncementResponse)
def update_announcement(ann_id: int, data: AnnouncementUpdate, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == ann_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(announcement, key, value)
    
    db.commit()
    db.refresh(announcement)
    return announcement


@router.delete("/{ann_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_announcement(ann_id: int, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == ann_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")
    
    db.delete(announcement)
    db.commit()
