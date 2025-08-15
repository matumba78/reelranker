import re
from typing import List, Tuple
import logging

from app.core.constants import MIN_TITLE_LENGTH, MAX_TITLE_LENGTH

logger = logging.getLogger(__name__)

class ScoringService:
    def __init__(self):
        self.emotional_words = [
            'shocking', 'secret', 'truth', 'hidden', 'untold', 'amazing', 
            'incredible', 'viral', 'trending', 'mind-blowing', 'insane',
            'crazy', 'unbelievable', 'wow', 'omg', 'wtf', 'epic', 'legendary'
        ]
        
        self.question_words = ['how', 'why', 'what', 'when', 'where', 'who']
        
        self.trending_keywords = [
            'viral', 'trending', 'shorts', 'fyp', 'tiktok', 'youtube',
            '2024', '2025', 'new', 'latest', 'now', 'today'
        ]
    
    def calculate_viral_score(self, title: str, tags: List[str] = None, 
                            hashtags: List[str] = None, topic: str = None) -> Tuple[float, List[str]]:
        """Calculate viral score for a title and provide reasons"""
        reasons = []
        score = 0.0
        
        # Title length analysis
        length_score, length_reasons = self._analyze_title_length(title)
        score += length_score
        reasons.extend(length_reasons)
        
        # Emotional impact analysis
        emotional_score, emotional_reasons = self._analyze_emotional_impact(title)
        score += emotional_score
        reasons.extend(emotional_reasons)
        
        # Curiosity gap analysis
        curiosity_score, curiosity_reasons = self._analyze_curiosity_gap(title)
        score += curiosity_score
        reasons.extend(curiosity_reasons)
        
        # Trending keyword analysis
        trending_score, trending_reasons = self._analyze_trending_keywords(title, tags, hashtags)
        score += trending_score
        reasons.extend(trending_reasons)
        
        # Topic relevance analysis
        if topic:
            relevance_score, relevance_reasons = self._analyze_topic_relevance(title, topic)
            score += relevance_score
            reasons.extend(relevance_reasons)
        
        # Engagement trigger analysis
        engagement_score, engagement_reasons = self._analyze_engagement_triggers(title)
        score += engagement_score
        reasons.extend(engagement_reasons)
        
        # Cap score at 1.0
        final_score = min(score, 1.0)
        
        return final_score, reasons
    
    def get_improvement_suggestions(self, title: str, current_score: float) -> List[str]:
        """Get suggestions to improve viral score"""
        suggestions = []
        
        if current_score < 0.3:
            suggestions.append("Consider adding emotional hooks like 'Shocking' or 'Secret'")
            suggestions.append("Include trending keywords relevant to your topic")
            suggestions.append("Add numbers or specific details to increase credibility")
        
        if current_score < 0.5:
            suggestions.append("Create curiosity gaps with phrases like 'The Truth About' or 'Why'")
            suggestions.append("Keep title length between 30-50 characters for optimal engagement")
            suggestions.append("Include action words that encourage clicks")
        
        if current_score < 0.7:
            suggestions.append("Add urgency with words like 'Now', 'Today', or 'Latest'")
            suggestions.append("Include social proof elements like 'Everyone is talking about'")
            suggestions.append("Use power words that evoke strong emotions")
        
        # Specific suggestions based on current title
        if len(title) < MIN_TITLE_LENGTH:
            suggestions.append(f"Title is too short. Aim for at least {MIN_TITLE_LENGTH} characters")
        
        if len(title) > MAX_TITLE_LENGTH:
            suggestions.append(f"Title is too long. Keep it under {MAX_TITLE_LENGTH} characters")
        
        if not any(word in title.lower() for word in self.emotional_words):
            suggestions.append("Add emotional words to make the title more compelling")
        
        if not any(word in title.lower() for word in self.question_words):
            suggestions.append("Consider using question words to create curiosity")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _analyze_title_length(self, title: str) -> Tuple[float, List[str]]:
        """Analyze title length and return score and reasons"""
        length = len(title)
        score = 0.0
        reasons = []
        
        # Optimal length is 30-50 characters
        if 30 <= length <= 50:
            score += 0.2
            reasons.append("Optimal title length (30-50 characters)")
        elif 20 <= length <= 60:
            score += 0.1
            reasons.append("Good title length")
        elif length < MIN_TITLE_LENGTH:
            score -= 0.1
            reasons.append("Title too short")
        elif length > MAX_TITLE_LENGTH:
            score -= 0.1
            reasons.append("Title too long")
        
        return score, reasons
    
    def _analyze_emotional_impact(self, title: str) -> Tuple[float, List[str]]:
        """Analyze emotional impact of title"""
        score = 0.0
        reasons = []
        title_lower = title.lower()
        
        emotional_count = sum(1 for word in self.emotional_words if word in title_lower)
        
        if emotional_count >= 2:
            score += 0.25
            reasons.append("Strong emotional hooks present")
        elif emotional_count == 1:
            score += 0.15
            reasons.append("Emotional hook present")
        else:
            reasons.append("No emotional hooks detected")
        
        return score, reasons
    
    def _analyze_curiosity_gap(self, title: str) -> Tuple[float, List[str]]:
        """Analyze curiosity gap creation"""
        score = 0.0
        reasons = []
        title_lower = title.lower()
        
        # Check for question words
        question_count = sum(1 for word in self.question_words if word in title_lower)
        if question_count > 0:
            score += 0.15
            reasons.append("Creates curiosity with question words")
        
        # Check for mystery words
        mystery_words = ['secret', 'hidden', 'truth', 'untold', 'revealed', 'exposed']
        mystery_count = sum(1 for word in mystery_words if word in title_lower)
        if mystery_count > 0:
            score += 0.1
            reasons.append("Creates mystery and intrigue")
        
        # Check for incomplete information
        if '...' in title or '...' in title:
            score += 0.05
            reasons.append("Uses ellipsis to create suspense")
        
        return score, reasons
    
    def _analyze_trending_keywords(self, title: str, tags: List[str] = None, 
                                 hashtags: List[str] = None) -> Tuple[float, List[str]]:
        """Analyze trending keywords"""
        score = 0.0
        reasons = []
        title_lower = title.lower()
        
        # Check title for trending keywords
        title_trending = sum(1 for word in self.trending_keywords if word in title_lower)
        if title_trending > 0:
            score += 0.1
            reasons.append("Contains trending keywords")
        
        # Check tags and hashtags
        all_text = title_lower
        if tags:
            all_text += ' ' + ' '.join(tags).lower()
        if hashtags:
            all_text += ' ' + ' '.join(hashtags).lower()
        
        total_trending = sum(1 for word in self.trending_keywords if word in all_text)
        if total_trending >= 3:
            score += 0.1
            reasons.append("Multiple trending keywords detected")
        
        return score, reasons
    
    def _analyze_topic_relevance(self, title: str, topic: str) -> Tuple[float, List[str]]:
        """Analyze topic relevance"""
        score = 0.0
        reasons = []
        
        title_lower = title.lower()
        topic_lower = topic.lower()
        
        # Check if topic appears in title
        if topic_lower in title_lower:
            score += 0.15
            reasons.append("Topic directly mentioned in title")
        
        # Check for topic keywords
        topic_words = topic_lower.split()
        relevant_words = sum(1 for word in topic_words if word in title_lower)
        if relevant_words >= 2:
            score += 0.1
            reasons.append("Multiple topic keywords present")
        elif relevant_words == 1:
            score += 0.05
            reasons.append("Topic keyword present")
        
        return score, reasons
    
    def _analyze_engagement_triggers(self, title: str) -> Tuple[float, List[str]]:
        """Analyze engagement triggers"""
        score = 0.0
        reasons = []
        title_lower = title.lower()
        
        # Check for numbers
        if re.search(r'\d+', title):
            score += 0.1
            reasons.append("Contains numbers (increases credibility)")
        
        # Check for urgency words
        urgency_words = ['now', 'today', 'latest', 'new', 'just', 'breaking']
        urgency_count = sum(1 for word in urgency_words if word in title_lower)
        if urgency_count > 0:
            score += 0.1
            reasons.append("Creates urgency")
        
        # Check for action words
        action_words = ['watch', 'see', 'learn', 'discover', 'find', 'get']
        action_count = sum(1 for word in action_words if word in title_lower)
        if action_count > 0:
            score += 0.05
            reasons.append("Contains action words")
        
        return score, reasons
