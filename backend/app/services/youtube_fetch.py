import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def search_shorts(self, query: str, max_results: int = 50, region_code: str = "IN") -> List[Dict]:
        """Search for YouTube Shorts videos"""
        try:
            if not self.api_key:
                logger.warning("YouTube API key not configured")
                return []
            
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "videoDuration": "short",
                "maxResults": max_results,
                "regionCode": region_code,
                "key": self.api_key
            }
            
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            for item in data.get("items", []):
                video_data = {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["medium"]["url"]
                }
                videos.append(video_data)
            
            return videos
            
        except Exception as e:
            logger.error(f"Error fetching YouTube Shorts: {e}")
            return []
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """Get detailed information for multiple videos"""
        try:
            if not self.api_key:
                logger.warning("YouTube API key not configured")
                return []
            
            # YouTube API allows max 50 video IDs per request
            all_videos = []
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                params = {
                    "part": "snippet,statistics,contentDetails",
                    "id": ",".join(batch_ids),
                    "key": self.api_key
                }
                
                response = requests.get(f"{self.base_url}/videos", params=params)
                response.raise_for_status()
                
                data = response.json()
                
                for item in data.get("items", []):
                    video_data = {
                        "video_id": item["id"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "channel_id": item["snippet"]["channelId"],
                        "channel_title": item["snippet"]["channelTitle"],
                        "published_at": item["snippet"]["publishedAt"],
                        "thumbnail_url": item["snippet"]["thumbnails"]["medium"]["url"],
                        "views": int(item["statistics"].get("viewCount", 0)),
                        "likes": int(item["statistics"].get("likeCount", 0)),
                        "comments": int(item["statistics"].get("commentCount", 0)),
                        "duration": self._parse_duration(item["contentDetails"]["duration"])
                    }
                    all_videos.append(video_data)
            
            return all_videos
            
        except Exception as e:
            logger.error(f"Error fetching video details: {e}")
            return []
    
    def get_trending_videos(self, region_code: str = "IN", category_id: str = "1") -> List[Dict]:
        """Get trending videos for a region"""
        try:
            if not self.api_key:
                logger.warning("YouTube API key not configured")
                return []
            
            params = {
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "regionCode": region_code,
                "videoCategoryId": category_id,
                "maxResults": 50,
                "key": self.api_key
            }
            
            response = requests.get(f"{self.base_url}/videos", params=params)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            for item in data.get("items", []):
                video_data = {
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["medium"]["url"],
                    "views": int(item["statistics"].get("viewCount", 0)),
                    "likes": int(item["statistics"].get("likeCount", 0)),
                    "comments": int(item["statistics"].get("commentCount", 0))
                }
                videos.append(video_data)
            
            return videos
            
        except Exception as e:
            logger.error(f"Error fetching trending videos: {e}")
            return []
    
    def _parse_duration(self, duration: str) -> int:
        """Parse ISO 8601 duration to seconds"""
        try:
            # Remove 'PT' prefix
            duration = duration[2:]
            seconds = 0
            
            if 'H' in duration:
                hours = int(duration.split('H')[0])
                seconds += hours * 3600
                duration = duration.split('H')[1]
            
            if 'M' in duration:
                minutes = int(duration.split('M')[0])
                seconds += minutes * 60
                duration = duration.split('M')[1]
            
            if 'S' in duration:
                secs = int(duration.split('S')[0])
                seconds += secs
            
            return seconds
        except:
            return 0
