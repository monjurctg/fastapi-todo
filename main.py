from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory data store with some static todos
todos = [
    {"id": 1, "task": "Learn FastAPI"},
    {"id": 2, "task": "Build a To-Do app"},
    {"id": 3, "task": "Deploy to Render"},
]

# Request model
class Todo(BaseModel):
    id: int
    task: str

# Get all todos
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

# Create a new todo
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    for t in todos:
        if t["id"] == todo.id:  # Access dictionary keys with []
            raise HTTPException(status_code=400, detail="ID already exists")
    todos.append(todo.dict())  # Convert Pydantic model to dict before appending
    return todo

# Delete a todo by ID
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")


@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    for todo in todos:
        if todo['id']==todo_id:
            return {"todo":todo}
        raise HTTPException(status_code=404,detail="Todo not found")

