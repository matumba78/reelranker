# API Constants
API_VERSION = "v1"
BASE_URL = "https://api.viralshorts.ai"

# Video Processing Constants
MAX_VIDEO_DURATION = 60  # seconds
MIN_VIDEO_DURATION = 5   # seconds
MAX_TITLE_LENGTH = 100
MIN_TITLE_LENGTH = 10

# Engagement Thresholds
HIGH_ENGAGEMENT_THRESHOLD = 0.05
MEDIUM_ENGAGEMENT_THRESHOLD = 0.02
LOW_ENGAGEMENT_THRESHOLD = 0.01

# Trending Constants
TRENDING_DAYS = 7
VIRAL_VIEWS_THRESHOLD = 1000000
VIRAL_LIKES_THRESHOLD = 50000

# Content Categories
VIDEO_CATEGORIES = [
    "entertainment",
    "education",
    "news",
    "sports",
    "music",
    "comedy",
    "lifestyle",
    "technology",
    "gaming",
    "food",
    "travel",
    "fitness",
    "beauty",
    "fashion",
    "pets",
    "science",
    "history",
    "politics",
    "business",
    "art"
]

# Viral Patterns
VIRAL_TITLE_PATTERNS = [
    "The Shocking Truth About {topic}",
    "How {topic} Changed Everything",
    "The Untold Story of {topic}",
    "Why {topic} is Going Viral",
    "The Secret Behind {topic}",
    "What Nobody Tells You About {topic}",
    "The Real Reason {topic} is Popular",
    "How to {topic} in 60 Seconds",
    "The Hidden Meaning of {topic}",
    "Why {topic} is Trending Right Now"
]

# Hashtag Categories
HASHTAG_CATEGORIES = {
    "trending": ["#Shorts", "#Viral", "#Trending", "#FYP"],
    "engagement": ["#Like", "#Comment", "#Share", "#Follow"],
    "content": ["#Video", "#Content", "#Creator", "#YouTube"],
    "time": ["#Now", "#Today", "#Latest", "#New"]
}

# Rate Limiting
RATE_LIMITS = {
    "free": {"requests_per_minute": 10, "requests_per_hour": 100},
    "basic": {"requests_per_minute": 50, "requests_per_hour": 1000},
    "premium": {"requests_per_minute": 200, "requests_per_hour": 5000}
}

# Error Messages
ERROR_MESSAGES = {
    "invalid_topic": "Topic must be between 3 and 100 characters",
    "invalid_title": "Title must be between 10 and 100 characters",
    "rate_limit_exceeded": "Rate limit exceeded. Please upgrade your plan.",
    "api_key_required": "API key is required for this endpoint",
    "invalid_api_key": "Invalid API key provided",
    "video_not_found": "Video not found",
    "topic_not_found": "Topic not found"
}

# Success Messages
SUCCESS_MESSAGES = {
    "video_created": "Video created successfully",
    "video_updated": "Video updated successfully",
    "video_deleted": "Video deleted successfully",
    "topic_created": "Topic created successfully",
    "topic_updated": "Topic updated successfully",
    "topic_deleted": "Topic deleted successfully"
}
