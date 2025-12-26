"""
新闻模块统一路由
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conf.db_conf import get_db
from crud.news_curd import get_categories, get_news_count, get_news_list, get_news_detail, update_news_views, \
    get_related_news
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


@router.get("/list")
async def read_news(category_id: int = Query(..., alias="categoryId"), page: int = Query(default=1),
                    page_size: int = Query(default=10, alias="pageSize", le=100), db: AsyncSession = Depends(get_db)):
    """
    查询新闻列表
    :param category_id: 分类ID
    :param page: 页码
    :param page_size: 每页数量
    :param db: 数据库会话
    :return: 新闻列表
    """
    # 计算跳过的记录数
    skip = (page - 1) * page_size

    # 获取新闻列表
    news_list = await get_news_list(db, category_id, skip, page_size)

    # 获取新闻总数
    total = await get_news_count(db, category_id)

    # 判断是否有更多数据
    has_more = total > skip + page_size

    response_data = {
        "list": news_list,
        "total": total,
        "hasMore": has_more
    }

    return success_response(message="成功查询新闻列表", data=response_data)


## ...............
## 其他代码
## ...............

@router.get("/detail")
async def read_news_detail(news_id: int=Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    """
    查询新闻详情
    :param news_id: 新闻ID
    :param db: 数据库会话
    :return: 新闻详情
    """
    # 获取新闻详情
    news = await get_news_detail(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 更新新闻浏览量
    await update_news_views(db, news_id)

    # 获取相关新闻数据
    related_news = await get_related_news(news_id, news, db)


    response_data = {
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,  # 注意字段名映射
        "categoryId": news.category_id,  # 注意字段名映射
        "views": news.views,
        "relatedNews": related_news
    }


    return success_response(message="成功查询新闻详情", data=response_data)