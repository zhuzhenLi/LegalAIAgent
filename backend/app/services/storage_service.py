import os
import uuid
from typing import Optional

class LocalStorageService:
    """本地文件存储服务"""
    
    def __init__(self, upload_dir: str = "temp_uploads"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_file(self, file_data: bytes, filename: Optional[str] = None) -> str:
        """
        保存文件到本地存储
        
        Args:
            file_data: 文件二进制数据
            filename: 原始文件名（可选）
            
        Returns:
            str: 文件存储路径
        """
        # 生成唯一文件名
        if filename:
            file_id = str(uuid.uuid4())
            ext = os.path.splitext(filename)[1]
            unique_filename = f"{file_id}{ext}"
        else:
            unique_filename = f"{uuid.uuid4()}.bin"
        
        # 构建文件路径
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(file_data)
        
        return file_path
    
    async def get_file(self, file_path: str) -> bytes:
        """
        从本地存储获取文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bytes: 文件二进制数据
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        with open(file_path, "rb") as f:
            return f.read()
    
    async def delete_file(self, file_path: str) -> bool:
        """
        从本地存储删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否成功删除
        """
        if not os.path.exists(file_path):
            return False
        
        os.remove(file_path)
        return True 