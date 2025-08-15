import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class HashtagExtractor:
    def __init__(self):
        self.common_hashtags = [
            "#Shorts", "#Viral", "#Trending", "#FYP", "#YouTube", "#TikTok",
            "#Like", "#Comment", "#Share", "#Follow", "#Subscribe",
            "#New", "#Latest", "#Now", "#Today", "#2024", "#2025"
        ]
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        try:
            # Find all hashtags using regex
            hashtag_pattern = r'#\w+'
            hashtags = re.findall(hashtag_pattern, text)
            
            # Remove duplicates and return
            return list(set(hashtags))
            
        except Exception as e:
            logger.error(f"Error extracting hashtags: {e}")
            return []
    
    def extract_tags(self, text: str) -> List[str]:
        """Extract tags (words without #) from text"""
        try:
            # Remove hashtags first
            text_without_hashtags = re.sub(r'#\w+', '', text)
            
            # Extract words (potential tags)
            words = re.findall(r'\b\w+\b', text_without_hashtags.lower())
            
            # Filter out common words and short words
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
            }
            
            tags = [word for word in words if word not in stop_words and len(word) > 2]
            
            # Remove duplicates and return
            return list(set(tags))
            
        except Exception as e:
            logger.error(f"Error extracting tags: {e}")
            return []
    
    def suggest_hashtags(self, topic: str, count: int = 10) -> List[str]:
        """Suggest relevant hashtags for a topic"""
        try:
            suggested_hashtags = []
            
            # Add topic-specific hashtag
            topic_hashtag = "#" + topic.replace(" ", "").title()
            suggested_hashtags.append(topic_hashtag)
            
            # Add common hashtags
            suggested_hashtags.extend(self.common_hashtags[:5])
            
            # Generate topic-related hashtags
            topic_words = topic.lower().split()
            for word in topic_words:
                if len(word) > 3:  # Only use words longer than 3 characters
                    hashtag = "#" + word.title()
                    if hashtag not in suggested_hashtags:
                        suggested_hashtags.append(hashtag)
            
            # Add some trending hashtags based on topic
            trending_hashtags = self._get_trending_hashtags(topic)
            suggested_hashtags.extend(trending_hashtags)
            
            # Remove duplicates and return requested count
            unique_hashtags = list(set(suggested_hashtags))
            return unique_hashtags[:count]
            
        except Exception as e:
            logger.error(f"Error suggesting hashtags: {e}")
            return self.common_hashtags[:count]
    
    def analyze_hashtag_performance(self, hashtags: List[str]) -> List[Dict]:
        """Analyze hashtag performance (mock implementation)"""
        try:
            performance_data = []
            
            for hashtag in hashtags:
                # Mock performance metrics
                performance_data.append({
                    "hashtag": hashtag,
                    "reach_score": self._calculate_reach_score(hashtag),
                    "engagement_score": self._calculate_engagement_score(hashtag),
                    "trending_score": self._calculate_trending_score(hashtag),
                    "recommendation": self._get_hashtag_recommendation(hashtag)
                })
            
            # Sort by overall performance
            performance_data.sort(key=lambda x: x["reach_score"] + x["engagement_score"], reverse=True)
            
            return performance_data
            
        except Exception as e:
            logger.error(f"Error analyzing hashtag performance: {e}")
            return []
    
    def _get_trending_hashtags(self, topic: str) -> List[str]:
        """Get trending hashtags related to a topic (mock implementation)"""
        # This would typically query a trending hashtags database
        topic_trending_map = {
            "history": ["#History", "#Facts", "#Education", "#Learn"],
            "technology": ["#Tech", "#AI", "#Innovation", "#Future"],
            "entertainment": ["#Fun", "#Entertainment", "#Comedy", "#Music"],
            "sports": ["#Sports", "#Fitness", "#Athlete", "#Game"],
            "food": ["#Food", "#Cooking", "#Recipe", "#Delicious"],
            "travel": ["#Travel", "#Adventure", "#Explore", "#Wanderlust"]
        }
        
        for category, hashtags in topic_trending_map.items():
            if category in topic.lower():
                return hashtags
        
        return ["#Trending", "#Viral", "#Popular"]
    
    def _calculate_reach_score(self, hashtag: str) -> float:
        """Calculate reach score for a hashtag (mock implementation)"""
        # This would typically query hashtag usage statistics
        base_score = 0.5
        
        # Mock factors
        if hashtag.lower() in ["#shorts", "#viral", "#trending"]:
            base_score += 0.3
        elif len(hashtag) < 10:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _calculate_engagement_score(self, hashtag: str) -> float:
        """Calculate engagement score for a hashtag (mock implementation)"""
        # This would typically analyze engagement rates for hashtags
        base_score = 0.5
        
        # Mock factors
        if hashtag.lower() in ["#like", "#comment", "#share"]:
            base_score += 0.2
        elif hashtag.lower() in ["#follow", "#subscribe"]:
            base_score += 0.15
        
        return min(base_score, 1.0)
    
    def _calculate_trending_score(self, hashtag: str) -> float:
        """Calculate trending score for a hashtag (mock implementation)"""
        # This would typically analyze recent hashtag growth
        base_score = 0.5
        
        # Mock factors
        if hashtag.lower() in ["#2024", "#2025", "#new", "#latest"]:
            base_score += 0.2
        elif hashtag.lower() in ["#now", "#today"]:
            base_score += 0.15
        
        return min(base_score, 1.0)
    
    def _get_hashtag_recommendation(self, hashtag: str) -> str:
        """Get recommendation for hashtag usage (mock implementation)"""
        if hashtag.lower() in ["#shorts", "#viral", "#trending"]:
            return "Highly recommended - high reach potential"
        elif hashtag.lower() in ["#like", "#comment", "#share"]:
            return "Good for engagement - encourages interaction"
        elif len(hashtag) < 10:
            return "Good length - easy to remember"
        else:
            return "Standard hashtag - moderate performance"
