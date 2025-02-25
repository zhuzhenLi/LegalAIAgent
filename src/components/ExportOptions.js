import React from 'react';

const ExportOptions = ({ messages, onClose }) => {
  const exportAsPDF = () => {
    // PDF导出逻辑
    console.log('Exporting as PDF...');
    onClose();
  };
  
  const exportAsText = () => {
    const text = messages
      .map(msg => `${msg.sender === 'user' ? 'You' : 'Hazel'}: ${msg.text}`)
      .join('\n\n');
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `hazel-conversation-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    onClose();
  };
  
  const shareViaEmail = () => {
    const subject = 'Hazel Legal Assistant Conversation';
    const body = messages
      .map(msg => `${msg.sender === 'user' ? 'You' : 'Hazel'}: ${msg.text}`)
      .join('\n\n');
    
    window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    onClose();
  };
  
  return (
    <div className="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10">
      <div className="py-1" role="menu">
        <button
          onClick={exportAsPDF}
          className="block w-full text-left px-4 py-2 text-sm text-secondary-700 hover:bg-secondary-100"
          role="menuitem"
        >
          Export as PDF
        </button>
        <button
          onClick={exportAsText}
          className="block w-full text-left px-4 py-2 text-sm text-secondary-700 hover:bg-secondary-100"
          role="menuitem"
        >
          Export as Text
        </button>
        <button
          onClick={shareViaEmail}
          className="block w-full text-left px-4 py-2 text-sm text-secondary-700 hover:bg-secondary-100"
          role="menuitem"
        >
          Share via Email
        </button>
      </div>
    </div>
  );
};

export default ExportOptions; 