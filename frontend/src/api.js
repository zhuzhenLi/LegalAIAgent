import axios from 'axios';
// import io from 'socket.io-client';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
axios.defaults.baseURL = API_URL;
// let socket = null;

export const uploadFiles = async (files, taskType) => {
  try {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    formData.append('task_type', taskType);
    
    const response = await axios.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    console.log('Upload response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error uploading files:', error);
    throw error;
  }
};

export const processDocument = async (documentIds, taskType) => {
  try {
    console.log("Processing document with IDs:", documentIds, "and task type:", taskType);
    
    // 确保 documentIds 是数组
    const docIds = Array.isArray(documentIds) ? documentIds : [documentIds];
    
    const response = await axios.post('/ai/process', {
      document_ids: docIds,
      task_type: taskType
    });
    
    console.log("Process response:", response.data);
    return response.data;
  } catch (error) {
    console.error('Error processing document:', error);
    if (error.response) {
      console.error("Error response data:", error.response.data);
    }
    throw error;
  }
};

export const getResult = async (fileId) => {
  console.log("Calling getResult API for fileId:", fileId);
  try {
    const response = await axios.get(`/result/${fileId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting result:', error);
    throw error;
  }
};

export const connectWebSocket = (sessionId, onMessage) => {
  console.log('WebSocket connection disabled');
  return () => {};
};

export const pollForResults = async (taskId, onUpdate) => {
  try {
    let completed = false;
    
    while (!completed) {
      const response = await axios.get(`/ai/tasks/${taskId}`);
      const { status, result } = response.data;
      
      if (onUpdate) {
        onUpdate(result?.current_output || '');
      }
      
      if (status === 'completed' || status === 'failed') {
        completed = true;
        return response.data;
      }
      
      // 等待 1 秒后再次轮询
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  } catch (error) {
    console.error('Error polling for results:', error);
    throw error;
  }
};

export const sendMessage = async (sessionId, content) => {
  try {
    const response = await axios.post(`/sessions/${sessionId}/messages`, {
      content,
      sender: 'user'
    });
    
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const getMessages = async (sessionId) => {
  try {
    const response = await axios.get(`/sessions/${sessionId}/messages`);
    return response.data;
  } catch (error) {
    console.error('Error getting messages:', error);
    throw error;
  }
}; 