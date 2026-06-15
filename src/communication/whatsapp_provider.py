from config.whatsapp_config import WhatsappConfig

import httpx
import asyncio


class WhatsappCommunicationProvider:

    def __init__(self, apiKey: str, instance_id: str, webhook_endpoint: str, evolution_base_url: str = None):
        self.config = WhatsappConfig(evolution_base_url=evolution_base_url)
        self.client = httpx.AsyncClient(
            headers={
                "apiKey": f"{apiKey}",
                "Content-Type": "application/json"
            }
        )
        self.webhook_endpoint = webhook_endpoint
        self.instance_id = instance_id

    async def create(self):
        payload = {
            "instanceName": self.instance_id,
            "qrcode": False,
            "integration": "WHATSAPP-BAILEYS",
            "webhook": {
                "url": self.webhook_endpoint.replace('{instance_id}', self.instance_id),
                "byEvents": True,
                "base64": True,
                "events": [
                    "APPLICATION_STARTUP",
                    "QRCODE_UPDATED",
                    "CONNECTION_UPDATE",
                    "MESSAGES_SET",
                    "MESSAGES_UPSERT",
                    "SEND_MESSAGE"
                ]
            }
        }
        response = await self.client.post(self.config.create_endpoint, json=payload)

        return response.json()
    
    async def connect(self):
        url = self.config.fabricate_endpoint(self.config.connect_endpoint, self.instance_id)
        response = await self.client.get(url)

        return response.json()

    async def disconnect(self):
        url = self.config.fabricate_endpoint(self.config.disconnect_endpoint, self.instance_id)
        response = await self.client.delete(url)

        return response.json()
    
    async def is_connected(self):
        url = self.config.fabricate_endpoint(self.config.check_connection_endpoint, self.instance_id)
        response = await self.client.get(url)

        return response.json()
    
    async def send_message(self, to, message):
        url = self.config.fabricate_endpoint(self.config.send_message_endpoint, self.instance_id)
        response = await self.client.post(url, json={
            "instance": self.instance_id,
            "number": to,
            "text": message
        })
        
        return response.json()


if __name__ == "__main__":
    
    async def run():
        provider = WhatsappCommunicationProvider(apiKey='', webhook_endpoint='')
        print('Tentando enviar mensagem...')
        response = await provider.send_message('1-LojinhaTeste', '', 'sei lá né, vai que!')
        print(response)
    
    asyncio.run(run())
    