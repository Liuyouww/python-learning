from idlelib.query import Query
from typing import Annotated

import anyio
from app.api.dependencies import get_query_service
from app.services.query_service import QueryService
from fastapi.responses import StreamingResponse
from app.api.schemas.query_schema import QuerySchema
from fastapi import APIRouter, Depends

query_router = APIRouter()

# 流式输出--StreamingResponse(fake_video_streamer(),media_type="text/event-stream")
#        --async def fake_video_streamer():
#             for i in range(10):
#                 yield f'step{i}'--遵循SSE协议(data:[空格] message之间\n\n区分，message内换行\n)--yield f'data: step{i}\n\n'

async def fake_video_streamer():
    for i in range(10):
        yield f'step{i}'
        await anyio.sleep(0.5)

@query_router.post('/api/query')
async def query_handler(query: QuerySchema,query_service:Annotated[QueryService, Depends(get_query_service)]):
    return StreamingResponse(query_service.query(query.query),media_type="text/event-stream") # 告知前端输入数据为流式文本
