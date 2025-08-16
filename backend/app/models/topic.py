from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

# Import Base from video model to use single Base class
from .video import Base

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Topic metrics
    total_videos = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    avg_engagement_rate = Column(Float, default=0.0)
    
    # Trending analysis
    is_trending = Column(Boolean, default=False)
    trend_score = Column(Float, default=0.0)
    trend_direction = Column(String(20))  # "up", "down", "stable"
    
    # Content analysis
    top_tags = Column(JSON, default=list)
    top_hashtags = Column(JSON, default=list)
    viral_patterns = Column(JSON, default=list)
    
    # Category and classification
    category = Column(String(100))
    keywords = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_trending_at = Column(DateTime)
    
    # Relationships - commented out for now to avoid circular imports
    # videos = relationship("Video", back_populates="topic_relation")
    
    def __repr__(self):
        return f"<Topic(id={self.id}, name='{self.name}', trend_score={self.trend_score})>"
    
    def calculate_trend_score(self):
        """Calculate trend score based on recent activity"""
        # This would be implemented based on recent video performance
        # For now, return a placeholder
        return self.trend_score
    
    def update_metrics(self):
        """Update topic metrics based on associated videos"""
        if not self.videos:
            return
        
        self.total_videos = len(self.videos)
        self.total_views = sum(video.views for video in self.videos)
        self.total_likes = sum(video.likes for video in self.videos)
        
        if self.total_videos > 0:
            self.avg_engagement_rate = sum(video.engagement_rate for video in self.videos) / self.total_videos
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "total_videos": self.total_videos,
            "total_views": self.total_views,
            "total_likes": self.total_likes,
            "avg_engagement_rate": self.avg_engagement_rate,
            "is_trending": self.is_trending,
            "trend_score": self.trend_score,
            "trend_direction": self.trend_direction,
            "top_tags": self.top_tags,
            "top_hashtags": self.top_hashtags,
            "viral_patterns": self.viral_patterns,
            "category": self.category,
            "keywords": self.keywords,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_trending_at": self.last_trending_at.isoformat() if self.last_trending_at else None
        }
