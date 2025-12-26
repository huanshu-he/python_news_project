import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import UserToken, User
from schemas.users import UserRegisterLoginRequest, UserUpdateRequest

# 密码加密上下文
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


# deprecated 自动处理已经加密的密码

def get_password_hash(password: str) -> str:
    """
    对密码进行哈希处理

    Args:
        password: 明文密码

    Returns:
        str: 哈希后的密码
    """
    return pwd_context.hash(password)


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    """
    根据用户名获取用户

    Args:
        db: 数据库会话
        username: 用户名

    Returns:
        User: 用户对象，如果不存在返回None
    """
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserRegisterLoginRequest) -> User:
    """
    创建新用户

    Args:
        db: 数据库会话
        user_data: 用户注册数据

    Returns:
        User: 创建的用户对象
    """
    # 对密码进行哈希处理
    hashed_password = get_password_hash(user_data.password)

    # 创建用户对象
    db_user = User(
        username=user_data.username,
        password=hashed_password

    )

    # 添加到数据库
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def create_user_token(db: AsyncSession, user_id: int) -> str:
    """
    为用户创建访问令牌

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        str: 访问令牌
    """
    # 生成随机token
    token = str(uuid.uuid4())

    # 设置过期时间（7天）
    expires_at = datetime.now() + timedelta(days=7)

    # 查询用户是否已有令牌记录
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    existing_token = result.scalar_one_or_none()

    if existing_token:
        # 如果用户已有令牌，则更新令牌信息
        existing_token.token = token
        existing_token.expires_at = expires_at
        await db.commit()
    else:
        # 如果用户没有令牌，则创建新的令牌记录
        db_token = UserToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.add(db_token)
        await db.commit()

    return token


# 验证用户密码
def verify_password(plain_password, hashed_password):
    """
    调用pwd_context对明文和密文密码进行校验
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


# 验证登录信息: 用户名和密码
async def authenticate_user(username: str, password: str, db: AsyncSession):
    """
    验证用户名和密码
    :param username:
    :param password:
    :param db:
    :return:
    """
    # 验证用户名
    user = await get_user_by_username(db, username)
    if not user:
        return False

    # 验证密码
    if not verify_password(password, user.password):
        return False

    return user


# 验证登录信息: 用户名和密码
async def authenticate_user(username: str, password: str, db: AsyncSession):
    """
    验证用户名和密码
    :param username:
    :param password:
    :param db:
    :return:
    """
    # 验证用户名
    user = await get_user_by_username(db, username)
    if not user:
        return False

    # 验证密码
    if not verify_password(password, user.password):
        return False

    return user


# 通过token查询用户信息
async def get_user_by_token(token: str, db: AsyncSession):
    """
    使用authorization传递的token值来查询用户信息
    :param token:
    :param db:
    :return:
    """
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    user_token = result.scalar_one_or_none()
    # token如果不存在或者过期了, 返回None
    if not user_token or user_token.expires_at < datetime.now():
        return None

    # 通过用户token表的user_id查询用户信息
    stmt = select(User).where(User.id == user_token.user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 更新用户信息
async def change_user_info(user_data: UserUpdateRequest, db: AsyncSession, user: User):
    """
    更新用户信息
    :param user_data:
    :param db:
    :param user:
    :return:
    """
    # # 使用Update更新用户信息: 使用model_dump(pydantic方法)将数据转换为字典, 忽略未设置属性, 忽略None属性
    # stmt = Update(User).where(User.id == user.id).values(**user_data.model_dump(exclude_unset= True, exclude_none=True))
    # await db.execute(stmt)


    # 使用属性赋值的方法更新用户信息
    for key, value in user_data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(user, key, value)  # setattr设置属性值, getattr获取属性值

    await db.commit()
    await db.refresh(user)  # 刷新数据, 重新从数据库获取最新数据

    return user