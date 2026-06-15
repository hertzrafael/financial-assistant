from database.base import Base

from database.models.spent_model import SpentModel


class Models:

    def __init__(self, engine):
        self.engine = engine
    
    async def create_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
