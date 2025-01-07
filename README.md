# WebSocket 客户端 - Napcat 消息平台适配器

本项目实现了一个 WebSocket 客户端，通过与本地的 Napcat 消息平台服务连接，帮助自己以及qq群群友们获得一些生活上的小帮助。

## 功能

- 获取城市的天气信息（温度、湿度、风速等）
- 解决宇宙终极难题今天到底吃点啥，收录了https://cook.aiursoft.cn/的一些食谱
- 通过 WebSocket 将信息推送至 Napcat 消息平台

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

## 今天吃点啥示例
/eat_help

/what_we_have {食物种类}

/what_to_eat {食物种类}

/how_to_cook {食物名称}