from pydantic import Field, BaseModel, ConfigDict


# 创建用户注册登录请求参数模型
class UserRegisterLoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20) #必传
    password: str = Field(..., min_length=3, max_length=20)

    # # 定义模型配置
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "username": "example_user",
    #             "password": "example_password"
    #         }
    #     }
    # 定义模型配置
    model_config = ConfigDict(
        from_attributes=True,  # 从orm_mode属性中获取数据
        populate_by_name=True,  # 有配置别名时, pydantic模型可以接收属性名和别名
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "123456"
            }
        }
    )


class UserUpdateRequest(BaseModel):
    """
    用户信息更新请求数据模型
    """
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "nickname": "New Nickname",
    #             "avatar": "https://example.com/new_avatar.jpg",
    #             "gender": "female",
    #             "bio": "Updated bio"
    #         }
    #     }