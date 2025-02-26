import fitz  # PyMuPDF库，用于处理PDF文件
from typing import List

# 如果 LocalStorageService 存在，请确保正确导入
# from .storage_service import LocalStorageService

class PDFService:
    def __init__(self):
        # self.storage = LocalStorageService()  # 初始化存储服务
        pass
    
    async def extract_text(self, file_path: str) -> str:
        """从PDF文件中提取文本内容"""
        doc = fitz.open(file_path)  # 打开PDF文件
        text = ""
        for page in doc:  # 遍历每一页
            text += page.get_text()  # 提取文本
        return text
    
    async def save_pdf(self, file_data: bytes, filename: str) -> str:
        """保存PDF文件到存储系统"""
        # return await self.storage.save_file(file_data, filename)
        pass

# 独立的PDF文本提取函数
# 这个函数被路由直接调用，不需要创建PDFService实例
def extract_text_from_pdf(file_path: str) -> str:
    """
    从PDF文件中提取文本
    
    Args:
        file_path: PDF文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {str(e)}")
        return f"Error extracting text: {str(e)}"