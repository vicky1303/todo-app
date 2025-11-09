import React from 'react';

const TodoItem = ({ todo, onToggle, onDelete }) => {
  return (
    <li className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        <h3>{todo.title}</h3>
        {todo.description && <p>{todo.description}</p>}
        <small>Created: {new Date(todo.created_at).toLocaleDateString()}</small>
      </div>
      <div className="todo-actions">
        <button className="toggle-btn" onClick={onToggle}>
          {todo.completed ? 'Undo' : 'Complete'}
        </button>
        <button className="delete-btn" onClick={onDelete}>
          Delete
        </button>
      </div>
    </li>
  );
};

export default TodoItem;
