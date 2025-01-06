# WebSocket 客户端 - Napcat 消息平台适配器

本项目实现了一个 WebSocket 客户端，通过与本地的 Napcat 消息平台服务连接，获取城市天气信息并将其推送到 Napcat 平台。客户端通过调用腾讯地图 API 获取城市的经纬度，并利用 OpenWeather API 获取天气信息。

## 功能

- 获取指定城市的经纬度
- 获取城市的天气信息（温度、湿度、风速等）
- 通过 WebSocket 将天气信息推送至 Napcat 消息平台

## 环境要求

- Python 3.x
- `napcat` 服务（需在本地运行）
- `aiohttp`：用于异步 HTTP 请求
- `websockets`：用于 WebSocket 客户端连接

## 安装依赖

首先，确保你的环境中已经安装了 `napcat` 服务，并且该服务正在本地运行，监听在 3000 端口。

然后安装 Python 依赖：

```bash
pip install aiohttp websockets
```

## 查询天气示例

/weather {地点}