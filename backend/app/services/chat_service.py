from ..db.repositories.session_repository import SessionRepository
from ..db.repositories.message_repository import MessageRepository
from datetime import datetime

class ChatService:
    def __init__(self, session_repository: SessionRepository, message_repository: MessageRepository):
        self.session_repository = session_repository
        self.message_repository = message_repository
        
    async def create_session(self, user_id: int, title: str):
        # 创建新会话
        session_data = {
            "title": title,
            "user_id": user_id
        }
        
        session_id = await self.session_repository.create(session_data)
        
        return {
            "id": session_id,
            "title": title,
            "created_at": datetime.now().isoformat()
        }
    
    async def send_message(self, session_id: int, content: str, sender: str = "user"):
        # 保存用户消息
        message_data = {
            "content": content,
            "sender": sender,
            "session_id": session_id
        }
        
        message_id = await self.message_repository.create(message_data)
        
        # 如果是用户消息，生成AI响应
        if sender == "user":
            # 这里调用AI处理逻辑
            ai_response = "这是AI的回复"  # 实际应用中替换为真正的AI响应
            
            # 保存AI响应
            ai_message_data = {
                "content": ai_response,
                "sender": "ai",
                "session_id": session_id
            }
            
            ai_message_id = await self.message_repository.create(ai_message_data)
            
            return {
                "user_message_id": message_id,
                "ai_message_id": ai_message_id,
                "ai_response": ai_response
            }
        
        return {
            "message_id": message_id
        }
    
    async def get_session_messages(self, session_id: int):
        # 获取会话的所有消息
        messages = await self.message_repository.get_by_session(session_id)
        return messages 