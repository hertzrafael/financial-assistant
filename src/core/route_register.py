from fastapi import APIRouter
from fastapi import FastAPI

from routes.webhook.webhook_controller import router as webhook_router


class RouteRegister:
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.api = APIRouter(
            prefix="/api/v1",
            tags=["API"],
        )

    def register_routes(self):
        self.api.get("/health", tags=["Health"])(self.__health_check__)
        self.api.include_router(webhook_router)

        self.app.include_router(self.api)

    def __health_check__(self):
        return {"status": "ok"}
    