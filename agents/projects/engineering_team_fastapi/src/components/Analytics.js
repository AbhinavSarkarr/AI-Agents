import React, { useEffect, useContext, useState } from "react";
import UserContext from "../context/UserContext";
import { fetchCompletedTasks, fetchOutstandingTasks } from "../services/apiService";

const Analytics = () => {
  const { state } = useContext(UserContext);
  const [completed, setCompleted] = useState([]);
  const [outstanding, setOutstanding] = useState([]);

  useEffect(() => {
    const getAnalytics = async () => {
      const completedTasks = await fetchCompletedTasks();
      const outstandingTasks = await fetchOutstandingTasks();
      setCompleted(completedTasks);
      setOutstanding(outstandingTasks);
    };

    getAnalytics();
  }, []);

  return (
    <div>
      <h2>Analytics</h2>
      <div>
        <h3>Completed Tasks</h3>
        <ul>
          {completed.map(task => <li key={task.id}>{task.title}</li>)}
        </ul>
      </div>
      <div>
        <h3>Outstanding Tasks</h3>
        <ul>
          {outstanding.map(task => <li key={task.id}>{task.title}</li>)}
        </ul>
      </div>
    </div>
  );
};

export default Analytics;