"""封装的回复消息函数"""

async def send_message(client, message_type, user_id=None, group_id=None, msg=None):
    if message_type == 'private':
        await client.send(
            {
                "action": "send_private_msg",
                "params": {"user_id": user_id, "message": msg},
            }
        )
    elif message_type == 'group':
        await client.send(
            {
                "action": "send_group_msg",
                "params": {"group_id": group_id, "message": msg},
            }
        )