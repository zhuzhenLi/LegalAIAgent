import axios from 'axios';
import io from 'socket.io-client';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
let socket = null;

export const uploadFiles = async (files, taskType) => {
  const formData = new FormData();
  
  files.forEach(file => {
    formData.append('files', file);
  });
  
  formData.append('task_type', taskType);
  
  try {
    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading files:', error);
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

export const pollForResults = async (sessionId, onUpdate) => {
  let completed = false;
  let text = '';
  
  while (!completed) {
    try {
      const response = await axios.get(`${API_URL}/status/${sessionId}`);
      const { status, partial_text } = response.data;
      
      if (partial_text && partial_text !== text) {
        text = partial_text;
        onUpdate(text);
      }
      
      if (status === 'completed') {
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