import requests
import logging
import aiohttp
from datetime import datetime, timedelta
from urllib.parse import quote


from module.message import send_message

WEATHER_KEY = "d2781ca364e25b47435537dafa7817ed"
LOCATION_KEY = "NYMBZ-RAGWL-IWVPG-MVAJK-7THT5-O4FUJ"

LOCATION = {
    "上海": (31.14, 121.29),
    "北京": (39.91, 116.39),
    "武汉": (30.59, 114.31),
    "长沙": (28.21, 112.97),
}


async def fetch_json(url):
    """通用的异步 GET 请求函数，返回 JSON 数据"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_location(city):
    """调用腾讯地图接口，根据城市获取经纬度"""
    city = quote(city)
    url = f"https://apis.map.qq.com/ws/geocoder/v1/?address={city}&key={LOCATION_KEY}"

    data = await fetch_json(url)
    if data.get("status") != 0:
        logging.error(f"获取经纬度失败: {data.get('message')}")
        return None, None

    location = data.get("result", {}).get("location", {})
    return location.get("lat"), location.get("lng")


async def get_weather(lat, lon):
    """调用天气接口，根据经纬度获取天气信息"""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_KEY}&lang=zh_cn"

    data = await fetch_json(url)
    if not data:
        logging.error("获取天气信息失败")
        return "无法获取天气信息, 可能是网络异常, 请重试"

    location = data.get("name", "未知地点")
    weather = data.get("weather", [{}])[0].get("description", "未知天气")
    main = data.get("main", {})
    temperature_c = main.get("temp", 0) - 273.15
    temperature_feel = main.get("feels_like", 0) - 273.15
    humidity = main.get("humidity", 0)
    wind_speed = data.get("wind", {}).get("speed", 0)
    visibility = data.get("visibility", 0) / 1000  # 转换为公里

    return (
        f"地点: {location}\n"
        f"天气状况: {weather}\n"
        f"当前温度: {temperature_c:.2f}°C\n"
        f"体感温度: {temperature_feel:.2f}°C\n"
        f"湿度: {humidity}%\n"
        f"风速: {wind_speed} m/s\n"
        f"能见度: {visibility:.1f} km"
    )


async def forcast(client, data=None):
    """根据城市名称获取天气信息并发送消息"""
    city = data.get("raw_message", "").split(" ")[-1]
    lat, lon = await get_location(city)

    if lat is None or lon is None:
        msg = f"无法获取城市 {city} 的经纬度信息，请检查输入是否正确。"
    else:
        msg = await get_weather(lat, lon)

    # 统一消息发送
    await send_message(
        client,
        message_type=data.get("message_type"),
        user_id=data.get("user_id"),
        group_id=data.get("group_id"),
        msg=msg,
    )


# async def forcast(client, data=None):
#     message_type = data.get("message_type")

#     for city, (lat, lon) in LOCATION.items():
#         msg = await get_weather(city, lat, lon)
#         # 通过 send_message 函数统一处理消息发送
#         await send_message(
#             client,
#             message_type,
#             user_id=data.get("user_id"),
#             group_id=data.get("group_id"),
#             msg=msg,
#         )
#     return


async def schedule_forcast(client):
    """每天早上八点发送天气信息"""
    while True:
        now = datetime.now()
        # 计算下一次执行时间（明天早上 8 点）
        next_run = datetime.combine(
            now.date() + timedelta(days=1), datetime.min.time()
        ) + timedelta(hours=8)
        delay = (next_run - now).total_seconds()

        logging.info(f"下一次任务将在 {next_run} 运行，延迟 {delay} 秒")
