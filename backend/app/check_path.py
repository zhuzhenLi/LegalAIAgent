import sys
import os

def main():
    print("Python 路径:")
    for path in sys.path:
        print(f"  - {path}")
    
    print("\n当前工作目录:")
    print(f"  - {os.getcwd()}")
    
    print("\n尝试导入 app.models:")
    try:
        import app.models
        print(f"  - 导入成功")
        print(f"  - 模块路径: {app.models.__file__}")
        print(f"  - 模块内容: {dir(app.models)}")
        
        if hasattr(app.models, 'Base'):
            print(f"  - Base 存在")
        else:
            print(f"  - Base 不存在")
    except Exception as e:
        print(f"  - 导入失败: {str(e)}")

if __name__ == "__main__":
    main() 