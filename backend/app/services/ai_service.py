import openai
import time
import os
from app.config import settings
from app import models
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document, Result, DocumentStatus, TaskType
from app.services.pdf_service import extract_text_from_pdf
from app.services.gpt_service import generate_legal_document
from fastapi import Depends, HTTPException
from datetime import datetime
from sqlalchemy import text
import re

# 配置OpenAI API密钥
openai.api_key = settings.OPENAI_API_KEY

def generate_legal_document(document_id, text_content, task_type, db: Session):
    """
    使用GPT-4o生成法律文书并保存到数据库
    """
    try:
        # 获取文档
        document = db.query(models.Document).filter(models.Document.id == document_id).first()
        if not document:
            print(f"错误: 找不到ID为 {document_id} 的文档")
            return
        
        # 根据任务类型构建提示词
        if task_type == "诉讼书":
            prompt = f"请根据以下材料生成一份完整的诉讼书:\n\n{text_content}"
        elif task_type == "应诉书":
            prompt = f"请根据以下材料生成一份完整的应诉书:\n\n{text_content}"
        else:
            prompt = f"请分析以下法律文件并生成相应的法律文书:\n\n{text_content}"
        
        # 调用GPT-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # 确保使用正确的模型名称
            messages=[
                {"role": "system", "content": "你是一位专业的法律顾问，擅长起草法律文书。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=4000
        )
        
        # 获取生成的内容
        generated_text = response.choices[0].message.content
        
        # 保存结果到数据库
        result = db.query(models.Result).filter(models.Result.document_id == document_id).first()
        
        if result:
            # 更新现有结果
            result.content = generated_text
        else:
            # 创建新结果
            result = models.Result(
                document_id=document_id,
                content=generated_text
            )
            db.add(result)
        
        # 更新文档状态
        document.status = models.DocumentStatus.COMPLETED
        
        # 提交更改
        db.commit()
        
        print(f"为文件 {document_id} 生成的文书已完成，长度: {len(generated_text)}")
        
        # 模拟保存到文件（可选，用于备份）
        result_dir = "ai_results"
        os.makedirs(result_dir, exist_ok=True)
        with open(os.path.join(result_dir, f"{document_id}_result.txt"), "w", encoding="utf-8") as f:
            f.write(generated_text)
            
        return generated_text
        
    except Exception as e:
        # 更新文档状态为失败
        try:
            document = db.query(models.Document).filter(models.Document.id == document_id).first()
            if document:
                document.status = models.DocumentStatus.FAILED
                db.commit()
        except:
            pass
            
        print(f"AI处理错误: {str(e)}")
        raise Exception(f"AI处理错误: {str(e)}")

async def process_document(text, task_type):
    """
    根据任务类型处理文档
    """
    if task_type == TaskType.TASK1:
        # 提取第一句话
        return extract_first_sentence(text)
    elif task_type == TaskType.TASK2:
        # 构建有说服力的论点
        return build_persuasive_arguments(text)
    elif task_type == TaskType.TASK3:
        # 完善法律策略
        return refine_legal_strategy(text)
    elif task_type == TaskType.TASK4:
        # 关于法律的问题
        return answer_about_law(text)
    elif task_type == TaskType.TASK5:
        # 查找案例
        return find_case(text)
    else:
        return "未知的任务类型"

def extract_first_sentence(text):
    """
    提取文本中的第一句话
    """
    # 使用正则表达式匹配第一个句子（以句号、问号或感叹号结尾）
    match = re.search(r'([^.!?]+[.!?])', text)
    if match:
        first_sentence = match.group(1).strip()
        return f'PDF文件的第一句话是：\n\n"{first_sentence}"'  # 使用英文引号
    else:
        # 如果没有找到句号等标点，则返回前100个字符
        first_part = text[:100].strip() + "..." if len(text) > 100 else text.strip()
        return f'PDF文件的开头内容是：\n\n"{first_part}"'  # 使用英文引号

def build_persuasive_arguments(text):
    """构建有说服力的论点"""
    # 暂时只返回第一句话
    return extract_first_sentence(text)

def refine_legal_strategy(text):
    """完善法律策略"""
    # 暂时只返回第一句话
    return extract_first_sentence(text)

def answer_about_law(text):
    """回答关于法律的问题"""
    # 暂时只返回第一句话
    return extract_first_sentence(text)

def find_case(text):
    """查找相关案例"""
    # 暂时只返回第一句话
    return extract_first_sentence(text)

async def get_result(file_id: int, db: Session):
    """
    获取文档处理结果
    
    Args:
        file_id: 文档ID
        db: 数据库会话
        
    Returns:
        dict: 包含结果内容和状态的字典
    """
    try:
        # 获取文档
        document = db.query(Document).filter(Document.id == file_id).first()
        if not document:
            return {"status": "error", "message": f"Document with ID {file_id} not found"}
        
        # 获取结果 - 使用原始 SQL 查询避免 case_id 列
        result_query = text("SELECT id, document_id, content, created_at, updated_at FROM results WHERE document_id = :doc_id")
        result_row = db.execute(result_query, {"doc_id": file_id}).first()
        
        if document.status == DocumentStatus.PROCESSING:
            return {"status": "processing", "message": "Document is still being processed"}
        
        elif document.status == DocumentStatus.FAILED:
            return {"status": "failed", "message": "Document processing failed"}
        
        elif document.status == DocumentStatus.COMPLETED and result_row:
            # 从查询结果构建 Result 对象
            result_content = result_row[2]  # content 是第三列
            
            return {
                "status": "completed",
                "content": result_content,
                "document": {
                    "id": document.id,
                    "filename": document.filename,
                    "task_type": document.task_type
                }
            }
        
        else:
            # 文档已上传但尚未处理
            if document.status == DocumentStatus.UPLOADED:
                return {"status": "uploaded", "message": "Document is uploaded but not yet processed. Please call the /ai/process endpoint first."}
            
            # 其他情况
            return {"status": "unknown", "message": "Result not found or document status is inconsistent"}
    
    except Exception as e:
        # 记录错误并返回友好的错误消息
        print(f"Error getting result for document {file_id}: {str(e)}")
        return {"status": "error", "message": f"An error occurred while retrieving the result: {str(e)}"} 