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
        youtube_service = YouTubeService()
        
        # Use real YouTube API to get trending videos
        if topic:
            # Search for videos with the topic
            videos = youtube_service.search_shorts(topic, limit, region)
        else:
            # Get trending videos
            videos = youtube_service.get_trending_videos(region, "1")  # Category 1 = Film & Animation
        
        # Get detailed information for the videos
        if videos:
            video_ids = [video['video_id'] for video in videos[:limit]]
            detailed_videos = youtube_service.get_video_details(video_ids)
            
            # Format the response
            formatted_videos = []
            for video in detailed_videos:
                engagement_rate = 0.0
                if video.get('views', 0) > 0:
                    engagement_rate = (video.get('likes', 0) + video.get('comments', 0)) / video.get('views', 1)
                
                formatted_video = {
                    "video_id": video['video_id'],
                    "title": video['title'],
                    "views": video.get('views', 0),
                    "likes": video.get('likes', 0),
                    "tags": [topic] if topic else [],
                    "hashtags": ["#Shorts", "#Viral", "#Trending"],
                    "published_at": video['published_at'],
                    "engagement_rate": round(engagement_rate, 4),
                    "channel_title": video['channel_title'],
                    "thumbnail_url": video['thumbnail_url']
                }
                formatted_videos.append(formatted_video)
            
            return {
                "topic": topic or "trending",
                "videos": formatted_videos,
                "source": "youtube_api"
            }
        else:
            # Fallback to mock data if YouTube API fails
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
                }
            ]
            return {
                "topic": topic or "trending",
                "videos": mock_videos[:limit],
                "source": "mock_data"
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
