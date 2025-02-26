import React, { useCallback, useRef } from 'react';
import { useDropzone } from 'react-dropzone';

const UploadBox = ({ files, setFiles, onDrop: propOnDrop, onFileChange, fileInputRef: externalFileInputRef, uploadedFiles = [] }) => {
  // 如果没有提供外部ref，则创建一个内部ref
  const internalFileInputRef = useRef(null);
  const fileInputRef = externalFileInputRef || internalFileInputRef;

  const onDrop = useCallback(acceptedFiles => {
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

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({ 
    onDrop,
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

  // 手动触发文件选择
  const handleClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="w-full flex flex-col h-full">
      <div 
        className={`flex-1 flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-lg text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-secondary-300 hover:border-primary-400'}`}
        onClick={handleClick}
        onDragOver={(e) => {
          e.preventDefault();
          e.stopPropagation();
        }}
        onDragEnter={(e) => {
          e.preventDefault();
          e.stopPropagation();
        }}
        onDragLeave={(e) => {
          e.preventDefault();
          e.stopPropagation();
        }}
        onDrop={(e) => {
          e.preventDefault();
          e.stopPropagation();
          const files = Array.from(e.dataTransfer.files);
          onDrop(files);
        }}
      >
        <input 
          type="file"
          ref={fileInputRef}
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
          multiple
          accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.txt"
        />
        
        <svg className="mx-auto h-12 w-12 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        
        <p className="mt-2 text-secondary-600">
          {isDragActive ? 
            'Drop files here...' : 
            'Drag and drop files here, or click to select files'}
        </p>
        <p className="text-xs text-secondary-500 mt-1">
          Supports PDF, Word, images and more
        </p>
      </div>

      {fileRejections.length > 0 && (
        <div className="mt-2 text-sm text-red-600">
          {fileRejections.map(({ file, errors }) => (
            <div key={file.path}>
              <strong>{file.path}</strong> - {errors.map(e => e.message).join(', ')}
            </div>
          ))}
        </div>
      )}

      {files.length > 0 && (
        <div className="mt-4">
          <h3 className="text-sm font-medium text-secondary-700">Selected Files:</h3>
          <ul className="mt-2 divide-y divide-secondary-200">
            {files.map((file, index) => (
              <li key={index} className="py-2 flex items-center justify-between">
                <div className="flex items-center">
                  {isFileUploaded(file.name) && (
                    <span className="mr-2 text-green-500">✅</span>
                  )}
                  {getFileIcon(file.name)}
                  <span className="ml-2 text-sm text-secondary-700">{file.name}</span>
                  <span className="ml-2 text-xs text-secondary-500">
                    ({Math.round(file.size / 1024)} KB)
                  </span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(index);
                  }}
                  className="text-secondary-500 hover:text-secondary-700"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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