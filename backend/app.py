from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Todo, TodoCreate, TodoUpdate
from database import (
    get_todos, get_todo, create_todo, update_todo, delete_todo
)

app = FastAPI(
    title="Simple Todo API",
    description="A basic CRUD API for managing todos.",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Todo API is up and running! Check /docs for interactive API."}

@app.get("/todos", response_model=List[Todo], tags=["Todos"])
async def read_todos(skip: int = 0, limit: int = 100):
    todos = get_todos()
    return todos[skip : skip + limit]

@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED, tags=["Todos"])
async def create_new_todo(todo: TodoCreate):
    if not todo.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot be empty."
        )
    return create_todo(todo)

@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def read_todo(todo_id: int):
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )
    return todo

@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def update_existing_todo(todo_id: int, todo_update: TodoUpdate):
    updated_todo = update_todo(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )
    return updated_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
async def delete_existing_todo(todo_id: int):
    if not delete_todo(todo_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )
    return None  # No content for DELETE

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
