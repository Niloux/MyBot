from typing import Dict

from module.message import send_message


async def echo(client, data: Dict):
    """
    私人消息复读机
    """
    # response = {
    #     "self_id": 1400621898,
    #     "user_id": 183734182,
    #     "time": 1735887700,
    #     "message_id": 527314297,
    #     "message_seq": 527314297,
    #     "real_id": 527314297,
    #     "message_type": "private",
    #     "sender": {"user_id": 183734182, "nickname": "textValue", "card": ""},
    #     "raw_message": "111",
    #     "font": 14,
    #     "sub_type": "friend",
    #     "message": [{"type": "text", "data": {"text": "111"}}],
    #     "message_format": "array",
    #     "post_type": "message",
    #     "target_id": 183734182,
    # }
    message_type = data["message_type"]
    user_id = data.get("user_id")
    group_id = data.get("group_id")
    message = data["raw_message"].split(" ")[-1]
    await send_message(client, message_type, user_id, group_id, message)
    return
