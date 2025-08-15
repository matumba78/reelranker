from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

from app.services.scoring import ScoringService

router = APIRouter(prefix="/score", tags=["score"])

class ScoreRequest(BaseModel):
    title: str
    tags: Optional[List[str]] = []
    hashtags: Optional[List[str]] = []
    topic: Optional[str] = None

class ScoreResponse(BaseModel):
    viral_score: float
    reasons: List[str]
    suggestions: Optional[List[str]] = []

@router.post("/", response_model=ScoreResponse)
async def get_viral_score(request: ScoreRequest):
    """Calculate viral score for a title and tags"""
    try:
        scoring_service = ScoringService()
        
        # Calculate viral score
        score, reasons = scoring_service.calculate_viral_score(
            title=request.title,
            tags=request.tags,
            hashtags=request.hashtags,
            topic=request.topic
        )
        
        # Generate improvement suggestions
        suggestions = scoring_service.get_improvement_suggestions(
            title=request.title,
            current_score=score
        )
        
        return ScoreResponse(
            viral_score=round(score, 3),
            reasons=reasons,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch")
async def score_multiple_titles(titles: List[ScoreRequest]):
    """Score multiple titles in batch"""
    try:
        scoring_service = ScoringService()
        results = []
        
        for request in titles:
            score, reasons = scoring_service.calculate_viral_score(
                title=request.title,
                tags=request.tags,
                hashtags=request.hashtags,
                topic=request.topic
            )
            
            results.append({
                "title": request.title,
                "viral_score": round(score, 3),
                "reasons": reasons
            })
        
        # Sort by viral score descending
        results.sort(key=lambda x: x["viral_score"], reverse=True)
        
        return {
            "results": results,
            "total": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
