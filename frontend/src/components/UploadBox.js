import React, { useCallback, useRef, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const UploadBox = ({ files, setFiles, onDrop: propOnDrop, onFileChange, fileInputRef: externalFileInputRef, uploadedFiles = [], userId, sessionId, onUploadSuccess }) => {
  // 如果没有提供外部ref，则创建一个内部ref
  const internalFileInputRef = useRef(null);
  const fileInputRef = externalFileInputRef || internalFileInputRef;

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleDrop = useCallback(acceptedFiles => {
    console.log("Files dropped:", acceptedFiles);
    if (propOnDrop) {
      propOnDrop(acceptedFiles);
    } else {
      setFiles(prevFiles => [...prevFiles, ...acceptedFiles]);
    }
  }, [propOnDrop, setFiles]);

  const handleFileInputChange = (e) => {
    console.log("File input changed:", e.target.files);
    if (onFileChange) {
      onFileChange(e);
    } else if (setFiles) {
      setFiles(Array.from(e.target.files));
    }
  };

  // 添加点击处理函数
  const handleClick = () => {
    fileInputRef.current.click();
  };

  // eslint-disable-next-line no-unused-vars
  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({ 
    onDrop: handleDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxSize: 10485760, // 10MB
    maxFiles: 5
  });

  const removeFile = (index) => {
    if (setFiles) {
      setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
    }
  };

  const getFileIcon = (filename) => {
    const ext = filename.split('.').pop().toLowerCase();
    
    if (ext === 'pdf') {
      return (
        <svg className="w-5 h-5 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
        </svg>
      );
    } else if (['jpg', 'jpeg', 'png'].includes(ext)) {
      return (
        <svg className="w-5 h-5 text-accent-500" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
        </svg>
      );
    } else if (['doc', 'docx'].includes(ext)) {
      return (
        <svg className="w-5 h-5 text-primary-700" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
        </svg>
      );
    } else if (ext === 'txt') {
      return (
        <svg className="w-5 h-5 text-secondary-600" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 2v8h8V6H6z" clipRule="evenodd" />
        </svg>
      );
    }
    
    return (
      <svg className="w-5 h-5 text-secondary-500" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
      </svg>
    );
  };

  // 检查文件是否已上传成功
  const isFileUploaded = (filename) => {
    if (!uploadedFiles || uploadedFiles.length === 0) {
      return false;
    }
    
    // 尝试多种可能的匹配方式
    return uploadedFiles.some(file => 
      file.filename === filename || // 完全匹配
      file.filename.endsWith(filename) || // 文件名可能包含路径
      filename.endsWith(file.filename) // 或者反过来
    );
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };
  
  const handleUpload = async () => {
    if (!file) return;
    
    setUploading(true);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);
    if (sessionId) {
      formData.append('session_id', sessionId);
    }
    
    try {
      const response = await axios.post('/api/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      setUploading(false);
      setFile(null);
      
      if (onUploadSuccess) {
        onUploadSuccess(response.data);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div 
        onClick={handleClick}
        className="border-2 border-dashed border-secondary-300 rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer hover:bg-secondary-50"
      >
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
          multiple
          accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.txt"
        />
        <svg className="w-10 h-10 text-secondary-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p className="text-secondary-600 text-center">
          {isDragActive ? 'Drop files here' : 'Drag and drop files here, or click to select files'}
        </p>
        <p className="text-xs text-secondary-500 mt-1">
          Supports PDF, Word, images and more
        </p>
      </div>
      
      {files.length > 0 && (
        <div className="border rounded-lg overflow-hidden">
          <div className="bg-secondary-50 px-4 py-2 border-b">
            <h3 className="text-sm font-medium text-secondary-700">Selected Files</h3>
          </div>
          <ul className="divide-y divide-secondary-200">
            {files.map((file, index) => (
              <li key={index} className="px-4 py-3 flex items-center justify-between">
                <div className="flex items-center">
                  {isFileUploaded(file.name) && (
                    <span className="mr-2 text-green-500" role="img" aria-label="Checkmark">✅</span>
                  )}
                  {getFileIcon(file.name)}
                  <span className="ml-2 text-sm text-secondary-700 truncate max-w-xs">{file.name}</span>
                  <span className="ml-2 text-xs text-secondary-500">
                    {(file.size / 1024).toFixed(1)} KB
                  </span>
                </div>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(index);
                  }}
                  className="text-secondary-400 hover:text-secondary-600"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadBox;