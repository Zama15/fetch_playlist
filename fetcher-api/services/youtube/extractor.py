from typing import Tuple, Dict, Any, List, Set
from enum import Enum
from yt_dlp import YoutubeDL
from .constants import (
  DOWNLOAD_PATH,
  PlaylistTargetKeys,
  VideoTargetKeys,
  ThumbnailStrategy,
  AuthorTargetKeys
)
from .utils import (
  select_thumbnail,
  extract_author_thumbnails,
  load_downloaded_playlist_meta,
  save_download_playlist_meta,
  YDLLogger
)
from utils.task_manager import TaskManager
from utils.debug import log, log_trace

def _default_ydl_opts(overrides: dict = None) -> dict:
  base_opts = {
    "quiet": True,
    "skip_download": True,
    "ignoreerrors": True,
    "socket_timeout": 20,
  }

  if overrides:
    base_opts.update(overrides)
  
  return base_opts

def _ydl_progress_hook(
    task_manager: TaskManager,
    task_id: str,
    data: Dict[str, Any]
  ):
  if task_manager.is_cancelled(task_id):
    raise Exception("Cancelled by user")

  if data.get("status") == "downloading":
    total = data.get("total_bytes") or data.get("total_bytes_estimate") or 1
    downloaded = data.get("downloaded_bytes", 0)
    task_manager.start_step(task_id, f"downloading {data.get("filename", "")}")
    task_manager.update_progress(task_id, downloaded / total)

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
    offset: int = 1,
    limit: int = 10
  ) -> Tuple[Dict[str, Any], bool]:
  url = f"https://www.youtube.com/playlist?list={playlist_id}"

  start_index = offset
  end_index = offset + limit - 1

  options = _default_ydl_opts({
    "playlist_items": f"{start_index}-{end_index}",
  })

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
    offset: int = 1,
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

      filtered = [
        _filter_metadata(item, PlaylistTargetKeys) if item is not None else None
        for item in metadata.get("entries", [])
      ]
      sanitized = ydl.sanitize_info({ "items": filtered })

      return sanitized, True
  except Exception as e:
    return { "error": str(e) }, False

def _download_videos(
  task_manager: TaskManager,
  task_id: str,
  playlist_id: str,
  indexes: List[int],
  meta: Dict[str, Any],
  logger: YDLLogger,
) -> Tuple[Set[int], Set[int]]:
  """
  Downloads the given playlist indexes and returns (downloaded_indexes, failed_indexes)
  """
  missing_indexes = set(indexes)
  downloaded_indexes = set()

  opts = _default_ydl_opts({
    "skip_download": False,
    "retries": 5,
    "http_chunk_size": 10 * 1024 * 1024, # 10MiB
    "concurrent_fragment_downloads": 5, 
    "fragment_retries": 5,
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "outtmpl": f"{DOWNLOAD_PATH}/{playlist_id}/%(id)s.%(ext)s",
    "restrictfilenames": True,
    "writeinfojson": True,
    "embedthumbnail": True,
    "addmetadata": True,
    "download_archive": f"{DOWNLOAD_PATH}/{playlist_id}/archive.txt",
    "playlist_items": ",".join(str(i) for i in indexes),
    "logger": logger,
    "progress_hooks": [lambda d: _ydl_progress_hook(task_manager, task_id, d)],
  })

  url = f"https://www.youtube.com/playlist?list={playlist_id}"

  try:
    log(f"[{task_id}] _download_videos: starting extract_info for indexes={indexes}")
    if task_manager.is_cancelled(task_id):
      raise Exception("Cancelled before starting download")

    with YoutubeDL(opts) as ydl:
      if task_manager.is_cancelled(task_id):
        raise Exception("Cancelled before starting download")

      try:
        result = ydl.extract_info(url)
      except Exception as ex:
        log(f"[{task_id}] _download_videos: extract_info raised: {ex}")
        log_trace()
        raise

      if result and "entries" in result:
        for idx, entry in zip(indexes, result.get("entries")):
          if entry:
            vid_id = entry.get("id")
            downloaded_indexes.add(idx)
            missing_indexes.discard(idx)
            meta["videos"][vid_id] = {
              "title": entry.get("title"),
              "index": idx,
              "file": f"{vid_id}.{entry.get("ext")}"
            }
            logger.current_video_id = None
        
    return downloaded_indexes, missing_indexes
  
  except Exception as e:
    log(f"[{task_id}] _download_videos: exception: {e}")
    log_trace()
    raise

