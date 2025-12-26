from fastapi import APIRouter, Depends, Header
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from conf.db_conf import get_db
from crud.users_curd import get_user_by_username, create_user, create_user_token, authenticate_user, get_user_by_token, \
    change_user_info, change_user_password
from schemas.users import UserRegisterLoginRequest, UserUpdateRequest, UserUpdatePasswordRequest
from utils.response_handlers import success_response

router = APIRouter(
    prefix="/api/user",
    tags=["user"],
)


# 用户模块注册
@router.post("/register")
async def register(user_data: UserRegisterLoginRequest, db: AsyncSession = Depends(get_db)):
    """
    用户注册
    :param username: 用户名
    :param password: 密码
    :return: 注册结果
    """
    # 查看用户名是否已存在
    user = await get_user_by_username(db, user_data.username)
    if user:
        return HTTPException(status_code=400, detail="用户名已存在")

    # 创建用户
    user = await create_user(db, user_data)
    # 创建访问令牌token
    token = await create_user_token(db, user.id)
    response_data = {
        "token": token,
        "userInfo": user
    }
    return success_response(message="注册成功", data=response_data)


# 用户模块的登录
@router.post("/login")
async def login(login_data: UserRegisterLoginRequest, db: AsyncSession = Depends(get_db)):
    """
    登录账户
    :param login_data:
    :param db:
    :return:
    """
    # 验证登录信息: 用户名, 密码
    user = await authenticate_user(login_data.username, login_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 登录验证成功, 创建token(token生成, token有效期设置)
    token = await create_user_token(db, user.id)
    response_data = {
        "token": token,
        "userInfo": user
    }

    return success_response(message="登录成功", data=response_data)


# 用户模块的获取用户信息
@router.get("/info")
async def get_user_info(authorization: str = Header(None), db: AsyncSession = Depends(get_db)):
    """
    获取用户信息
    :param db:
    :param authorization:
    :return:
    """
    # 通过authorization传递的token获取用户信息
    print(f"我是是是是是是是的authorization：{authorization}")
    token = authorization.split(" ")[1]
    print(f"我是是是是是是是的token：{token}")

    user = await get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=400, detail="用户没有登录")
    user = jsonable_encoder(user)
    return success_response(message="获取用户信息成功", data=user)


# 用户模块更新用户信息
@router.put("/update")
async def update_user_info(user_update_data: UserUpdateRequest, authorization: str = Header(None),
                           db: AsyncSession = Depends(get_db)):
    """
    更新用户信息
    :param user_update_data:
    :param authorization:
    :return:
    """
    user = await get_user_by_token(authorization, db)
    if not user:
        raise HTTPException(status_code=400, detail="用户没有登录")
    user = await change_user_info(user_update_data, db, user)
    return success_response(message="更新用户信息成功", data=user)


# 用户模块修改用户密码



@router.put("/password")
async def update_user_password(password_data: UserUpdatePasswordRequest,
                               authorization: str = Header(None),
                               db: AsyncSession = Depends(get_db)):
    """
    修改用户密码
    :param user_update_password_data:
    :param authorization:
    :return:
    """
    old_password = password_data.old_password
    new_password = password_data.new_password
    user = await get_user_by_token(authorization, db)
    if not user:
        raise HTTPException(status_code=400, detail="用户没有登录")
    if not await authenticate_user(user.username, old_password, db):
        raise HTTPException(status_code=400, detail="旧密码错误")
    user = await change_user_password(new_password, db, user)
    return success_response(message="修改用户密码成功", data=user)

