from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.video import Video
from app.db.connection import get_db
from app.services.trend_analysis import TrendAnalysisService

router = APIRouter(prefix="/trends", tags=["trends"])

@router.get("/")
async def get_trends(
    topic: Optional[str] = Query(None, description="Topic to analyze"),
    period: str = Query("7d", description="Time period: 7d, 30d, 90d"),
    db: Session = Depends(get_db)
):
    """Get historical trends for a topic"""
    try:
        # Validate period parameter
        valid_periods = ["7d", "30d", "90d"]
        if period not in valid_periods:
            raise HTTPException(status_code=400, detail="Invalid period. Use: 7d, 30d, 90d")
        
        # Calculate date range
        days = int(period[:-1])
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query videos within date range
        query = db.query(Video).filter(
            Video.published_at >= start_date,
            Video.published_at <= end_date
        )
        
        if topic:
            query = query.filter(Video.topic.ilike(f"%{topic}%"))
        
        videos = query.all()
        
        # Group by date and calculate trends
        trends = []
        current_date = start_date
        while current_date <= end_date:
            day_videos = [v for v in videos if v.published_at.date() == current_date.date()]
            
            if day_videos:
                avg_views = sum(v.views for v in day_videos) / len(day_videos)
                # Get most common tag for the day
                all_tags = []
                for video in day_videos:
                    if video.tags:
                        all_tags.extend(video.tags)
                
                top_tag = max(set(all_tags), key=all_tags.count) if all_tags else None
                
                trends.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "avg_views": int(avg_views),
                    "top_tag": top_tag
                })
            
            current_date += timedelta(days=1)
        
        return {
            "topic": topic or "all",
            "period": period,
            "trends": trends
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics")
async def get_trending_topics(
    limit: int = Query(10, description="Number of topics to return"),
    db: Session = Depends(get_db)
):
    """Get currently trending topics"""
    try:
        # Get videos from last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Query for trending topics based on engagement
        trending_videos = db.query(Video).filter(
            Video.published_at >= week_ago
        ).order_by(Video.engagement_rate.desc()).limit(limit * 5).all()
        
        # Group by topic and calculate average engagement
        topic_stats = {}
        for video in trending_videos:
            if video.topic:
                if video.topic not in topic_stats:
                    topic_stats[video.topic] = {
                        "total_views": 0,
                        "total_engagement": 0,
                        "video_count": 0
                    }
                
                topic_stats[video.topic]["total_views"] += video.views
                topic_stats[video.topic]["total_engagement"] += video.engagement_rate
                topic_stats[video.topic]["video_count"] += 1
        
        # Calculate averages and sort
        trending_topics = []
        for topic, stats in topic_stats.items():
            avg_engagement = stats["total_engagement"] / stats["video_count"]
            trending_topics.append({
                "topic": topic,
                "avg_engagement": round(avg_engagement, 4),
                "total_views": stats["total_views"],
                "video_count": stats["video_count"]
            })
        
        # Sort by average engagement and return top results
        trending_topics.sort(key=lambda x: x["avg_engagement"], reverse=True)
        
        return {
            "trending_topics": trending_topics[:limit]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
