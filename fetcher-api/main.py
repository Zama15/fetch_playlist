from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
from services.youtube import extractor

load_dotenv()

API_URL = getenv("VUE_APP")
SECRET_KEY = getenv("SECRET_KEY")
DEBUG_MODE = getenv("DEBUG") == "True"

app = FastAPI()

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
def read_item(playlist_id: str):
  result, ok = extractor.get_playlist_metadata(playlist_id)
  if not ok:
    raise HTTPException(status_code=404, detail=result)
  return result

@app.get("/meta/author/{author_id}")
def read_item(author_id: str):
  result, ok = extractor.get_author_metadata(author_id)
  if not ok:
    raise HTTPException(status_code=404, detail=result)
  return result

@app.get("/playlist/{playlist_id}")
def read_item(
  playlist_id: str,
  offset: int = 0,
  limit: int = 10
):
  result, ok = extractor.get_limited_playlist_items(playlist_id, offset, limit)
  if not ok:
    raise HTTPException(status_code=404, detail=result)
  return result
