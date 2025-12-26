"""
新闻模块统一路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conf.db_conf import get_db
from crud.news_curd import get_categories
from models.news import Category
from utils.response_handlers import success_response

# 实例化APIRouter路由
router = APIRouter(
    prefix="/api/news",
    tags=["news"],
)

# todo: 创建新闻分类路由
# 查询参数的注解类型: Query,  路径参数的注解类型: Path
"""
注解类型常用参数:
        default: 默认值
        gt: float | None = None,  大于
        ge: float | None = None,  大于等于
        lt: float | None = None,  小于
        le: float | None = None,  小于等于
        min_length: int | None = None,  最小长度
        max_length: int | None = None,  最大长度
"""


@router.get("/categories")
async def read_categories(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100),
                          db: AsyncSession = Depends(get_db)):
    """
    查询分类数据
    :param skip: 跳过记录数
    :param limit: 返回记录数
    :param db: 数据库会话
    :return: 新闻分类列表
    """
    data = await get_categories(skip, limit, db)
    return success_response(data)

#
# @router.get("/list")
# async def read_news(category_id: int = Query(..., alias="categoryId"), page: int = Query(default=1),
#                     page_size: int = Query(default=10, alias="pageSize", le=100), db: AsyncSession = Depends(get_db)):
#     """
#          获取新闻列表接口（支持分页和分类筛选）
#
#         Args:
#             category_id (int): 分类ID，必填参数，通过查询参数categoryId传入
#             page (int, optional): 页码，从1开始，默认为第1页
#             page_size (int, optional): 每页显示的新闻数量，最大值为100，默认为10
#             db (AsyncSession): 通过依赖注入获取的数据库会话对象
#
#         Example:
#             GET /api/news/list?categoryId=1
#             GET /api/news/list?categoryId=1&page=2&pageSize=20
#         """
#     data = "await get_list(db)"
#
#     return success_response(data)


## ...............
## 其他代码
## ...............

@router.get("/detail")
async def read_news_detail(news_id: int=Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    """
        获取新闻详情接口

        Args:
            news_id (int): 新闻ID，必填参数，通过查询参数id传入
            db (AsyncSession): 通过依赖注入获取的数据库会话对象
        Example:
            GET /api/news/detail?id=1
    """


    return {
        "code": 200,
        "message": "success",
        "data": "新闻详情"
    }