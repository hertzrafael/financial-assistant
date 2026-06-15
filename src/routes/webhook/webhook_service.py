from fastapi import Request, HTTPException, status


async def message_upsert(request: Request):
    print("PASSOU UPSERT")
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
    

async def connection_update(request: Request):
    print('connection method')
    # async with session_maker() as session:
    #     async with session.begin():
    #         body = await request.json()
    #         status = body['data']['state']
            
    #         instance = await repository.get_instance_from_query(session, InstanceModel.evolution_name == instance_id)
    #         if not instance:
    #             raise HTTPException(
    #                 status.HTTP_404_NOT_FOUND,
    #                 f"Instância com id {instance_id} não encontrada."
    #             )
            
    #         await repository.patch_instance(session, instance.id, connection_status=status)
