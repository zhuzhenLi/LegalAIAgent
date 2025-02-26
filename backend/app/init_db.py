from app.database import engine
from app.models import Base

def init_db():
    """
    初始化数据库
    创建所有定义的数据库表
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("数据库表创建完成！") 