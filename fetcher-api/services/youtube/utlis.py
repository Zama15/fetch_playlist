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
    width = thumb.get("width", 0)
    height = thumb.get("height", 0)

    if "avatar" in tid.lower() or (width == height and width >= 100):
      if not avatar or (width > avatar.get("width", 0)):
        avatar = thumb

    if "banner" in tid.lower() or (width > height and width > 1000):
      if not banner or (width > banner.get("width", 0)):
        banner = thumb
      
  return {
    "avatar": avatar,
    "banner": banner
  }
