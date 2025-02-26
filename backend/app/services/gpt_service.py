import openai
from app.config import settings
from typing import List

# 设置 API 密钥
openai.api_key = settings.OPENAI_API_KEY

async def generate_legal_document(text: str, task_type: str) -> str:
    """
    使用 GPT 模型生成法律文书
    
    Args:
        text: 从 PDF 提取的文本内容
        task_type: 任务类型，如 "TASK1"
        
    Returns:
        str: 生成的法律文书内容
    """
    # 根据任务类型构建提示
    prompt = get_prompt_for_task(text, task_type)
    
    # 调用 OpenAI API (旧版本方式)
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # 或其他适合的模型
        messages=[
            {"role": "system", "content": "You are a legal expert assistant that helps draft legal documents based on provided information."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    # 返回生成的内容
    return response.choices[0].message.content

def get_prompt_for_task(text: str, task_type: str) -> str:
    """
    根据任务类型获取适当的提示模板
    
    Args:
        text: 从 PDF 提取的文本内容
        task_type: 任务类型
        
    Returns:
        str: 构建的提示
    """
    if task_type == "TASK1":
        return f"""
        Based on the following information, perform TASK1:
        
        {text}
        
        Please format the document properly with all necessary sections.
        """
    
    elif task_type == "TASK2":
        return f"""
        Based on the following information, perform TASK2:
        
        {text}
        
        Please format the document properly with all necessary sections.
        """
    
    elif task_type == "TASK3":
        return f"""
        Based on the following information, perform TASK3:
        
        {text}
        
        Please include all necessary details.
        """
    
    elif task_type == "TASK4":
        return f"""
        Based on the following information, perform TASK4:
        
        {text}
        
        Please include all necessary details.
        """
    
    elif task_type == "TASK5":
        return f"""
        Based on the following information, perform TASK5:
        
        {text}
        
        Please include all necessary details.
        """
    
    else:
        # 默认提示
        return f"""
        Based on the following information, please analyze and generate an appropriate response:
        
        {text}
        
        Please ensure the document is properly formatted and includes all necessary elements.
        """