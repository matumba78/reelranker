from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.services.ai_generation import AIGenerationService

router = APIRouter(prefix="/generate", tags=["generate"])

class GenerateRequest(BaseModel):
    topic: str
    count: Optional[int] = 10
    style: Optional[str] = "viral"  # viral, educational, entertaining, etc.

class GenerateResponse(BaseModel):
    titles: List[dict]
    hashtags: List[str]
    topic: str
    provider: Optional[str] = None

@router.post("/", response_model=GenerateResponse)
async def generate_viral_content(request: GenerateRequest):
    """Generate viral titles and hashtags for a topic"""
    try:
        if request.count > 20:
            raise HTTPException(status_code=400, detail="Count cannot exceed 20")
        
        ai_service = AIGenerationService()
        
        # Generate viral titles
        titles = ai_service.generate_viral_titles(
            topic=request.topic,
            count=request.count,
            style=request.style
        )
        
        # Generate hashtags
        hashtags = ai_service.generate_hashtags(
            topic=request.topic,
            titles=titles
        )
        
        # Get provider info
        provider_info = ai_service.ai_service.get_provider_info()
        
        return GenerateResponse(
            titles=titles,
            hashtags=hashtags,
            topic=request.topic,
            provider=provider_info["provider"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/titles")
async def generate_titles_only(request: GenerateRequest):
    """Generate only viral titles"""
    try:
        if request.count > 20:
            raise HTTPException(status_code=400, detail="Count cannot exceed 20")
        
        ai_service = AIGenerationService()
        
        titles = ai_service.generate_viral_titles(
            topic=request.topic,
            count=request.count,
            style=request.style
        )
        
        return {
            "titles": titles,
            "topic": request.topic
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hashtags")
async def generate_hashtags_only(request: GenerateRequest):
    """Generate only hashtags"""
    try:
        ai_service = AIGenerationService()
        
        hashtags = ai_service.generate_hashtags(
            topic=request.topic,
            count=request.count
        )
        
        return {
            "hashtags": hashtags,
            "topic": request.topic
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_topic(request: GenerateRequest):
    """Analyze a topic and provide insights"""
    try:
        ai_service = AIGenerationService()
        
        # Get topic analysis
        analysis = ai_service.analyze_topic(
            topic=request.topic,
            limit=request.count
        )
        
        return {
            "topic": request.topic,
            "top_tags": analysis.get("top_tags", []),
            "top_hashtags": analysis.get("top_hashtags", []),
            "viral_patterns": analysis.get("viral_patterns", []),
            "trending_keywords": analysis.get("trending_keywords", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
