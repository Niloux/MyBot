import logging
import asyncio
from handler import WebSocketHandler
from websocket import WebSocketClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # 设置日志输出格式
)

async def main():
    uri = "ws://localhost:3000"

    try:
        # 创建 WebSocket 客户端
        async with WebSocketClient(uri) as client:
            handler = WebSocketHandler(client)

            while client.is_connected:
                try:
                    # 接收消息
                    res = await client.receive()
                    await handler.handle_event(res)
                except Exception as e:
                    logging.error(f"Error during message handling: {e}")
                    break
    except Exception as e:
        logging.error(f"Error during WebSocket connection: {e}")

# 运行客户端
if __name__ == "__main__":
    asyncio.run(main())
