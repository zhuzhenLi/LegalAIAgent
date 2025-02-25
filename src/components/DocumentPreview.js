import React from 'react';

const DocumentPreview = ({ file, onClose }) => {
  // 对于PDF文件，使用PDF.js或嵌入式预览
  if (file.type === 'application/pdf') {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full h-5/6 flex flex-col">
          <div className="flex justify-between items-center p-4 border-b border-secondary-200">
            <h2 className="text-lg font-medium text-secondary-900">{file.name}</h2>
            <button onClick={onClose} className="text-secondary-500 hover:text-secondary-700">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="flex-1 overflow-hidden">
            <iframe
              src={URL.createObjectURL(file)}
              className="w-full h-full"
              title={file.name}
            />
          </div>
        </div>
      </div>
    );
  }
  
  // 对于图片文件
  if (file.type.startsWith('image/')) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full flex flex-col">
          <div className="flex justify-between items-center p-4 border-b border-secondary-200">
            <h2 className="text-lg font-medium text-secondary-900">{file.name}</h2>
            <button onClick={onClose} className="text-secondary-500 hover:text-secondary-700">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="p-4 flex items-center justify-center">
            <img
              src={URL.createObjectURL(file)}
              alt={file.name}
              className="max-w-full max-h-[70vh] object-contain"
            />
          </div>
        </div>
      </div>
    );
  }
  
  // 对于其他文件类型，显示无法预览的消息
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium text-secondary-900">{file.name}</h2>
          <button onClick={onClose} className="text-secondary-500 hover:text-secondary-700">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="text-center py-8">
          <svg className="mx-auto h-12 w-12 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="mt-2 text-secondary-600">Preview not available for this file type.</p>
        </div>
        <div className="flex justify-end mt-4">
          <button
            onClick={onClose}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-700 hover:bg-primary-800"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default DocumentPreview; 