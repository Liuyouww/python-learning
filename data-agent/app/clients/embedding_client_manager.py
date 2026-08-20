from app.conf.app_config import EmbeddingConfig, app_config
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings


class EmbeddingClientManager:
    def __init__(self,config:EmbeddingConfig):
        self.client: HuggingFaceEndpointEmbeddings | None = None
        self.config:EmbeddingConfig = config
    def __get_url(self):
        return f'http://{self.config.host}:{self.config.port}'
    def init(self):
        self.client=HuggingFaceEndpointEmbeddings(model=self.__get_url())

embedding_client_manager = EmbeddingClientManager(app_config.embedding)