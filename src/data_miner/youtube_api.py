from .youtube_link_processor import YouTubeLinkProcessor
from .youtube_data_processor import YouTubeDataProcessor

link_processor = YouTubeLinkProcessor()
data_processor = YouTubeDataProcessor()

record = link_processor.process_video_link(frontend_url, max_comments=50)
data_processor.add_record(record)

hits = data_processor.search_videos("carrot")