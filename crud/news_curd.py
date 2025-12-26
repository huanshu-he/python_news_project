from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from sqlalchemy import select, func, Update
from sqlalchemy.ext.asyncio import AsyncSession

from conf.db_conf import get_db
from models.news import Category, News



# 定义新闻分类数据查询函数
async def get_categories(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    """
    查询分类数据
    :param skip:
    :param limit:
    :param db:
    :return:
    """
    # 查询数据语句, offset(skip) 跳过skip条数据, limit(limit) 返回limit条数据
    stmt = select(Category).offset(skip).limit(limit)
    # 执行查询语句
    result = await db.execute(stmt)
    # cats = result.scalars().all()
    # 将查询结果转换为前端需要的属性值的字典
    # 初始化分类字典
    cats = []
    for cat in result.scalars().all():
        # 使用jsonable_encoder()转换成字典
        cat_dict = jsonable_encoder(cat)
        # 使用pop()方法将字典中的键值对移动到新的字典中, 删除原字典中的键值对
        cat_dict["sortOrder"] = cat_dict.pop("sort_order", None)
        cat_dict["updatedAt"] = cat_dict.pop("updated_at", None)
        cat_dict["createdAt"] = cat_dict.pop("created_at", None)
        cats.append(cat_dict)

    # return result.scalars().all()  # 返回查询的所有分类列表
    return cats  # 返回查询的所有分类列表


# 查询新闻列表数据, 位置参数: db 必须写在 关键字参数前面
async def get_news_list(db: AsyncSession, category_id: int | None = None, skip: int = 1, limit: int = 10):
    """
    查询新闻列表
    :param db:
    :param category_id:
    :param skip:
    :param limit:
    :return:
    """
    # 创建查询语句, 查询所有新闻
    stmt = select(News)
    # 判断category_id是否传值, 如果有值, 返回当前分类的新闻
    if category_id:
        stmt = stmt.where(News.category_id == category_id)

    # 执行查询, offset: 跳过skip条数据, limit: 返回limit条数据
    result = await db.execute(stmt.offset(skip).limit(limit))
    # news_list = result.scalars().all()

    # 将查询结果转换为前端需要的属性值的字典
    # 初始化新闻列表
    news_list = []
    for news in result.scalars().all():
        # 使用jsonable_encoder()转换成字典
        news_dict = jsonable_encoder(news)
        # 使用pop()方法将字典中的键值对移动到新的字典中, 删除原字典中的键值对
        news_dict["categoryId"] = news_dict.pop("category_id", None)
        news_dict["publishTime"] = news_dict.pop("publish_time", None)
        news_dict.pop("content", None)
        # del news_dict["content"]  # 删除content属性
        news_list.append(news_dict)

    # return result.scalars().all()
    return news_list

# 查询新闻数量，为了计算是否还有更多新闻
async def get_news_count(db: AsyncSession, category_id: int = None):
    """
    查询新闻总数
    :param db: 数据库会话
    :param category_id: 分类ID，可选
    :return: 新闻总数
    """
    # 创建查询语句，统计News表中的记录数量
    stmt = select(func.count(News.id))
    # 如果提供了分类ID，则在查询条件中添加分类过滤
    if category_id:
        stmt = stmt.where(News.category_id == category_id)
    # 执行数据库查询
    result = await db.execute(stmt)
    # 获取查询结果的标量值（即计数结果）
    return result.scalar()


# 获取新闻详情数据
async def get_news_detail(db: AsyncSession, news_id: int):
    """
    获取新闻详情数据
    :param news_id:
    :param db:
    :return:
    """
    # 创建查询语句, 获取新闻详情数据
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)

    return result.scalar_one_or_none()


# 更新新闻浏览量
async def update_news_views(db: AsyncSession, news_id: int):
    """
    更新新闻浏览量: 浏览量+1
    :param news_id:
    :param db:
    :return:
    """
    # 创建更新语句, 更新逻辑: views=News.views + 1
    stmt = Update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()  # 需要事务操作的场景, select查询不需要commit

    return result.rowcount > 0


# 查询相关新闻
async def get_related_news(news_id: int, news: News, db: AsyncSession, limit: int = 5):
    """
    查询相关新闻: 同类新闻而且不包括自己, 排序 热度, 发布时间 倒序, limit获取前几条
    :param news_id:
    :param db:
    :return:
    """
    # 创建查询语句, 获取相关新闻
    stmt = select(News).where(
        News.category_id == news.category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)

    result = await db.execute(stmt)

    # 将查询结果转换为前端需要的属性值的字典: 使用列表推导式, 字典推导式
    # example_list = [("key", "value"), ("key1", "value1")]
    # example_dict = {key: value for key, value in example_list}

    # 如果不需要改变字段的名称, 只需将字段值移动到新的字典中
    # related_news = [
    #        jsonable_encoder(news) for news in result.scalars().all()
    # ]

    related_news = [
        {
            "id": news.id,
            "title": news.title,
            "content": news.content,
            "image": news.image,
            "author": news.author,
            "publishTime": news.publish_time,
            "categoryId": news.category_id,
            "views": news.views
        }
        for news in result.scalars().all()
    ]

    # return result.scalars().all()
    return related_news