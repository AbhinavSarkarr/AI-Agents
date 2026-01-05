import axios from "axios";

const API_URL = "/api/tasks";

export const fetchTasks = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const createTask = async (taskData) => {
  const response = await axios.post(API_URL, taskData);
  return response.data;
};

export const updateTask = async (taskId, taskData) => {
  const response = await axios.put(`${API_URL}/${taskId}`, taskData);
  return response.data;
};

export const deleteTask = async (taskId) => {
  await axios.delete(`${API_URL}/${taskId}`);
};

export const fetchCompletedTasks = async () => {
  const response = await axios.get("/api/analytics/completed");
  return response.data;
};

export const fetchOutstandingTasks = async () => {
  const response = await axios.get("/api/analytics/outstanding");
  return response.data;
};