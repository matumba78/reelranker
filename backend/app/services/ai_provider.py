#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Provider Service for ReelRanker
Supports Google AI Studio (Gemini)
"""

import requests
import logging
import google.generativeai as genai
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod

from app.core.config import settings

logger = logging.getLogger(__name__)

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate_text(self, messages: List[Dict[str, str]], max_tokens: int = 500, temperature: float = 0.8) -> str:
        """Generate text using the AI provider"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured"""
        pass

class GoogleAIProvider(AIProvider):
    """Google AI Studio (Gemini) API provider"""
    
    def __init__(self, model_name: str = None):
        self.api_key = settings.GOOGLE_AI_API_KEY
        # Use provided model or default to gemini-1.5-flash
        self.model = model_name or settings.MODEL_NAME
        
        # Validate model name
        valid_models = ["gemini-1.5-flash", "gemini-1.5-flash-8b"]
        if self.model not in valid_models:
            logger.warning(f"Model {self.model} not in valid models, using gemini-1.5-flash")
            self.model = "gemini-1.5-flash"
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate_text(self, messages: List[Dict[str, str]], max_tokens: int = 500, temperature: float = 0.8) -> str:
        """Generate text using Google AI Studio API"""
        try:
            # Convert OpenAI format messages to Gemini format
            prompt = self._convert_messages_to_prompt(messages)
            
            # Configure generation config for newer models
            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.8,
                "top_k": 40
            }
            
            # Generate content with newer API format
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response.text:
                return response.text.strip()
            else:
                raise Exception("No response text generated")
                
        except Exception as e:
            logger.error(f"Google AI API error: {e}")
            raise
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI format messages to Gemini prompt format"""
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        return "\n\n".join(prompt_parts)

class AIProviderFactory:
    """Factory for creating AI providers"""
    
    @staticmethod
    def get_provider(provider_name: str = None, model_name: str = None) -> AIProvider:
        """Get the appropriate AI provider"""
        if provider_name is None:
            provider_name = settings.AI_PROVIDER
        
        # Use Google AI Studio (default and only provider)
        if provider_name.lower() == "google":
            provider = GoogleAIProvider(model_name=model_name)
            if provider.is_available():
                return provider
            else:
                logger.warning("Google AI Studio not available")
        
        # If no provider is available, raise an error
        raise Exception("No AI provider is configured. Please set GOOGLE_AI_API_KEY")

class AIService:
    """Main AI service that uses the appropriate provider"""
    
    def __init__(self, provider_name: str = None, model_name: str = None):
        self.provider = AIProviderFactory.get_provider(provider_name, model_name)
        self.provider_name = provider_name or settings.AI_PROVIDER
        self.model_name = model_name or settings.MODEL_NAME
    
    def generate_text(self, messages: List[Dict[str, str]], max_tokens: int = 500, temperature: float = 0.8) -> str:
        """Generate text using the configured provider"""
        return self.provider.generate_text(messages, max_tokens, temperature)
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider"""
        return {
            "provider": self.provider_name,
            "available": self.provider.is_available(),
            "model": getattr(self.provider, 'model', 'unknown'),
            "model_name": self.model_name
        }
