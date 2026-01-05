import React, { useContext, useEffect } from "react";
import UserContext from "../context/UserContext";
import TaskItem from "./TaskItem";
import { fetchTasks } from "../services/apiService";

const TaskList = () => {
  const { state, dispatch } = useContext(UserContext);

  useEffect(() => {
    const getTasks = async () => {
      const tasks = await fetchTasks();
      dispatch({ type: "SET_TASKS", payload: tasks });
    };

    getTasks();
  }, [dispatch]);

  return (
    <div>
      <h2>Task List</h2>
      <ul>
        {state.tasks.map(task => (
          <TaskItem key={task.id} task={task} />
        ))}
      </ul>
    </div>
  );
};

export default TaskList;