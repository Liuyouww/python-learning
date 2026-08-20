from app.conf.app_config import QdrantConfig, app_config
from qdrant_client import AsyncQdrantClient

class QrantClientManager:
    def __init__(self,config:QdrantConfig):
        self.client: AsyncQdrantClient|None = None
        self.config: QdrantConfig = config
    def __get_url(self):
        return f'http://{self.config.host}:{self.config.port}'

    def init(self):
        self.client = AsyncQdrantClient(url=self.__get_url())
    async def close(self):
        await self.client.close()

qdrant_client_manager=QrantClientManager(app_config.qdrant)
