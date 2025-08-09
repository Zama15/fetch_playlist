from typing import Tuple, Dict, Any
from enum import Enum
from .constants import PlaylistTargetKeys, VideoTargetKeys, ThumbnailStrategy, AuthorTargetKeys
from .utlis import select_thumbnail, extract_author_thumbnails
from yt_dlp import YoutubeDL

def _default_ydl_opts(overrides: dict = None) -> dict:
  base_opts = {
    "quiet": True,
    "skip_download": True,
    "ignoreerrors": True,
    "retries": 5,
    "socket_timeout": 20,
    "http_chunk_size": "10M",
  }

  if overrides:
    base_opts.update(overrides)
  
  return base_opts

def _filter_metadata(metadata: dict, keys_enum: Enum) -> dict:
  return { key.value: metadata.get(key.value) for key in keys_enum }

def get_playlist_metadata(playlist_id: str) -> Tuple[Dict[str, Any], bool]:
  url = f"https://www.youtube.com/playlist?list={playlist_id}"
  options = _default_ydl_opts({ "playlist_items": "0" })

  try:
    with YoutubeDL(options) as ydl:
      metadata = ydl.extract_info(url)
      
      if (metadata is None):
        return ({ "error": "Playlist could not be retrieved" }, False)

      filtered = _filter_metadata(metadata, PlaylistTargetKeys)
      sanitized = ydl.sanitize_info(filtered)
      sanitized["thumbnail_best"] = select_thumbnail(sanitized.get("thumbnails"), strategy=ThumbnailStrategy.HIGHEST_RES.value)

      return sanitized, True
  except Exception as e:
    return { "error": str(e) }, False
  
def get_author_metadata(author_id: str) -> Tuple[Dict[str, Any], bool]:
  channel_url = f"https://www.youtube.com/channel/{author_id}"
  featured_url = f"https://www.youtube.com/{author_id}/featured"

  options = _default_ydl_opts({ "playlist_items": "0" })

  try:
    with YoutubeDL(options) as ydl:
      url = featured_url if "@" in author_id else channel_url
      metadata = ydl.extract_info(url)
      
      if (metadata is None):
        return ({ "error": "Author could not be retrieved" }, False)

      filtered = _filter_metadata(metadata, AuthorTargetKeys)
      sanitized = ydl.sanitize_info(filtered)

      thumbnails_info = extract_author_thumbnails(sanitized.get("thumbnails", []))
      sanitized.update({
        "avatar": thumbnails_info.get("avatar"),
        "banner": thumbnails_info.get("banner")
      })

      return sanitized, True
  except Exception as e:
    return { "error": str(e) }, False

def get_limited_playlist_items(
    playlist_id: str,
    offset: int = 0,
    limit: int = 10
  ) -> Tuple[Dict[str, Any], bool]:
  url = f"https://www.youtube.com/playlist?list={playlist_id}"

  start_index = offset
  end_index = offset + limit - 1

  options = _default_ydl_opts({ "playlist_items": f"{start_index}-{end_index}" })

  try:
    with YoutubeDL(options) as ydl:
      metadata = ydl.extract_info(url)
      
      if (metadata is None):
        return ({ "error": "Playlist could not be retrieved" }, False)

      filtered = [
        _filter_metadata(item, VideoTargetKeys) if item is not None else None
        for item in metadata.get("entries", [])
      ]
      sanitized = ydl.sanitize_info({ "items": filtered })

      return sanitized, True
  except Exception as e:
    return { "error": str(e) }, False

def get_limited_author_playlists(
    uploader_id: str,
    offset: int = 0,
    limit: int = 5
  ) -> Tuple[Dict[str, Any], bool]:
  url = f"https://www.youtube.com/{uploader_id}/playlists"

  start_index = offset
  end_index = offset + limit - 1

  options = _default_ydl_opts({
    "playlist_items": f"{start_index}-{end_index}",
    "extract_flat": True,
  })

  try:
    with YoutubeDL(options) as ydl:
      metadata = ydl.extract_info(url)
      
      if (metadata is None):
        return ({ "error": "Author playlists could not be retrieved" }, False)

      sanitized = ydl.sanitize_info(metadata)

      thumbnails_info = extract_author_thumbnails(sanitized.get("thumbnails", []))
      sanitized.update({
        "avatar": thumbnails_info.get("avatar"),
        "banner": thumbnails_info.get("banner")
      })

      return sanitized, True
  except Exception as e:
    return { "error": str(e) }, False
