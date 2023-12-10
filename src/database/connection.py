from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import Config


class Connection:
    def __init__(self, config: Config):
        self.config = config
        self.engine = self.__create_engine()

    def get_url(self) -> str:
        return self.get_default_url() + f"/{self.config.name}"

    def get_default_url(self) -> str:
        return f"{self.config.driver}://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}"

    def __create_engine(self):
        return create_async_engine(url=self.get_url(), poolclass=NullPool)
