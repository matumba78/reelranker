from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.db.connection import get_db

router = APIRouter(prefix="/topics", tags=["topics"])

@router.get("/")
async def get_topics(
    limit: int = 20,
    offset: int = 0,
    trending: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of topics with optional trending filter"""
    try:
        query = db.query(Topic)
        if trending is not None:
            query = query.filter(Topic.is_trending == trending)
        
        topics = query.offset(offset).limit(limit).all()
        return {"topics": topics, "total": len(topics)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{topic_id}")
async def get_topic(topic_id: str, db: Session = Depends(get_db)):
    """Get specific topic by ID"""
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        return topic
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{topic_id}/videos")
async def get_topic_videos(
    topic_id: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get videos for a specific topic"""
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        videos = topic.videos.offset(offset).limit(limit).all()
        return {"videos": videos, "total": len(videos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_topic(topic_data: dict, db: Session = Depends(get_db)):
    """Create a new topic"""
    try:
        topic = Topic(**topic_data)
        db.add(topic)
        db.commit()
        db.refresh(topic)
        return topic
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{topic_id}")
async def update_topic(topic_id: str, topic_data: dict, db: Session = Depends(get_db)):
    """Update an existing topic"""
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        for key, value in topic_data.items():
            setattr(topic, key, value)
        
        db.commit()
        db.refresh(topic)
        return topic
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{topic_id}")
async def delete_topic(topic_id: str, db: Session = Depends(get_db)):
    """Delete a topic"""
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        db.delete(topic)
        db.commit()
        return {"message": "Topic deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
