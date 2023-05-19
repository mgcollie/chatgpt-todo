import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List

# Define your MongoDB connection and database
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGODB_URL)
database = client.todo_database
collection = database.todo_collection


# Define your data model
class Todo(BaseModel):
    task: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/todos/{username}")
async def add_todo(username: str, todo: Todo):
    todo_dict = todo.dict()
    todo_dict["username"] = username
    todo_dict["created_at"] = datetime.now()
    todo_dict["updated_at"] = datetime.now()
    result = await collection.insert_one(todo_dict)
    return {"_id": str(result.inserted_id)}


@app.put("/todos/{username}/{id}")
async def update_todo(username: str, id: str, todo: Todo):
    todo_dict = todo.dict()
    todo_dict["updated_at"] = datetime.now()
    result = await collection.update_one({"username": username, "_id": id}, {"$set": todo_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo updated successfully"}


@app.get("/todos/{username}")
async def get_todos(username: str):
    todos = []
    for document in await collection.find({"username": username}).to_list(length=100):
        todos.append(Todo(**document))
    return todos


@app.delete("/todos/{username}")
async def delete_todo(username: str, id: str):
    result = await collection.delete_one({"username": username, "_id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


@app.get("/logo.png")
async def plugin_logo():
    return FileResponse('logo.png', media_type='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open(".well-known/ai-plugin.json") as f:
        text = f.read()
        text = text.replace('${API_PORT}', os.getenv('API_PORT', '8000'))
        return Response(content=text, media_type="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace('${API_PORT}', os.getenv('API_PORT', '8000'))
        return Response(content=text, media_type="text/yaml")
