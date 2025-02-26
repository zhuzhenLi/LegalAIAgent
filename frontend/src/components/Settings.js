import React, { useState } from 'react';

const Settings = ({ isOpen, onClose, onSave }) => {
  const [theme, setTheme] = useState('blue'); // blue, green, purple
  
  const handleSave = () => {
    onSave({ theme });
    onClose();
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium text-secondary-900">Settings</h2>
          <button onClick={onClose} className="text-secondary-500 hover:text-secondary-700">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-secondary-700 mb-2">Theme</label>
          <div className="flex space-x-4">
            <button
              onClick={() => setTheme('blue')}
              className={`w-8 h-8 rounded-full ${theme === 'blue' ? 'ring-2 ring-offset-2 ring-primary-500' : ''}`}
              style={{ backgroundColor: '#0369a1' }}
            />
            <button
              onClick={() => setTheme('green')}
              className={`w-8 h-8 rounded-full ${theme === 'green' ? 'ring-2 ring-offset-2 ring-primary-500' : ''}`}
              style={{ backgroundColor: '#047857' }}
            />
            <button
              onClick={() => setTheme('purple')}
              className={`w-8 h-8 rounded-full ${theme === 'purple' ? 'ring-2 ring-offset-2 ring-primary-500' : ''}`}
              style={{ backgroundColor: '#6d28d9' }}
            />
          </div>
        </div>
        
        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="mr-2 px-4 py-2 border border-secondary-300 text-sm font-medium rounded-md text-secondary-700 bg-white hover:bg-secondary-50"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-700 hover:bg-primary-800"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings; 