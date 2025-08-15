from .video import Video, Base as VideoBase
from .topic import Topic, Base as TopicBase
from .tag import Tag, Base as TagBase

# Export all models
__all__ = [
    "Video",
    "Topic", 
    "Tag",
    "VideoBase",
    "TopicBase",
    "TagBase"
]
