from fastapi import Request, HTTPException, status


async def message_upsert(request: Request):
    body = await request.json()

    remote_jid = body['data']['key']['remoteJid']
    
    message = body['data']['message']['conversation']
    to = body['data']['key']['remoteJid']

    agent = request.app.state.agent
    if hasattr(request.state, "session_maker"):
        session_maker = request.state.session_maker
    else:
        session_maker = request.app.state.session_maker

    ai_response = await agent.send(message, remote_jid, session_maker)
    
    whatsapp_communication = request.app.state.whatsapp_communication
    await whatsapp_communication.send_message(to, ai_response)

    print(f'[LOG] A IA RESPONDEU PARA {to}: {ai_response}')
    
    return {"message": "OK"}

