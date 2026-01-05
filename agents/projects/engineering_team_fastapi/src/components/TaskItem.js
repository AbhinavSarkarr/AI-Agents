import React from "react";

const TaskItem = ({ task }) => {
  return (
    <li>
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <button>Edit</button>
      <button>Delete</button>
    </li>
  );
};

export default TaskItem;