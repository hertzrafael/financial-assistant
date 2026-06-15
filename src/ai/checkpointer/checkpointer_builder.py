from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import asyncio


@asynccontextmanager
async def build_checkpointer_psql(db_dsn: str) -> AsyncGenerator[AsyncPostgresSaver]:
    async with AsyncPostgresSaver.from_conn_string(db_dsn) as checkpointer:
        await checkpointer.setup()
        yield checkpointer


async def test_connection(db_dsn: str):
    try:
        async with build_checkpointer_psql(db_dsn) as checkpointer:
            print("✅ Conectado com sucesso ao Postgres")
    except Exception as e:
        print("❌ Erro ao conectar:", e)
