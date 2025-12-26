# """
# 依赖注入的函数
# """
# from fastapi import Header, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from conf.db_conf import get_db
# from crud.users_curd import get_user_by_token
#
#
# 用户登录状态检测函数
from fastapi import HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from conf.db_conf import get_db
from crud.users_curd import get_user_by_token


async def get_current_user(authorization: str = Header(...), db: AsyncSession = Depends(get_db)):
    """
    获取token , 使用token获取用户
    :param authorization:
    :param db:
    :return:
    """
    print(authorization)
    info = authorization.split(" ")
    if len(info) == 1:
        token = authorization
    else:
        token = info[1]
    user = await get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=400, detail="用户没有登录")

    return user
