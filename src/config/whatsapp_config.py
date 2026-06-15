class WhatsappConfig:

    def __init__(self, evolution_base_url: str = None):
        self.base_url = evolution_base_url or "http://localhost:8080"
        self.create_endpoint = f"{self.base_url}/instance/create"
        self.connect_endpoint = f"{self.base_url}/instance/connect"
        self.disconnect_endpoint = f"{self.base_url}/instance/logout"
        self.check_connection_endpoint = f"{self.base_url}/instance/connectionState"
        self.send_message_endpoint = f"{self.base_url}/message/sendText"

    def fabricate_endpoint(self, endpoint, id):
        return f"{endpoint}/{id}"