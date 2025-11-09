import threading
from typing import List, Optional
from datetime import datetime
from models import Todo, TodoCreate, TodoUpdate

# Thread-safe in-memory storage (simple lock for concurrency)
todos: List[Todo] = []
next_id = 1
lock = threading.Lock()

def get_todos() -> List[Todo]:
    with lock:
        return todos.copy()

def get_todo(todo_id: int) -> Optional[Todo]:
    with lock:
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None

def create_todo(todo_data: TodoCreate) -> Todo:
    global next_id
    with lock:
        new_todo = Todo(
            id=next_id,
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed,
            created_at=datetime.now()
        )
        todos.append(new_todo)
        next_id += 1
        return new_todo

def update_todo(todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
    with lock:
        for todo in todos:
            if todo.id == todo_id:
                todo.title = todo_update.title
                todo.description = todo_update.description
                todo.completed = todo_update.completed
                todo.created_at = datetime.now()  # Refresh timestamp
                return todo
        return None

def delete_todo(todo_id: int) -> bool:
    global todos
    with lock:
        initial_len = len(todos)
        todos = [t for t in todos if t.id != todo_id]
        return len(todos) < initial_len
