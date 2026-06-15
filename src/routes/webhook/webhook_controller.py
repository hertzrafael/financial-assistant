from fastapi import APIRouter, status, Request

from routes.webhook import webhook_service


router = APIRouter(
    prefix='/webhook'
)


@router.post('/messages-upsert', status_code=status.HTTP_201_CREATED)
async def message_upsert(request: Request):
    return await webhook_service.message_upsert(request)

@router.post('/connection-update', status_code=status.HTTP_201_CREATED)
async def connection_update(request: Request):
    return await webhook_service.connection_update(request)
