from typing import Dict, Any
from pathlib import Path
from json import load, dump
from re import compile
from .constants import DOWNLOAD_PATH

def select_thumbnail(thumbnails: list[dict], strategy: str = "highest_res") -> dict:
  if not thumbnails or not isinstance(thumbnails, list):
    return None

  if strategy == "first":
    return thumbnails[0]
  elif strategy == "last":
    return thumbnails[-1]
  elif strategy == "lowest_res":
    return min(thumbnails, key=lambda t: t.get("width", 0) * t.get("height", 0))
  else:  # "highest_res" (default)
    return max(thumbnails, key=lambda t: t.get("width", 0) * t.get("height", 0))

def extract_author_thumbnails(thumbnails: list[dict]) -> dict:
  avatar = None
  banner = None

  if not thumbnails:
    return {}
  
  for thumb in thumbnails:
    tid = thumb.get("id", "")
    tp = thumb.get("preference", -100)
    width = thumb.get("width", 0)
    height = thumb.get("height", 0)

    if "avatar" in tid.lower() or (width == height and width >= 100):
      if not avatar or (width > avatar.get("width", 0)):
        avatar = thumb

    if "banner" in tid.lower() or (width > height and width > 1000):
      if not banner or (tp > banner.get("preference", -100)):
        banner = thumb
      
  return {
    "avatar": avatar,
    "banner": banner
  }

def playlist_meta_path(playlist_id: str) -> Path:
  return Path(DOWNLOAD_PATH) / playlist_id / "_playlist_meta.json"

def load_json(file_path: Path) -> Dict[str, Any]:
  if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as f:
      return load(f)
  return {}

def save_json(file_path: Path, data: Dict[str, Any]):
  file_path.parent.mkdir(parents=True, exist_ok=True)
  with open(file_path, "w", encoding="utf-8") as f:
    dump(data, f, indent=2)

def load_downloaded_playlist_meta(playlist_id: str) -> Dict[str, Any]:
  meta_path = playlist_meta_path(playlist_id)
  meta = load_json(meta_path) or {
    "playlist_id": playlist_id,
    "downloaded_indexes": [],
    "videos": {}
  }

  return meta

def save_download_playlist_meta(playlist_id: str, meta: Dict[str, Any]):
  meta_path = playlist_meta_path(playlist_id)
  save_json(meta_path, meta)

# class YDLLogger:
#   def __init__(self):
#     self.errors = {}
#     self.current_video_id = None

#   def debug(self, msg): pass

#   def warning(self, msg):
#     print("YDLLogger [warning] msg: ", msg)
#     print("YDLLogger [warning] errors:", self.errors)
#     print("YDLLogger [warning] video id:", self.current_video_id)
#     if self.current_video_id:
#       self.errors[self.current_video_id] = msg

#   def error(self, msg):
#     print("YDLLogger [error] msg: ", msg)
#     print("YDLLogger [error] errors:", self.errors)
#     print("YDLLogger [error] video id:", self.current_video_id)
#     if (self.current_video_id):
#       self.error[self.current_video_id] = msg

class YDLLogger:
  _id_pattern = compile(r"\[youtube\]\s+([A-Za-z0-9_-]{11})")

  def __init__(self):
    self.errors = {}

  def _extract_id(self, msg):
    m = self._id_pattern.search(msg)
    return m.group(1) if m else None

  def debug(self, msg): pass

  def warning(self, msg):
    vid_id = self._extract_id(msg)
    if vid_id:
      self.errors[vid_id] = msg

  def error(self, msg):
    vid_id = self._extract_id(msg)
    if vid_id:
      self.errors[vid_id] = msg
