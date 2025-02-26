import os
import sys
from pathlib import Path

# 添加 backend 目录到 Python 路径
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

# 导入并运行初始化函数
from app.db.init_db import init_db

if __name__ == "__main__":
    init_db() 