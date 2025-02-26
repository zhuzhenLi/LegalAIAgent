import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.append(str(Path(__file__).parent))

from app.database import engine, Base, create_tables

def test_connection():
    try:
        # 尝试连接数据库
        connection = engine.connect()
        print("数据库连接成功!")
        connection.close()
        
        # 尝试创建表
        create_tables()
        print("表创建成功!")
        
        return True
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 