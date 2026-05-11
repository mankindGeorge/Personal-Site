from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse

router = APIRouter(prefix="/api/docs", tags=["文档"])


@router.get("", response_model=List[DocumentResponse])
def get_all_docs(db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.is_published == True).order_by(Document.order_index).all()
    return docs


@router.get("/{slug}", response_model=DocumentResponse)
def get_doc_by_slug(slug: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.slug == slug, Document.is_published == True).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    return doc


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_doc(doc_data: DocumentCreate, db: Session = Depends(get_db)):
    existing = db.query(Document).filter(Document.slug == doc_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug 已存在")
    
    doc = Document(**doc_data.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.put("/{doc_id}", response_model=DocumentResponse)
def update_doc(doc_id: int, doc_data: DocumentUpdate, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    if doc_data.slug:
        existing = db.query(Document).filter(
            Document.slug == doc_data.slug, 
            Document.id != doc_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug 已存在")
    
    update_data = doc_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(doc, key, value)
    
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doc(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    db.delete(doc)
    db.commit()
