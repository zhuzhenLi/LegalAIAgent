import React, { useState, useEffect } from 'react';
import UploadBox from './components/UploadBox';
import ChatBox from './components/ChatBox';
import ChatHistory from './components/ChatHistory';
import ActionButtons from './components/ActionButtons';
import { uploadFiles, connectWebSocket, pollForResults, processDocument } from './api';
import Logo from './components/Logo';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const TASK_TYPES = [
  { id: 'TASK1', name: 'Analyze Documents' },
  { id: 'TASK2', name: 'Build Persuasive Arguments' },
  { id: 'TASK3', name: 'Refine Legal Strategy' },
  { id: 'TASK4', name: 'Ask About the Law' },
  { id: 'TASK5', name: 'Find a Case' }
];

function App() {
  const [files, setFiles] = useState([]);
  const [taskType, setTaskType] = useState('TASK1');
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [currentResponse, setCurrentResponse] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { id: 1, title: 'Legal Document Generation', date: '2023-12-01', active: true },
    { id: 2, title: 'Defense Analysis', date: '2023-11-28', active: false },
    { id: 3, title: 'Legal Consultation', date: '2023-11-25', active: false },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showHelp, setShowHelp] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showExport, setShowExport] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const [showSidebar, setShowSidebar] = useState(!isMobile);
  const [filesUploaded, setFilesUploaded] = useState(false);

  // Handle text updates from WebSocket or polling
  const handleTextUpdate = (text) => {
    setCurrentResponse(text);
    setIsTyping(true);
  };

  // When a complete response is received, add it to the message list
  useEffect(() => {
    if (!isProcessing && currentResponse) {
      setMessages(prev => [...prev, { sender: 'ai', text: currentResponse }]);
      setCurrentResponse('');
      setIsTyping(false);
    }
  }, [isProcessing, currentResponse]);

  const handleSubmit = async () => {
    if (files.length === 0) {
      alert('Please upload at least one PDF file');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      setIsProcessing(true);
      setIsTyping(true);
      
      // 添加用户消息，显示上传的文件名
      const fileNames = files.map(file => file.name).join(', ');
      const userMessage = `Uploaded files: ${fileNames}`;
      
      setMessages(prev => [...prev, { sender: 'user', text: userMessage }]);
      
      // 上传文件到后端
      const response = await uploadFiles(files, taskType);
      
      // 设置文件已上传标志
      setFilesUploaded(true);
      
      // 显示收到的PDF名称
      if (response.documents && response.documents.length > 0) {
        const receivedFiles = response.documents.map(doc => doc.filename).join(', ');
        setMessages(prev => [...prev, { 
          sender: 'ai', 
          text: `Received PDF files: ${receivedFiles}` 
        }]);
        
        const fileId = response.documents[0].id;
        
        // 处理文档
        await processDocument(fileId, taskType);
        
        // 轮询结果
        await pollForResults(fileId, handleTextUpdate);
      } else {
        throw new Error('No document ID returned from server');
      }
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsLoading(false);
      setIsProcessing(false);
    }
  };

  const handleClear = () => {
    setFiles([]);
    setCurrentResponse('');
    setIsTyping(false);
  };

  const handleNewChat = () => {
    setMessages([]);
    setFiles([]);
    setChatHistory(prev => [
      { id: Date.now(), title: 'New Conversation', date: new Date().toISOString().split('T')[0], active: true },
      ...prev.map(chat => ({ ...chat, active: false }))
    ]);
  };

  const handleChatSelect = (id) => {
    setChatHistory(prev => prev.map(chat => ({
      ...chat,
      active: chat.id === id
    })));
    // Here you should load the messages for the selected chat
    // loadChatMessages(id);
  };

  const handleActionButton = (taskId, actionLabel) => {
    console.log("Action button clicked:", taskId, actionLabel);
    if (!files.length) {
      setError("Please upload a document first");
      return;
    }
    
    // 显示用户选择的操作和文件名
    const fileNames = files.map(file => file.name).join(', ');
    setMessages(prev => [...prev, { 
      sender: 'user', 
      text: `Please ${actionLabel} for files: ${fileNames}` 
    }]);
    
    // 处理文档
    handleProcessDocument(taskId);
  };

  const handleProcessDocument = async (taskType) => {
    console.log("Processing document with task type:", taskType);
    try {
      setIsLoading(true);
      setError(null);
      setIsProcessing(true);
      setIsTyping(true);
      
      // 上传文件到后端
      const response = await uploadFiles(files, taskType);
      
      // 设置文件已上传标志
      setFilesUploaded(true);
      
      // 显示收到的PDF名称
      if (response.documents && response.documents.length > 0) {
        const receivedFiles = response.documents.map(doc => doc.filename).join(', ');
        setMessages(prev => [...prev, { 
          sender: 'ai', 
          text: `Received PDF files: ${receivedFiles}` 
        }]);
        
        const fileId = response.documents[0].id;
        
        // 处理文档
        await processDocument(fileId, taskType);
        
        // 轮询结果
        await pollForResults(fileId, handleTextUpdate);
      } else {
        throw new Error('No document ID returned from server');
      }
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsLoading(false);
      setIsProcessing(false);
    }
  };

  const handleSendMessage = () => {
    if (!inputMessage.trim() && !filesUploaded) return;
    
    // 如果有输入消息，则发送消息
    if (inputMessage.trim()) {
      setMessages(prev => [...prev, { sender: 'user', text: inputMessage }]);
      setInputMessage('');
      
      // 这里应该调用API发送消息
      // sendMessageToBackend(inputMessage);
    } 
    // 如果没有输入消息但有上传文件，则处理文件
    else if (filesUploaded) {
      // 使用默认任务类型处理文件
      handleProcessDocument(taskType);
    }
  };

  // 添加键盘快捷键处理
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl/Cmd + / 打开帮助
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        setShowHelp(true);
      }
      
      // Ctrl/Cmd + N 新建对话
      if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        handleNewChat();
      }
      
      // Esc 关闭模态框
      if (e.key === 'Escape') {
        setShowSettings(false);
        setShowHelp(false);
        setShowExport(false);
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // 监听窗口大小变化
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (!mobile) setShowSidebar(true);
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="flex h-screen bg-secondary-50">
      {/* 移动版侧边栏切换按钮 */}
      {isMobile && (
        <button
          onClick={() => setShowSidebar(!showSidebar)}
          className="fixed z-20 bottom-4 left-4 p-2 rounded-full bg-primary-600 text-white shadow-lg"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {showSidebar ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      )}
      
      {/* 左侧边栏 - 条件渲染 */}
      {(showSidebar || !isMobile) && (
        <div className={`${isMobile ? 'fixed inset-0 z-10 w-64' : 'w-64'} bg-white border-r border-secondary-200 flex flex-col`}>
          <div className="p-4 border-b border-secondary-200 bg-primary-700">
            <Logo size="md" variant="default" />
          </div>
          <ChatHistory 
            history={chatHistory} 
            onSelect={handleChatSelect}
            onNewChat={handleNewChat}
          />
        </div>
      )}
      
      {/* 主内容区域 */}
      <div className={`flex-1 flex flex-col ${isMobile && showSidebar ? 'opacity-50' : ''}`}>
        <header className="bg-white shadow-sm p-4 border-b border-secondary-200">
          <h2 className="text-lg font-medium text-secondary-800">
            {chatHistory.find(chat => chat.active)?.title || 'New Conversation'}
          </h2>
        </header>
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <ChatBox messages={messages} isTyping={isTyping} />
          
          {/* Action buttons area */}
          <div className="p-4 bg-white border-t border-secondary-200">
            <ActionButtons onAction={handleActionButton} />
          </div>
          
          {/* Bottom input area */}
          <div className="p-4 bg-secondary-50 border-t border-secondary-200">
            <div className="flex items-end space-x-3">
              <div className="flex-1">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Type your message here..."
                  className="block w-full rounded-md border-secondary-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm resize-none"
                  rows={2}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSendMessage();
                    }
                  }}
                />
              </div>
              
              <button
                onClick={handleSendMessage}
                disabled={isProcessing || (!inputMessage.trim() && !filesUploaded)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-700 hover:bg-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* 右侧边栏 - 在移动版隐藏 */}
      {!isMobile && (
        <div className="w-80 bg-white border-l border-secondary-200 flex flex-col">
          <div className="p-4 border-b border-secondary-200 bg-primary-700">
            <h2 className="text-lg font-medium text-white">File Upload</h2>
          </div>
          <div className="flex-1 p-4 overflow-y-auto">
            <UploadBox files={files} setFiles={setFiles} />
          </div>
        </div>
      )}

      {/* Error notification */}
      {error && (
        <div className="p-4 bg-red-50 border-l-4 border-red-500 mb-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
            <div className="ml-auto pl-3">
              <div className="-mx-1.5 -my-1.5">
                <button
                  onClick={() => setError(null)}
                  className="inline-flex rounded-md p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  <span className="sr-only">Dismiss</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App; 