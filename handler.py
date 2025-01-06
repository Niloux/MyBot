"""动态事件处理和定时任务处理"""

import logging
import json
import asyncio
from typing import Callable, Dict

from websocket import WebSocketClient
from module.echo import echo
from module.weather import forcast


class WebSocketHandler:
    def __init__(self, client: WebSocketClient):
        self.client = client
        self.event_handlers: Dict[str, Callable] = {}  # 存储事件处理函数
        self.schedule_handlers: list[Callable] = []  # 存储定时任务处理函数

        self.register_event("/echo", echo)
        self.register_event("/weather", forcast)

    def register_event(self, event_name: str, handler: Callable):
        """注册事件处理函数"""
        self.event_handlers[event_name] = handler

    def register_schedule(self, handler: Callable):
        """注册定时任务"""
        self.schedule_handlers.append(handler)

    async def handle_event(self, response: str):
        """处理接收到的消息，调用相应的事件处理函数以及执行定时任务"""
        try:
            data = json.loads(response)
            event_name = data.get("raw_message")
            # 对事件进行解析(很蠢的一刀切解析方式...但目前能用)
            if event_name:
                event_name = event_name.split(" ")[0]
                logging.info(f"Received event: {event_name}")
            if event_name in self.event_handlers:
                handler = self.event_handlers[event_name]
                await handler(self.client, data)
            else:
                pass
                # logging.warning(f"Unrecognized event: {event_name}")
        except json.JSONDecodeError:
            logging.error("Failed to parse response as JSON")
        except Exception as e:
            logging.error(f"Error handling event: {e}")
