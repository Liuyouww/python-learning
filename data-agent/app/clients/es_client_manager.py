from app.conf.app_config import ESConfig, app_config
from elasticsearch import AsyncElasticsearch

class EsClientManager:
    def __init__(self,config:ESConfig):
        self.client: AsyncElasticsearch|None = None
        self.config:ESConfig = config
    def __get_url(self):
        return  f'http://{self.config.host}:{self.config.port}'
    def init(self):
        self.client = AsyncElasticsearch(hosts=[self.__get_url()])
    async def close(self):
        await self.client.close()

es_client_manager = EsClientManager(app_config.es)