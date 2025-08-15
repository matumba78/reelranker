from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from collections import Counter

logger = logging.getLogger(__name__)

class TrendAnalysisService:
    def __init__(self):
        self.trending_threshold = 0.02  # 2% engagement rate
        self.viral_threshold = 0.05     # 5% engagement rate
    
    def analyze_topic(self, topic: str, limit: int = 50) -> Dict:
        """Analyze a topic and provide insights"""
        try:
            # This would typically query the database for videos with this topic
            # For now, return mock data
            return {
                "top_tags": [
                    {"tag": "IndependenceDay", "score": 0.92},
                    {"tag": "Freedom", "score": 0.87},
                    {"tag": "History", "score": 0.85},
                    {"tag": "India", "score": 0.82},
                    {"tag": "Celebration", "score": 0.78}
                ],
                "top_hashtags": [
                    {"hashtag": "#IndependenceDay", "score": 0.95},
                    {"hashtag": "#JaiHind", "score": 0.89},
                    {"hashtag": "#India", "score": 0.87},
                    {"hashtag": "#Freedom", "score": 0.84},
                    {"hashtag": "#Shorts", "score": 0.82}
                ],
                "viral_patterns": [
                    "How the World Celebrates X",
                    "The Shocking Truth About X",
                    "Why X is Trending Right Now",
                    "The Untold Story of X",
                    "X in 60 Seconds"
                ],
                "trending_keywords": [
                    "independence", "freedom", "celebration", "history", "patriotism"
                ]
            }
        except Exception as e:
            logger.error(f"Error analyzing topic {topic}: {e}")
            return {}
    
    def get_trending_topics(self, days: int = 7, limit: int = 10) -> List[Dict]:
        """Get currently trending topics"""
        try:
            # This would query the database for trending topics
            # For now, return mock data
            return [
                {
                    "topic": "history of indian independence",
                    "trend_score": 0.95,
                    "video_count": 150,
                    "avg_engagement": 0.045,
                    "trend_direction": "up"
                },
                {
                    "topic": "cricket world cup 2024",
                    "trend_score": 0.88,
                    "video_count": 200,
                    "avg_engagement": 0.038,
                    "trend_direction": "up"
                },
                {
                    "topic": "ai technology trends",
                    "trend_score": 0.82,
                    "video_count": 120,
                    "avg_engagement": 0.035,
                    "trend_direction": "stable"
                }
            ][:limit]
        except Exception as e:
            logger.error(f"Error getting trending topics: {e}")
            return []
    
    def analyze_viral_patterns(self, videos: List[Dict]) -> List[str]:
        """Analyze viral patterns from a list of videos"""
        try:
            patterns = []
            titles = [video.get('title', '') for video in videos]
            
            # Extract common patterns
            for title in titles:
                # Look for "How to" patterns
                if title.lower().startswith('how to'):
                    patterns.append("How to X")
                
                # Look for "The X of Y" patterns
                if 'the ' in title.lower() and ' of ' in title.lower():
                    patterns.append("The X of Y")
                
                # Look for question patterns
                if any(word in title.lower() for word in ['why', 'how', 'what', 'when']):
                    patterns.append("Question-based titles")
                
                # Look for number patterns
                if any(char.isdigit() for char in title):
                    patterns.append("Number-based titles")
            
            # Count and return most common patterns
            pattern_counts = Counter(patterns)
            return [pattern for pattern, count in pattern_counts.most_common(5)]
            
        except Exception as e:
            logger.error(f"Error analyzing viral patterns: {e}")
            return []
    
    def calculate_trend_score(self, topic: str, time_period: int = 7) -> float:
        """Calculate trend score for a topic"""
        try:
            # This would analyze recent video performance for the topic
            # For now, return a mock score
            base_score = 0.5
            
            # Mock factors that would affect trend score
            factors = {
                "recent_activity": 0.2,
                "engagement_rate": 0.15,
                "growth_rate": 0.1,
                "viral_potential": 0.05
            }
            
            trend_score = base_score + sum(factors.values())
            return min(trend_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating trend score for {topic}: {e}")
            return 0.0
    
    def get_topic_insights(self, topic: str) -> Dict:
        """Get comprehensive insights for a topic"""
        try:
            # This would aggregate data from multiple sources
            return {
                "topic": topic,
                "trend_score": self.calculate_trend_score(topic),
                "viral_potential": 0.85,
                "competition_level": "medium",
                "best_posting_times": ["10:00", "14:00", "18:00"],
                "recommended_duration": "30-60 seconds",
                "top_performing_tags": ["#Shorts", "#Viral", "#Trending"],
                "audience_demographics": {
                    "age_groups": ["18-24", "25-34"],
                    "interests": ["education", "history", "politics"]
                }
            }
        except Exception as e:
            logger.error(f"Error getting topic insights for {topic}: {e}")
            return {}
    
    def predict_trend_direction(self, topic: str) -> str:
        """Predict if a topic trend is going up, down, or stable"""
        try:
            # This would analyze historical data and current momentum
            # For now, return mock prediction
            predictions = ["up", "down", "stable"]
            import random
            return random.choice(predictions)
            
        except Exception as e:
            logger.error(f"Error predicting trend direction for {topic}: {e}")
            return "stable"
