import React from 'react';

const ChatHistory = ({ history, onSelect, onNewChat }) => {
  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div className="p-4">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          New Conversation
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        <div className="px-3 py-2 text-xs font-semibold text-secondary-500 uppercase tracking-wider">
          This Month
        </div>
        <ul className="space-y-1 px-2">
          {history.map(chat => (
            <li key={chat.id}>
              <button
                onClick={() => onSelect(chat.id)}
                className={`w-full text-left px-3 py-2 rounded-md text-sm ${
                  chat.active 
                    ? 'bg-primary-100 text-primary-900' 
                    : 'text-secondary-700 hover:bg-secondary-100'
                }`}
              >
                <div className="font-medium truncate">{chat.title}</div>
                <div className="text-xs text-secondary-500">{chat.date}</div>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChatHistory; 