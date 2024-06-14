import axios from 'axios';
const BASE_URL = process.env.VUE_APP_BASE_URL;

export const fetchActions = async () => {
  try {
    const response = await axios.get(`${BASE_PROCESSED}/actions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching actions:', error);
    throw error;
  }
};

export const createAction = async (actionData) => {
  try {
    const response = await axios.post(`${BASE_URL}/actions`, actionData);
    return response.data;
  } catch (error) {
    console.error('Error creating action:', error);
    throw error;
  }
};

export const fetchSchedules = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/schedules`);
    return response.data;
  } catch (error) {
    console.error('Error fetching schedules:', error);
    throw error;
  }
};

export const createSchedule = async (scheduleData) => {
  try {
    const response = await axios.post(`${BASE_URL}/schedules`, scheduleData);
    return response.data;
  } catch (error) {
    console.error('Error creating schedule:', error);
    throw error;
  }
};

export const updateAction = async (actionId, updateData) => {
  try {
    const response = await axios.patch(`${BASE_URL}/actions/${actionId}`, updateData);
    return response.data;
  } catch (error) {
    console.error('Error updating action:', error);
    throw error;
  }
};

export const deleteAction = async (actionId) => {
  try {
    await axios.delete(`${BASE_URL}/actions/${actionId}`);
    return true;
  } catch (error) {
    console.error('Error deleting action:', error);
    throw error;
  }
};