import openai
import time
import os
from app.config import settings
from app import models
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document, Result, DocumentStatus
from app.services.pdf_service import extract_text_from_pdf
from app.services.gpt_service import generate_legal_document
from fastapi import Depends, HTTPException
from datetime import datetime
from sqlalchemy import text

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

async def process_document(file_id: int, task_type: str, db: Session):
    """
    处理文档并生成简单输出（PDF 的第一句话）
    
    Args:
        file_id: 文档ID
        task_type: 任务类型，如 "TASK1"
        db: 数据库会话
    """
    # 获取文档
    document = db.query(Document).filter(Document.id == file_id).first()
    if not document:
        raise HTTPException(status_code=404, detail=f"Document with ID {file_id} not found")
    
    try:
        # 更新文档状态为处理中
        document.status = DocumentStatus.PROCESSING
        db.commit()
        
        # 从PDF提取文本
        text = extract_text_from_pdf(document.file_path)
        
        # 简单处理：获取第一句话（以句号、问号或感叹号结尾）
        first_sentence = ""
        if text:
            # 尝试找到第一个句子结束的位置
            for end_char in ['.', '?', '!']:
                pos = text.find(end_char)
                if pos > 0:
                    first_sentence = text[:pos+1]
                    break
            
            # 如果没有找到句子结束符，就取前100个字符
            if not first_sentence:
                first_sentence = text[:min(100, len(text))] + "..."
        else:
            first_sentence = "无法从PDF中提取文本内容。"
        
        # 添加任务类型信息
        result_content = f"任务类型: {task_type}\n\nPDF第一句话: {first_sentence}\n\n(这是一个简化的输出，用于测试系统功能。)"
        
        # 使用原始 SQL 查询检查是否已有结果记录
        check_result_query = text("SELECT id FROM results WHERE document_id = :doc_id")
        existing_result = db.execute(check_result_query, {"doc_id": file_id}).first()
        
        if existing_result:
            # 更新现有结果
            update_query = text("UPDATE results SET content = :content, updated_at = :updated_at WHERE document_id = :doc_id")
            db.execute(update_query, {
                "content": result_content,
                "updated_at": datetime.utcnow(),
                "doc_id": file_id
            })
        else:
            # 创建新的结果记录
            insert_query = text("INSERT INTO results (document_id, content, created_at, updated_at) VALUES (:doc_id, :content, :created_at, :updated_at)")
            db.execute(insert_query, {
                "doc_id": file_id,
                "content": result_content,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
        
        # 更新文档状态为已完成
        document.status = DocumentStatus.COMPLETED
        db.commit()
        
        return {"status": "success", "message": "Document processed successfully"}
        
    except Exception as e:
        # 更新文档状态为失败
        document.status = DocumentStatus.FAILED
        db.commit()
        print(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

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