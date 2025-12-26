"""
news新闻模块ORM模型类
"""
from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# 创建ORM当前模块的基类
class Base(DeclarativeBase):
    pass


# 定义新闻类型ORM模型类
class Category(Base):
    """
    Categorise对应数据库中的news_category表
    """
    # 指定表名
    __tablename__ = "news_category"

    # 定义字段
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, name='sort_order', default=0, nullable=False, comment="排序")
    # datetime: python类型, DateTime: ORM类型, 默认值: datetime.now: 当前时间, 注意不要加(),也就是创建数据时才调用datetime.now
    created_at: Mapped[datetime] = mapped_column(DateTime, name='created_at', default=datetime.now, nullable=False,
                                                comment="创建时间")
    # onupdate: 每次更新数据时, 调用当前时间作为更新时间
    updated_at: Mapped[datetime] = mapped_column(DateTime, name='updated_at', default=datetime.now,
                                                onupdate=datetime.now, nullable=False,
                                                comment="更新时间")

    def __repr__(self):
        return f"Categorise(id={self.id}, name={self.name})"


from sqlalchemy import String, Integer, DateTime, Index, Text, ForeignKey
from typing import Optional


## ..................
##  其他代码
## ..................


class News(Base):
    """
    新闻模型
    对应数据库中的 news 表
    """
    __tablename__ = 'news'

    # 创建索引
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),
        Index('idx_publish_time', 'publish_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), name='category_id',  nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, name='publish_time', default=datetime.now,
                                                   comment="发布时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, name='created_at', default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, name='updated_at', default=datetime.now,
                                                onupdate=datetime.now,
                                                comment="更新时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
