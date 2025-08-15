from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.video import Video
from app.db.connection import get_db
from app.services.youtube_fetch import YouTubeService
from app.services.trend_analysis import TrendAnalysisService

router = APIRouter(prefix="/shorts", tags=["shorts"])

@router.get("/trending")
async def get_trending_shorts(
    topic: Optional[str] = Query(None, description="Keyword filter"),
    limit: int = Query(20, description="Number of videos to return"),
    region: str = Query("IN", description="Region code"),
    db: Session = Depends(get_db)
):
    """Get trending video shorts"""
    try:
        # Mock data for development
        mock_videos = [
            {
                "video_id": "abc123",
                "title": "How the World Celebrates Indian Independence",
                "views": 9000000,
                "likes": 300000,
                "tags": ["IndependenceDay", "India", "History"],
                "hashtags": ["#IndependenceDay", "#India", "#Shorts"],
                "published_at": "2025-08-10T10:00:00Z",
                "engagement_rate": 0.035
            },
            {
                "video_id": "def456",
                "title": "The Shocking Truth About AI Technology",
                "views": 7500000,
                "likes": 250000,
                "tags": ["AI", "Technology", "Future"],
                "hashtags": ["#AI", "#Technology", "#Shorts"],
                "published_at": "2025-08-09T15:30:00Z",
                "engagement_rate": 0.032
            },
            {
                "video_id": "ghi789",
                "title": "Why Everyone is Talking About This",
                "views": 6000000,
                "likes": 200000,
                "tags": ["Trending", "Viral", "News"],
                "hashtags": ["#Trending", "#Viral", "#Shorts"],
                "published_at": "2025-08-08T12:00:00Z",
                "engagement_rate": 0.028
            }
        ]
        
        # Filter by topic if provided
        if topic:
            filtered_videos = [v for v in mock_videos if topic.lower() in v["title"].lower()]
        else:
            filtered_videos = mock_videos
        
        return {
            "topic": topic or "trending",
            "videos": filtered_videos[:limit]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_topic(request: dict):
    """Analyze a topic and provide insights"""
    try:
        topic = request.get("topic")
        limit = request.get("limit", 50)
        
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")
        
        trend_service = TrendAnalysisService()
        
        # Analyze topic patterns
        analysis = trend_service.analyze_topic(topic, limit)
        
        return {
            "topic": topic,
            "top_tags": analysis.get("top_tags", []),
            "top_hashtags": analysis.get("top_hashtags", []),
            "viral_patterns": analysis.get("viral_patterns", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{video_id}")
async def get_short(video_id: str, db: Session = Depends(get_db)):
    """Get specific video short by ID"""
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_short(video_data: dict, db: Session = Depends(get_db)):
    """Create a new video short entry"""
    try:
        video = Video(**video_data)
        db.add(video)
        db.commit()
        db.refresh(video)
        return video
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{video_id}")
async def update_short(video_id: str, video_data: dict, db: Session = Depends(get_db)):
    """Update an existing video short"""
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        for key, value in video_data.items():
            setattr(video, key, value)
        
        db.commit()
        db.refresh(video)
        return video
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{video_id}")
async def delete_short(video_id: str, db: Session = Depends(get_db)):
    """Delete a video short"""
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        db.delete(video)
        db.commit()
        return {"message": "Video deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
