import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ChatBox = ({ sessionId, userId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  
  // 加载历史消息
  useEffect(() => {
    if (sessionId) {
      loadMessages();
    }
  }, [sessionId]);
  
  const loadMessages = async () => {
    try {
      const response = await axios.get(`/api/sessions/${sessionId}/messages`);
      setMessages(response.data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    }
  };
  
  const sendMessage = async () => {
    if (!input.trim() || !sessionId) return;
    
    setLoading(true);
    
    // 添加用户消息到UI（乐观更新）
    const userMessage = {
      id: 'temp-' + Date.now(),
      content: input,
      sender: 'user',
      created_at: new Date().toISOString()
    };
    
    setMessages([...messages, userMessage]);
    setInput('');
    
    try {
      const response = await axios.post(`/api/sessions/${sessionId}/messages`, {
        content: input,
        sender: 'user'
      });
      
      // 更新消息列表，包括AI响应
      loadMessages();
      
    } catch (error) {
      console.error('Failed to send message:', error);
      // 回滚乐观更新
      setMessages(messages);
      setInput(userMessage.content);
    }
    
    setLoading(false);
  };
  
  return (
    <div className="chat-box">
      <div className="messages">
        {messages.map(message => (
          <div 
            key={message.id} 
            className={`message ${message.sender === 'user' ? 'user-message' : 'ai-message'}`}
          >
            {message.content}
          </div>
        ))}
        {loading && <div className="message ai-message loading">AI is typing...</div>}
      </div>
      
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBox; 