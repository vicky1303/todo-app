import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TodoItem from './components/TodoItem';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const { data } = await axios.get(`${API_BASE}/todos`);
      setTodos(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch todos. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.title.trim()) return;

    try {
      const { data } = await axios.post(`${API_BASE}/todos`, newTodo);
      setTodos([...todos, data]);
      setNewTodo({ title: '', description: '' });
    } catch (err) {
      setError('Failed to add todo.');
      console.error(err);
    }
  };

  const toggleTodo = async (id, currentCompleted) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    try {
      const { data } = await axios.put(`${API_BASE}/todos/${id}`, {
        ...todo,
        completed: !currentCompleted
      });
      setTodos(todos.map(t => t.id === id ? data : t));
    } catch (err) {
      setError('Failed to update todo.');
      console.error(err);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API_BASE}/todos/${id}`);
      setTodos(todos.filter(t => t.id !== id));
    } catch (err) {
      setError('Failed to delete todo.');
      console.error(err);
    }
  };

  if (loading) return <div className="loading">Loading todos...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="App">
      <header className="App-header">
        <h1>My Todo List</h1>
        <form onSubmit={addTodo} className="add-form">
          <input
            type="text"
            placeholder="Todo title..."
            value={newTodo.title}
            onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Description (optional)..."
            value={newTodo.description}
            onChange={(e) => setNewTodo({ ...newTodo, description: e.target.value })}
          />
          <button type="submit">Add Todo</button>
        </form>
        <ul className="todo-list">
          {todos.length === 0 ? (
            <li>No todos yet. Add one above!</li>
          ) : (
            todos.map(todo => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onToggle={() => toggleTodo(todo.id, todo.completed)}
                onDelete={() => deleteTodo(todo.id)}
              />
            ))
          )}
        </ul>
        <button onClick={fetchTodos} className="refresh-btn">Refresh</button>
      </header>
    </div>
  );
}

export default App;
