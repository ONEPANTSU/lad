from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


class SessionFactory:
    def __init__(self, engine: AsyncEngine):
        self.session_maker = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

    def __call__(self):
        return self.session_maker()
