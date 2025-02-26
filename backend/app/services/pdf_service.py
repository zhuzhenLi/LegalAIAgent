import fitz  # PyMuPDF库，用于处理PDF文件
from typing import List
import PyPDF2
import os
import re
import docx  # 用于处理Word文档
from PIL import Image  # 用于处理图片
import pytesseract  # 用于OCR识别

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

# 从Word文档中提取文本
def extract_text_from_docx(file_path):
    """
    从Word文档中提取文本
    
    Args:
        file_path: Word文档路径
        
    Returns:
        str: 提取的文本
    """
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"提取Word文档文本时出错: {str(e)}")
        return f"提取Word文档文本时出错: {str(e)}"

# 从图片中提取文本（OCR）
def extract_text_from_image(file_path):
    """
    从图片中提取文本（OCR）
    
    Args:
        file_path: 图片路径
        
    Returns:
        str: 提取的文本
    """
    try:
        # 打开图片
        image = Image.open(file_path)
        
        # 使用pytesseract进行OCR识别
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        
        # 清理文本
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    except Exception as e:
        print(f"从图片提取文本时出错: {str(e)}")
        return f"从图片提取文本时出错: {str(e)}"

# 独立的PDF文本提取函数
# 这个函数被路由直接调用，不需要创建PDFService实例
def extract_text_from_pdf(file_path):
    """
    从PDF文件中提取文本
    
    Args:
        file_path: PDF文件路径
        
    Returns:
        str: 提取的文本
    """
    try:
        # 检查文件类型
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # 处理TXT文件
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text
            
        # 处理PDF文件
        elif file_extension == '.pdf':
            try:
                # 首先尝试使用PyMuPDF
                with fitz.open(file_path) as doc:
                    text = ""
                    for page in doc:
                        try:
                            # 尝试不同的方法名
                            if hasattr(page, 'extract_text'):
                                text += page.extract_text() + "\n"
                            elif hasattr(page, 'get_text'):
                                text += page.get_text() + "\n"
                            else:
                                raise AttributeError("No text extraction method found")
                        except Exception as inner_e:
                            print(f"Error extracting text from page: {str(inner_e)}")
                    
                    # 清理文本
                    text = re.sub(r'\s+', ' ', text).strip()
                    return text
            except Exception as e:
                print(f"PyMuPDF extraction failed: {str(e)}")
                # 如果PyMuPDF失败，尝试使用PyPDF2
                try:
                    with open(file_path, 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        text = ""
                        for page_num in range(len(reader.pages)):
                            text += reader.pages[page_num].extract_text() + "\n"
                        
                        # 清理文本
                        text = re.sub(r'\s+', ' ', text).strip()
                        return text
                except Exception as e2:
                    print(f"PyPDF2 extraction failed: {str(e2)}")
                    return f"无法提取PDF文本: {str(e)} / {str(e2)}"
            
        # 处理Word文档
        elif file_extension in ['.doc', '.docx']:
            if file_extension == '.docx':
                return extract_text_from_docx(file_path)
            else:
                # .doc文件需要转换为.docx或使用其他库处理
                return "Legacy .doc format is not fully supported. Please convert to .docx"
            
        # 处理图片文件
        elif file_extension in ['.jpg', '.jpeg', '.png']:
            return extract_text_from_image(file_path)
            
        else:
            return f"Unsupported file type: {file_extension}"
            
    except Exception as e:
        print(f"提取文本时出错: {str(e)}")
        return f"提取文本时出错: {str(e)}"