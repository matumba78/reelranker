import openai
from typing import List, Dict, Optional
import logging
import re

from app.core.config import settings
from app.core.constants import VIRAL_TITLE_PATTERNS, HASHTAG_CATEGORIES

logger = logging.getLogger(__name__)

class AIGenerationService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.MODEL_NAME
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_viral_titles(self, topic: str, count: int = 10, style: str = "viral") -> List[Dict]:
        """Generate viral titles for a given topic"""
        try:
            if not self.api_key:
                logger.warning("OpenAI API key not configured, using fallback patterns")
                return self._generate_fallback_titles(topic, count)
            
            prompt = f"""
            Generate {count} viral YouTube Shorts titles for the topic: "{topic}"
            
            Requirements:
            - Each title should be engaging and click-worthy
            - Include emotional hooks and curiosity gaps
            - Keep titles under 60 characters
            - Use patterns like "The Shocking Truth", "How to", "Why", "The Secret"
            - Make them feel urgent and trending
            
            Style: {style}
            
            Return only the titles, one per line, with no numbering or extra text.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating viral YouTube Shorts titles that drive high engagement and views."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            titles_text = response.choices[0].message.content.strip()
            titles = [title.strip() for title in titles_text.split('\n') if title.strip()]
            
            # Calculate viral scores for each title
            result = []
            for title in titles[:count]:
                viral_score = self._calculate_title_viral_score(title, topic)
                result.append({
                    "title": title,
                    "viral_score": viral_score
                })
            
            # Sort by viral score
            result.sort(key=lambda x: x["viral_score"], reverse=True)
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating viral titles: {e}")
            return self._generate_fallback_titles(topic, count)
    
    def generate_hashtags(self, topic: str, titles: Optional[List] = None, count: int = 10) -> List[str]:
        """Generate relevant hashtags for a topic"""
        try:
            if not self.api_key:
                logger.warning("OpenAI API key not configured, using fallback hashtags")
                return self._generate_fallback_hashtags(topic, count)
            
            # Extract keywords from titles if provided
            keywords = []
            if titles:
                for title_data in titles:
                    title = title_data.get("title", "") if isinstance(title_data, dict) else str(title_data)
                    keywords.extend(self._extract_keywords(title))
            
            # Add topic keywords
            keywords.extend(self._extract_keywords(topic))
            keywords = list(set(keywords))[:5]  # Top 5 unique keywords
            
            prompt = f"""
            Generate {count} relevant hashtags for YouTube Shorts about: "{topic}"
            
            Keywords to include: {', '.join(keywords)}
            
            Requirements:
            - Mix of specific and general hashtags
            - Include trending hashtags like #Shorts, #Viral, #FYP
            - Use relevant topic-specific hashtags
            - Keep hashtags under 20 characters each
            - Include some engagement hashtags like #Like, #Comment
            
            Return only the hashtags, one per line, with no extra text.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating viral hashtags for social media content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            hashtags_text = response.choices[0].message.content.strip()
            hashtags = [tag.strip() for tag in hashtags_text.split('\n') if tag.strip()]
            
            # Add some standard hashtags
            standard_hashtags = ["#Shorts", "#Viral", "#FYP"]
            for tag in standard_hashtags:
                if tag not in hashtags:
                    hashtags.append(tag)
            
            return hashtags[:count]
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            return self._generate_fallback_hashtags(topic, count)
    
    def analyze_topic(self, topic: str, limit: int = 50) -> Dict:
        """Analyze a topic and provide insights"""
        try:
            if not self.api_key:
                logger.warning("OpenAI API key not configured, using fallback analysis")
                return self._generate_fallback_analysis(topic)
            
            prompt = f"""
            Analyze the topic "{topic}" for YouTube Shorts content creation.
            
            Provide insights on:
            1. Top 5 trending tags related to this topic
            2. Top 5 trending hashtags for this topic
            3. 3 viral title patterns that work well for this topic
            4. 5 trending keywords related to this topic
            
            Format your response as JSON with these keys:
            - top_tags: list of tags with scores (0-1)
            - top_hashtags: list of hashtags with scores (0-1)
            - viral_patterns: list of title patterns
            - trending_keywords: list of keywords
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing social media trends and viral content patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.5
            )
            
            # Parse JSON response
            import json
            try:
                analysis = json.loads(response.choices[0].message.content.strip())
                return analysis
            except json.JSONDecodeError:
                logger.error("Failed to parse AI response as JSON")
                return self._generate_fallback_analysis(topic)
            
        except Exception as e:
            logger.error(f"Error analyzing topic: {e}")
            return self._generate_fallback_analysis(topic)
    
    def _generate_fallback_titles(self, topic: str, count: int) -> List[Dict]:
        """Generate fallback titles using patterns when AI is not available"""
        titles = []
        for i, pattern in enumerate(VIRAL_TITLE_PATTERNS[:count]):
            title = pattern.format(topic=topic)
            viral_score = 0.7 + (i * 0.02)  # Decreasing score
            titles.append({
                "title": title,
                "viral_score": round(viral_score, 2)
            })
        return titles
    
    def _generate_fallback_hashtags(self, topic: str, count: int) -> List[str]:
        """Generate fallback hashtags when AI is not available"""
        hashtags = []
        
        # Add topic-based hashtag
        topic_hashtag = "#" + topic.replace(" ", "").title()
        hashtags.append(topic_hashtag)
        
        # Add standard hashtags
        for category, tags in HASHTAG_CATEGORIES.items():
            hashtags.extend(tags[:2])  # Add 2 from each category
        
        # Add some topic-specific variations
        keywords = self._extract_keywords(topic)
        for keyword in keywords[:3]:
            hashtags.append("#" + keyword.title())
        
        return list(set(hashtags))[:count]
    
    def _generate_fallback_analysis(self, topic: str) -> Dict:
        """Generate fallback analysis when AI is not available"""
        keywords = self._extract_keywords(topic)
        
        return {
            "top_tags": [
                {"tag": keyword.title(), "score": 0.8 - (i * 0.1)} 
                for i, keyword in enumerate(keywords[:5])
            ],
            "top_hashtags": [
                {"hashtag": "#" + keyword.title(), "score": 0.8 - (i * 0.1)}
                for i, keyword in enumerate(keywords[:5])
            ],
            "viral_patterns": [
                f"The Shocking Truth About {topic}",
                f"How {topic} Changed Everything",
                f"Why {topic} is Going Viral"
            ],
            "trending_keywords": keywords[:5]
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction - in production, use NLP libraries
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return list(set(keywords))
    
    def _calculate_title_viral_score(self, title: str, topic: str) -> float:
        """Calculate viral score for a title"""
        score = 0.5  # Base score
        
        # Length bonus (optimal length is 30-50 characters)
        length = len(title)
        if 30 <= length <= 50:
            score += 0.2
        elif 20 <= length <= 60:
            score += 0.1
        
        # Emotional words bonus
        emotional_words = ['shocking', 'secret', 'truth', 'hidden', 'untold', 'amazing', 'incredible', 'viral', 'trending']
        for word in emotional_words:
            if word.lower() in title.lower():
                score += 0.1
        
        # Question words bonus
        question_words = ['how', 'why', 'what', 'when', 'where', 'who']
        for word in question_words:
            if word.lower() in title.lower():
                score += 0.05
        
        # Topic relevance bonus
        if topic.lower() in title.lower():
            score += 0.1
        
        # Number bonus
        if any(char.isdigit() for char in title):
            score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0
