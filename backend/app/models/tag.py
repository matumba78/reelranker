from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

# Import Base from video model to use single Base class
from .video import Base

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False, index=True)
    
    # Tag metrics
    usage_count = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    avg_engagement_rate = Column(Float, default=0.0)
    
    # Trending analysis
    is_trending = Column(Boolean, default=False)
    trend_score = Column(Float, default=0.0)
    
    # Category and classification
    category = Column(String(100))
    related_tags = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}', usage_count={self.usage_count})>"
    
    def increment_usage(self):
        """Increment usage count and update last used timestamp"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
    
    def calculate_trend_score(self):
        """Calculate trend score based on recent usage"""
        # This would be implemented based on recent usage patterns
        # For now, return a placeholder
        return self.trend_score
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "usage_count": self.usage_count,
            "total_views": self.total_views,
            "avg_engagement_rate": self.avg_engagement_rate,
            "is_trending": self.is_trending,
            "trend_score": self.trend_score,
            "category": self.category,
            "related_tags": self.related_tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None
        }
