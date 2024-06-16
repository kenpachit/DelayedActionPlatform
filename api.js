import axios from 'axios';
const BASE_URL = process.env.VUE_APP_BASE_UR;

const handleError = (error, message) => {
  console.error(message, error);
  throw new Error(`${message}. Original error: ${error.message}`);
};

export const fetchActions = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/actions`);
    return response.data;
  } catch (error) {
    handleError(error, 'Error fetching actions');
  }
};

export const createAction = async (actionData) => {
  try {
    const response = await axios.post(`${BASE_URL}/actions`, actionData);
    return response.data;
  } catch (error) {
    handleError(error, 'Error creating action');
  }
};

export const fetchSchedules = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/schedules`);
    return response.data;
  } catch (error) {
    handleError(error, 'Error fetching schedules');
  }
};

export const createSchedule = async (scheduleData) => {
  try {
    const response = await axios.post(`${BASE_URL}/schedules`, scheduleData);
    return response.data;
  } catch (error) {
    handleError(error, 'Error creating schedule');
  }
};

export const updateAction = async (actionId, updateData) => {
  try {
    const response = await axios.patch(`${BASE_URL}/actions/${actionId}`, updateData);
    return response.data;
  } catch (downError) {
    handleError(downError, 'Error updating action');
  }
};

export const deleteAction = async (actionId) => {
  try {
    await axios.delete(`${BASE_URL}/actions/${actionId}`);
    return true;
  } catch (error) {
    handleError(error, 'Error deleting action');
  }
};