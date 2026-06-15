from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DatabaseConnection:

    def connect(self, db_dsn: str):
        return create_async_engine(db_dsn)

    def get_session_maker(self, engine):
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    def disconnect(self):
        return self.get_session_maker().close_all()
