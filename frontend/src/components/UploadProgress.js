import React from 'react';

const UploadProgress = ({ files, progress }) => {
  if (!files.length || !progress) return null;
  
  return (
    <div className="mt-4">
      <h3 className="text-sm font-medium text-secondary-700 mb-2">Upload Progress</h3>
      <div className="space-y-3">
        {files.map((file, index) => (
          <div key={index} className="flex flex-col">
            <div className="flex justify-between text-xs text-secondary-500 mb-1">
              <span className="truncate max-w-xs">{file.name}</span>
              <span>{progress[file.name] || 0}%</span>
            </div>
            <div className="w-full bg-secondary-200 rounded-full h-1.5">
              <div 
                className="bg-primary-600 h-1.5 rounded-full" 
                style={{ width: `${progress[file.name] || 0}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UploadProgress; 