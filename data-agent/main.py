import uuid
from contextlib import asynccontextmanager
import time
from app.api.lifespan import lifespan
from app.api.routers.query_router import query_router
from app.core.context import request_id_context_var
from fastapi import FastAPI, Request

# FastAPI:
# 生命周期lifespan--设定程序前后的初始化和关闭--设定上下文管理器函数--app=FastAPI(lifespan=函数名)
# 上下文管理器@[async]contextmanager定义函数(包括前操作+yield+后操作)，之后使用with
# 中间件@app.middleware("http")-类似拦截器--在路径操作前后进行操作--路径->中间件->操作->中间件->输出--request,call_next(request)
#   --可用于检查每个接口的一些信息
# 依赖注入：有一种方法声明需要的依赖（可以嵌套、重复子依赖、可以带yield的依赖函数）--声明依赖函数--在参数部分进行调用 name:Annotated[依赖类型, Depends(依赖函数名)]


app = FastAPI(lifespan=lifespan)

app.include_router(query_router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 请求被处理前
    request_id = uuid.uuid4()
    request_id_context_var.set(request_id)
    response = await call_next(request)
    # 请求被处理后
    return response
