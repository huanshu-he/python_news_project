import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from conf.db_conf import async_engine
# from models.news import Base as NewsBase


async def create_tables(base_classes=None):
    """
    通用创表方法，支持单个或多个Base类
    """
    if base_classes is None:
        return
    # 确保参数是可迭代的
    if not isinstance(base_classes, (list, tuple)):
        base_classes = [base_classes]

    async with async_engine.begin() as conn:
        for base in base_classes:
            await conn.run_sync(base.metadata.create_all)


# 存储需要清理的资源
app_resources = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    生命周期管理:
    fastapi应用创建时: 创建表, 存储需要清理的资源
    fastapi应用关闭时: 清理资源, 并取消异步任务
    :param app:
    :return:
    """
    # 创建表, 不传参默认不执行创建表
    await create_tables()

    # 初始化并存储需要清理的资源
    app_resources['db_engine'] = async_engine
    # app_resources['redis_client'] = redis_client

    yield

    # 清理所有资源
    if 'db_engine' in app_resources:
        await app_resources['db_engine'].dispose()
    # if 'redis_client' in app_resources:
    #     app_resources['redis_client'].close()

    app_resources.clear()

    # 确保所有异步任务完成, 正常关闭进程, 避免端口占用
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()  # 标记任务为取消状态
    await asyncio.gather(*tasks, return_exceptions=True)  # 等待所有任务被取消，处理取消异常