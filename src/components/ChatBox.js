import React, { useEffect, useRef } from 'react';

const ChatBox = ({ messages, isTyping }) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full">
          <div className="text-center text-secondary-500">
            <svg className="mx-auto h-12 w-12 text-secondary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium">No messages</h3>
            <p className="mt-1 text-sm">Upload files and select a task to get started</p>
          </div>
        </div>
      ) : (
        messages.map((message, index) => (
          <div 
            key={index} 
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`max-w-3xl rounded-lg px-4 py-2 ${
                message.sender === 'user' 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-secondary-100 text-secondary-800'
              }`}
            >
              <div className="whitespace-pre-wrap">
                {message.text}
              </div>
            </div>
          </div>
        ))
      )}
      
      {isTyping && (
        <div className="flex justify-start">
          <div className="max-w-3xl rounded-lg px-4 py-2 bg-secondary-100 text-secondary-800">
            <div className="typing-animation">
              Generating response
            </div>
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatBox; 