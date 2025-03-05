from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import threading

app = FastAPI()

# In-memory storage: {repo: {object: data}}
storage: Dict[str, Dict[str, str]] = {}

# Lock for thread safety
storage_lock = threading.Lock()

class ObjectData(BaseModel):
    data: str

@app.put("/repos/{repo}/objects/{object}")
def put_object(repo: str, object: str, obj: ObjectData):
    with storage_lock:
        if repo not in storage:
            storage[repo] = {}
        storage[repo][object] = obj.data
    return {"message": "Object stored successfully"}

@app.get("/repos/{repo}/objects/{object}")
def get_object(repo: str, object: str):
    with storage_lock:
        if repo not in storage or object not in storage[repo]:
            raise HTTPException(status_code=404, detail="Object not found")
        return {"data": storage[repo][object]}

@app.delete("/repos/{repo}/objects/{object}")
def delete_object(repo: str, object: str):
    with storage_lock:
        if repo not in storage or object not in storage[repo]:
            raise HTTPException(status_code=404, detail="Object not found")
        del storage[repo][object]
    return {"message": "Object deleted successfully"}
