from src.communication.whatsapp_provider import WhatsappCommunicationProvider
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database.connection import DatabaseConnection
from database import models_register
from core.route_register import RouteRegister
from ai.agent import FinancialAgent
from ai.graph import build_graph
from ai.checkpointer.checkpointer_builder import build_checkpointer_psql, test_connection

from os import getenv
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    await test_connection(getenv("CHECKPOINTER_DSN"))
    
    async with build_checkpointer_psql(getenv("CHECKPOINTER_DSN")) as checkpointer:
        graph = await build_graph(checkpointer)
        app.state.agent = FinancialAgent(graph=graph)

        print("INICIANDO CONEXÃO COM A INSTÂNCIA WHATSAPP...")
        app.state.whatsapp_communication = WhatsappCommunicationProvider(
            apiKey=getenv("EVOLUTION_API_KEY"),
            instance_id=getenv("EVOLUTION_INSTANCE_ID"),
            webhook_endpoint=getenv("EVOLUTION_WEBHOOK_URL"),
            evolution_base_url=getenv("EVOLUTION_BASE_URL")
        )
        await app.state.whatsapp_communication.create()
        print("FINALIZADA CONEXÃO COM A INSTÂNCIA WHATSAPP")

        connection = DatabaseConnection()
        engine = connection.connect(getenv("DATABASE_DSN"))

        await models_register.Models(engine).create_models()
        
        app.state.session_maker = connection.get_session_maker(engine)
        yield

        connection.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RouteRegister(app).register_routes()