def _fetch_unavailable_metadata(
  task_manager: TaskManager,
  task_id: str,
  playlist_id: str,
  indexes: Set[int],
  meta: Dict[str, Any],
  logger: YDLLogger,
) -> int:
  if not indexes:
    log(f"[{task_id}] _fetch_unavailable_metadata: no indexes, returning 0")
    return 0
  
  opts = _default_ydl_opts({
    "extract_flat": True,
    "playlist_items": ",".join(str(i) for i in sorted(indexes)),
    "logger": logger,
    "progress_hooks": [lambda d: _ydl_progress_hook(task_manager, task_id, d)],
  })
  
  url = f"https://www.youtube.com/playlist?list={playlist_id}"

  unavailable_count = 0
  try:
    log(f"[{task_id}] _fetch_unavailable_metadata: starting for indexes={sorted(indexes)}")
    if task_manager.is_cancelled(task_id):
      raise Exception("Cancelled before starting fetch unavailable videos")
    
    with YoutubeDL(opts) as ydl:  
      try:
        result = ydl.extract_info(url)
      except Exception as ex:
        log(f"[{task_id}] _fetch_unavailable_metadata: extract_info raised: {ex}")
        log_trace()
        raise

      if result and "entries" in result:
        for idx, entry in zip(indexes, result.get("entries")):
          if entry:
            vid_id = entry.get("id")
            error_msg = logger.errors.get(vid_id, "Video unavailable")
            meta["videos"][vid_id] = {
              "title": entry.get("title"),
              "index": idx,
              "error": error_msg
            }
            unavailable_count += 1

    return unavailable_count
  except Exception as e:
    log(f"[{task_id}] _fetch_unavailable_metadata: exception: {e}")
    log_trace()
    raise

def download_limited_playlist_items(
  task_manager: TaskManager,
  task_id: str,
  playlist_id: str,
  offset: int = 1,
  limit: int = 10,
):
  try:
    log(f"[{task_id}] download_limited_playlist_items: started")
    task_manager.start(task_id)
    
    meta = load_downloaded_playlist_meta(playlist_id)
    downloaded_set = set(meta["downloaded_indexes"])

    requested_indexes = list(range(offset, offset + limit))
    pending_indexes = [i for i in requested_indexes if i not in downloaded_set]
    
    if not pending_indexes:
      task_manager.update_result(task_id, "All requested items already downloaded")
      return 
    
    logger = YDLLogger()

    # Step 1: Try to download the videos in pending indexes
    task_manager.start_step(task_id, "download")
    dl_indexes, missing_indexes = _download_videos(
      task_manager, task_id, playlist_id, pending_indexes, meta, logger
    )
    task_manager.complete_step(task_id)

    ## Step 1.a: Check download task status
    dl_status = task_manager.get(task_id)["status"]
    if task_manager.is_cancelled(task_id):
      task_manager.update_result(task_id, "Cancelled during download")
      return 

    ## Step 1.b: Update metadata file in disk
    downloaded_set.update(dl_indexes)
    save_download_playlist_meta(playlist_id, {**meta, "downloaded_indexes": sorted(downloaded_set)})
    
    # Step 2: Get Metadata for non-donwloaded videos in Step 1
    task_manager.start_step(task_id, "fetch_metadata_errors")
    unavailable_count = _fetch_unavailable_metadata(
      task_manager, task_id, playlist_id, missing_indexes, meta, logger
    )
    task_manager.complete_step(task_id)

    ## Step 2.a: Check fallback task status
    if task_manager.is_cancelled(task_id):
      task_manager.update_result(task_id, "Cancelled during metadata fetch")
      return 

    ## Step 2.b: Update metadata file in disk
    downloaded_set.update(missing_indexes)
    save_download_playlist_meta(playlist_id, {**meta, "downloaded_indexes": sorted(downloaded_set)})

    task_manager.update_result(task_id, f"Downloaded {len(dl_indexes)} videos. {unavailable_count} unavailable.")
  except Exception as e:
    log(f"[{task_id}] download_limited_playlist_items: exception: {e}")
    log_trace()
    task_manager.update_error(task_id, str(e))
  finally:
    log(f"[{task_id}] download_limited_playlist_items: finished (task left in manager for inspection)")
    # DO NOT delete the task here during debug — keep it for inspection.
    # task_manager.delete(task_id)  # remove only when you want to forget the task
