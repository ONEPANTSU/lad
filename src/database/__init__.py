from datetime import datetime
from typing import Any, AsyncGenerator

from sqlalchemy import JSON, MetaData, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import config
from src.database.connection import Connection
from src.database.initializer import DataBaseInitializer
from src.database.session_factory import SessionFactory

__all__ = [
    "Base",
    "get_async_session",
    "engine",
    "connection",
    "session_factory",
    "init_database",
]

connection = Connection(config)
engine = connection.engine
session_factory = SessionFactory(engine)


class Base(DeclarativeBase):
    metadata = MetaData()
    type_annotation_map = {dict[str, Any]: JSON}

    def __repr__(self):
        attrs = self.get_info()
        representation = f"\n{self.__class__.__name__}:\n"
        for key, val in attrs.items():
            representation += f"{key}: {val}\n"
        return representation

    def get_info(self) -> dict:
        return {
            key: str(val) if isinstance(val, datetime) else val
            for key, val in self.get_dict().items()
        }

    def get_dict(self) -> dict:
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self).mapper.column_attrs
        }


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


def init_database():
    db_initializer = DataBaseInitializer(
        connection=connection, engine=engine, base=Base
    )
    db_initializer.initialize()
