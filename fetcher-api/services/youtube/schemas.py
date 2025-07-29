from typing import TypedDict, Optional

class PlaylistMetadata(TypedDict, total=False):
  id: str
  title: str
  description: Optional[str]
  thumbnails: list
  modified_date: Optional[str]
  channel: Optional[str]
  channel_id: Optional[str]
  channel_url: Optional[str]
  view_count: Optional[int]
  playlist_count: Optional[int]
  extractor: str
  extractor_key: str
  webpage_url: str
  original_url: str
