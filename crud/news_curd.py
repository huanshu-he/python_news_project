

from fastapi.params import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from conf.db_conf import get_db
from models.news import Category, News



# 定义新闻分类数据查询函数
async def get_categories(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    # """
    # 查询分类数据
    # :param skip:
    # :param limit:
    # :param db:
    # :return:
    # """
    # 查询数据语句, offset(skip) 跳过skip条数据, limit(limit) 返回limit条数据
    stmt = select(Category).offset(skip).limit(limit)
    # 执行查询语句
    result = await db.execute(stmt)
    cats = result.scalars().all()
    # # 将查询结果转换为前端需要的属性值的字典
    # # 初始化分类字典
    # cats = []
    # for cat in result.scalars().all():
    #     # 使用jsonable_encoder()转换成字典
    #     cat_dict = jsonable_encoder(cat)
    #     # 使用pop()方法将字典中的键值对移动到新的字典中, 删除原字典中的键值对
    #     cat_dict["sortOrder"] = cat_dict.pop("sort_order", None)
    #     cat_dict["updatedAt"] = cat_dict.pop("updated_at", None)
    #     cat_dict["createdAt"] = cat_dict.pop("created_at", None)
    #     cats.append(cat_dict)

    # return result.scalars().all()  # 返回查询的所有分类列表
    return cats  # 返回查询的所有分类列表


# 定义新闻列表数据查询函数

async def get_news_list(category_id: int = None, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(News))
    # 获取所有数据
    news_list = result.scalars().all()
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


