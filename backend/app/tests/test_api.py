import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

def test_upload_document():
    """测试文档上传API"""
    url = f"{BASE_URL}/documents/upload"
    
    # 准备测试文件
    files = {
        'files': ('test.txt', 'This is a test document content', 'text/plain')
    }
    
    data = {
        'task_type': 'TASK1'
    }
    
    # 获取认证令牌 (简化版，实际应用中应该使用正确的认证流程)
    # 这里假设有一个 /token 端点用于获取令牌
    token_response = requests.post(f"{BASE_URL}/token", data={
        "username": "testuser",
        "password": "password"
    })
    
    if token_response.status_code == 200:
        token = token_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 发送请求
        response = requests.post(url, files=files, data=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"上传成功: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        else:
            logger.error(f"上传失败: {response.status_code} - {response.text}")
    else:
        logger.error(f"获取令牌失败: {token_response.status_code} - {token_response.text}")

if __name__ == "__main__":
    test_upload_document() 