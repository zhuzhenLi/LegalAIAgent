
# Legal AI Assistant

A sophisticated legal document analysis and AI assistant platform that helps legal professionals analyze documents, extract insights, and get answers to legal questions.

![WechatIMG8](https://github.com/user-attachments/assets/3ab93583-a23d-44b7-8d79-bb4d2dbfa771)

## 📋 Overview

Legal AI Assistant is a web application that combines document processing capabilities with an AI-powered chat interface to help legal professionals work more efficiently. The system allows users to upload legal documents, analyze their content, and interact with an AI assistant that can answer questions based on the uploaded documents and general legal knowledge.

## 🌟 Features

- **User Authentication**: Secure login and registration system
- **Document Management**: Upload, view, and manage legal documents
- **Document Analysis**: Extract key information from legal documents
- **AI Chat Interface**: Interact with an AI assistant for legal questions
- **Session Management**: Maintain conversation history across sessions
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Project Structure

### System Architecture
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Frontend   │───▶│  Backend    │───▶│  Database   │
│  (React)    │◀───│  (FastAPI)  │◀───│(PostgreSQL)│
└─────────────┘   └─────────────┘   └─────────────┘
        │
        ▼
┌─────────────┐
│File Storage │
│  (Local)    │
└─────────────┘
```

### Frontend Structure (React)
```
frontend/
├── public/ # Static files
├── src/
│ ├── components/ # Reusable UI components
│ │ ├── ChatBox.js # Chat interface component
│ │ ├── DocumentList.js # Document listing component
│ │ ├── LoginForm.js # Authentication form
│ │ ├── Navbar.js # Navigation component
│ │ └── UploadBox.js # Document upload component
│ ├── pages/ # Page components
│ │ ├── Dashboard.js # Main dashboard page
│ │ ├── Login.js # Login page
│ │ └── Register.js # Registration page
│ ├── services/ # API service functions
│ │ ├── auth.js # Authentication API calls
│ │ ├── documents.js # Document API calls
│ │ └── chat.js # Chat API calls
│ ├── context/ # React context providers
│ ├── utils/ # Utility functions
│ ├── App.js # Main application component
│ └── index.js # Application entry point
└── package.json # Dependencies and scripts
 ```
### Backend Structure (FastAPI)
```
backend/
├── app/
│ ├── routers/ # API route definitions
│ │ ├── auth.py # Authentication routes
│ │ ├── document.py # Document management routes
│ │ ├── session.py # Chat session routes
│ │ └── message.py # Chat message routes
│ ├── services/ # Business logic
│ │ ├── auth_service.py # Authentication service
│ │ ├── chat_service.py # Chat processing service
│ │ ├── document_service.py # Document processing
│ │ └── pdf_service.py # PDF text extraction
│ ├── db/ # Database related code
│ │ ├── models/ # SQLAlchemy ORM models
│ │ │ ├── user.py # User model
│ │ │ ├── document.py # Document model
│ │ │ ├── session.py # Chat session model
│ │ │ └── message.py # Chat message model
│ │ └── repositories/ # Database operations
│ │ ├── user_repository.py
│ │ ├── document_repository.py
│ │ ├── session_repository.py
│ │ └── message_repository.py
│ ├── schemas/ # Pydantic models for validation
│ ├── core/ # Core application code
│ │ ├── config.py # Application configuration
│ │ ├── security.py # Security utilities
│ │ └── dependencies.py # FastAPI dependencies
│ ├── database.py # Database connection
│ └── main.py # Application entry point
├── init_user.py # User initialization script
├── setup_db.py # Database setup script
├── test_db_connection.py # Database connection test
├── diagnose_db.py # Database diagnostic tool
└── requirements.txt # Python dependencies

```
### Database Structure (PostgreSQL)

The application uses PostgreSQL with the following table structure:

#### Users Table
#### Sessions Table
#### Messages Table
#### Documents Table


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Zhuzhen Li** 

## 🙏 Acknowledgments

- FastAPI for the excellent Python web framework
- React for the frontend library
- PostgreSQL for the reliable database system
- All open-source libraries used in this project