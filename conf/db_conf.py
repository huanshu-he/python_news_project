# 定义一个模拟数据库函数
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


def get_database():
    db = "这是一个测试的数据库会话"
    return db

# 设置数据库URL
# 数据库引擎+数据库驱动://用户名:密码@ip:端口/数据库名?参数
async_database_url = "mysql+aiomysql://root:root@localhost:3307/news_app?charset=utf8mb4"

# 创建数据库 引擎
async_engine = create_async_engine(
    async_database_url,
    echo=True,  # 打印SQL语句
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 最大连接池溢出数量
)

# 创建数据库会话工厂
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False, # 提交之后是否缓存数据
    class_=AsyncSession,
)

# 创建数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话
            await session.commit()  # 会话完毕进行提交
        except Exception:
            await session.rollback()  # 如果会话出错, 回滚恢复处理之前的数据,保持数据库数据一致性
            raise  # 抛出异常
        finally:
            await session.close()  # 释放数据库连接