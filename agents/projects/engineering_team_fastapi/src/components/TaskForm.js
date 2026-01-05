import React, { useState, useContext } from "react";
import UserContext from "../context/UserContext";
import { createTask } from "../services/apiService";

const TaskForm = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const { dispatch } = useContext(UserContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newTask = await createTask({ title, description });
    dispatch({ type: "SET_TASKS", payload: [...tasks, newTask] });
    setTitle("");
    setDescription("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Task Title" required />
      <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Task Description" required />
      <button type="submit">Add Task</button>
    </form>
  );
};

export default TaskForm;