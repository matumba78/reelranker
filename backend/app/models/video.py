from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

# Use a single Base class for all models
Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    video_id = Column(String, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    channel_id = Column(String, nullable=False)
    channel_title = Column(String(200))
    
    # Video metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    # Calculated metrics
    engagement_rate = Column(Float, default=0.0)
    viral_score = Column(Float, default=0.0)
    
    # Content analysis
    topic = Column(String(200), index=True)
    category = Column(String(100))
    tags = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    
    # Video metadata
    duration = Column(Integer)  # in seconds
    thumbnail_url = Column(String(500))
    video_url = Column(String(500))
    
    # Timestamps
    published_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Processing flags
    is_processed = Column(Boolean, default=False)
    is_trending = Column(Boolean, default=False)
    is_viral = Column(Boolean, default=False)
    
    # Relationships - commented out for now to avoid circular imports
    # topic_relation = relationship("Topic", back_populates="videos")
    
    def __repr__(self):
        return f"<Video(id={self.id}, title='{self.title[:50]}...', views={self.views})>"
    
    def calculate_engagement_rate(self):
        """Calculate engagement rate based on likes, comments, shares vs views"""
        if self.views == 0:
            return 0.0
        
        total_engagement = self.likes + self.comments + self.shares
        self.engagement_rate = total_engagement / self.views
        return self.engagement_rate
    
    def is_viral_content(self):
        """Determine if video is viral based on thresholds"""
        return (
            self.views >= 1000000 or
            self.engagement_rate >= 0.05 or
            self.likes >= 50000
        )
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "video_id": self.video_id,
            "title": self.title,
            "description": self.description,
            "channel_id": self.channel_id,
            "channel_title": self.channel_title,
            "views": self.views,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "comments": self.comments,
            "shares": self.shares,
            "engagement_rate": self.engagement_rate,
            "viral_score": self.viral_score,
            "topic": self.topic,
            "category": self.category,
            "tags": self.tags,
            "hashtags": self.hashtags,
            "duration": self.duration,
            "thumbnail_url": self.thumbnail_url,
            "video_url": self.video_url,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_processed": self.is_processed,
            "is_trending": self.is_trending,
            "is_viral": self.is_viral
        }
