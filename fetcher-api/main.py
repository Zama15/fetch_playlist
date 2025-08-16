from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
from services.youtube import extractor
from utils.models import LimitedRequest
from utils.task_manager import TaskManager

load_dotenv()

API_URL = getenv("VUE_APP")
SECRET_KEY = getenv("SECRET_KEY")
DEBUG_MODE = getenv("DEBUG") == "True"

app = FastAPI()
task_manager = TaskManager()

app.add_middleware(
  CORSMiddleware,
  allow_origins=[API_URL],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def read_root():
  return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/meta/playlist/{playlist_id}")
def get_playlist_metadata(playlist_id: str):
  result, ok = extractor.get_playlist_metadata(playlist_id)
  if not ok:
    raise HTTPException(status_code=404, detail=result)
  return result

@app.get("/meta/author/{author_id}")
def get_author_metadata(author_id: str):
  result, ok = extractor.get_author_metadata(author_id)
  if not ok:
    raise HTTPException(status_code=404, detail=result)
  return result

@app.get("/playlist/{playlist_id}")
def get_limited_playlist_items(
  playlist_id: str,
  offset: int = 1,
  limit: int = 10
):
  result, ok = extractor.get_limited_playlist_items(playlist_id, offset, limit)
  if not ok:
    raise HTTPException(status_code=404, detail=result)
  return result

@app.get("/author/{uploader_id}")
def get_limited_author_playlists(
  uploader_id: str,
  offset: int = 1,
  limit: int = 5,
):
  result, ok = extractor.get_limited_author_playlists(uploader_id, offset, limit)
  if not ok:
    raise HTTPException(status_code=404, detail=result)
  return result

@app.post("/download/playlist/{playlist_id}")
def download_limited_playlist_items(
  playlist_id: str,
  request: LimitedRequest,
  background_task: BackgroundTasks
):
  task_id = task_manager.create()

  background_task.add_task(
    extractor.download_limited_playlist_items,
    task_manager,
    task_id,
    playlist_id,
    request.offset,
    request.limit,
  )

  return { "task_id": task_id }

@app.get("/tasks/{task_id}")
def get_status(task_id: str):
  task = task_manager.get(task_id)

  if not task:
    raise HTTPException(404, "Task not found")
  
  return task

@app.post("/tasks/{task_id}/cancel")
def cancel_task(task_id: str):
  if task_manager.cancel(task_id):
    return {"message": f"Task {task_id} cancellation requested"}
  else:
    raise HTTPException(status_code=404, detail="Task not found")
