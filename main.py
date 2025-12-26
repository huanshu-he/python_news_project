from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.news_router import router as news_router
from routers.users_router import router as users_router
from utils.lifespan_manager import lifespan
from utils.response_handlers import register_exception_handlers

app = FastAPI(lifespan=lifespan)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 允许所有源访问
    allow_credentials=True,    # 允许凭证
    allow_methods=["*"],    # 允许所有方法
    allow_headers=["*"],    # 允许所有头
)

# 注册全局异常处理器
register_exception_handlers(app)

# 注册路由
app.include_router(news_router)
app.include_router(users_router)

@app.get("/")
async def root():
    print()
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
