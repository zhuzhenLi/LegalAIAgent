import axios from 'axios';
import io from 'socket.io-client';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
let socket = null;

export const uploadFiles = async (files, taskType = "") => {
  const formData = new FormData();
  
  console.log("Files to upload:", files);
  
  files.forEach(file => {
    formData.append('files', file);
  });
  
  if (taskType) {
    formData.append('task_type', taskType);
  }
  
  console.log("Task type:", taskType);
  
  try {
    console.log("Sending request to:", `${API_URL}/documents/upload`);
    const response = await axios.post(`${API_URL}/documents/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log("Upload response:", response.data);
    return response.data;
  } catch (error) {
    console.error('Error uploading files:', error.response ? error.response.data : error.message);
    throw error;
  }
};

export const processDocument = async (fileId, taskType) => {
  console.log("Calling processDocument API with:", { fileId, taskType });
  try {
    const response = await axios.post(`${API_URL}/ai/process`, {
      file_id: fileId,
      task_type: taskType
    });
    return response.data;
  } catch (error) {
    console.error('Error processing document:', error);
    throw error;
  }
};

export const getResult = async (fileId) => {
  console.log("Calling getResult API for fileId:", fileId);
  try {
    const response = await axios.get(`${API_URL}/ai/result/${fileId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting result:', error);
    throw error;
  }
};

export const connectWebSocket = (sessionId, onMessage) => {
  if (socket) {
    socket.disconnect();
  }
  
  socket = io(API_URL);
  
  socket.on('connect', () => {
    console.log('WebSocket connected');
    socket.emit('join', { session_id: sessionId });
  });
  
  socket.on('message', (data) => {
    onMessage(data.text);
  });
  
  socket.on('disconnect', () => {
    console.log('WebSocket disconnected');
  });
  
  return () => {
    socket.disconnect();
  };
};

export const pollForResults = async (fileId, onUpdate) => {
  let completed = false;
  let text = '';
  
  while (!completed) {
    try {
      const response = await getResult(fileId);
      
      if (response.content && response.content !== text) {
        text = response.content;
        onUpdate(text);
      }
      
      if (response.status === 'completed') {
        completed = true;
      } else {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    } catch (error) {
      console.error('Error polling for results:', error);
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
}; 