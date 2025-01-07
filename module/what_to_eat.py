"""吃点啥"""

import requests
import logging
import urllib.parse
import random
from module.message import send_message


class Recipes:
    """食谱获取与管理类"""

    BASE_URL = "https://cook.aiursoft.cn/search/search_index.json"
    TYPES = {
        "aquatic": "水产",
        "breakfast": "早餐",
        "condiment": "酱料",
        "dessert": "甜点",
        "drink": "饮品",
        "meat_dish": "肉类",
        "semi-finished": "半成品",
        "soup": "汤",
        "staple": "主食",
        "vegetable_dish": "素菜",
    }
    TYPES_ZH_TO_EN = {type_zh: type_en for type_en, type_zh in TYPES.items()}

    def __init__(self):
        self.recipes = {type_zh: set() for type_zh in self.TYPES.values()}
        self.cooks = []
        self._fetch_and_process_recipes()

    def _fetch_and_process_recipes(self):
        """从远程获取并处理食谱数据"""
        try:
            response = requests.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            data = response.json().get("docs", [])
            self._process_recipes(data)
        except requests.RequestException as e:
            logging.error(f"请求失败: {e}")
        except ValueError as e:
            logging.error(f"解析响应失败: {e}")

    def _process_recipes(self, data):
        """处理并分类存储食谱数据"""
        if not data:
            logging.error("未获取到食谱数据。")
            return

        for item in data:
            url = item.get("location")
            if not url or "dishes" not in url or "template" in url:
                continue

            self.cooks.append(url)
            parts = url.split("dishes/")
            if len(parts) < 2:
                continue

            category, dish_name_encoded = parts[1].split("/", 1)
            dish_name = urllib.parse.unquote(dish_name_encoded.split("/")[0])

            if category in self.TYPES:
                self.recipes[self.TYPES[category]].add(dish_name)
            else:
                logging.warning(f"未知分类: {category}")

    def all_recipes(self):
        """获取所有分类及菜品"""
        return self.recipes

    def random_recipe(self, category):
        """随机获取指定分类中的菜品"""
        if category not in self.recipes:
            logging.warning(f"未知分类: {category}")
            return f"未知分类: {category}"

        if not self.recipes[category]:
            logging.warning(f"分类 '{category}' 下没有菜品。")
            return f"分类 '{category}' 下没有菜品。"

        selected_dish = random.choice(list(self.recipes[category]))
        return f"推荐的{category}: {selected_dish}。"

    def help(self):
        """生成帮助信息"""
        msgs = ["分类及菜品数量:"]
        for category, dishes in self.recipes.items():
            msgs.append(f"{category}: {len(dishes)} 种菜品")
        msgs.append("可使用/what_we_have，获取指定分类下的菜品。")
        msgs.append("可使用/what_to_eat，随机挑选一个指定分类的菜品。")
        msgs.append("可使用/how_to_cook，获得指定菜品的制作方法。")
        return "\n".join(msgs)

    def how_to_cook(self, food):
        """获取菜品的制作方式"""
        category = next(
            (cat for cat, dishes in self.recipes.items() if food in dishes), None
        )

        if not category:
            logging.warning(f"未找到菜品: {food}")
            return f"未找到菜品: {food}"

        url_path = f"dishes/{self.TYPES_ZH_TO_EN[category]}/{urllib.parse.quote(food)}"
        for c in self.cooks:
            if url_path in c:
                return f"{food}的制作方式：\nhttps://cook.aiursoft.cn/{c}"

        logging.warning(f"未找到菜品的制作方式: {food}")
        return f"未找到 {food} 的制作方式。"

    def what_we_have(self, category):
        """获取指定分类下的菜品列表"""
        if category in self.recipes:
            foods = self.recipes[category]
            if foods:
                return f"{category}分类下的菜品有：\n" + "\n".join(foods)
            else:
                return f"{category}分类下暂时没有菜品。"
        else:
            return f"未知分类: {category}"


recipes = Recipes()


async def what_to_eat(client, data=None):
    """随机选择一道菜品"""
    category = data.get("raw_message", "").split(" ")[-1]
    msg = recipes.random_recipe(category)
    await send_message(
        client,
        message_type=data.get("message_type"),
        user_id=data.get("user_id"),
        group_id=data.get("group_id"),
        msg=msg,
    )


async def eat_help(client, data=None):
    """获取帮助信息"""
    msg = recipes.help()
    await send_message(
        client,
        message_type=data.get("message_type"),
        user_id=data.get("user_id"),
        group_id=data.get("group_id"),
        msg=msg,
    )


async def how_to_cook(client, data=None):
    """获取指定菜品的制作方式"""
    food = data.get("raw_message", "").split(" ")[-1]
    msg = recipes.how_to_cook(food)
    await send_message(
        client,
        message_type=data.get("message_type"),
        user_id=data.get("user_id"),
        group_id=data.get("group_id"),
        msg=msg,
    )

async def what_we_have(client, data=None):
    """获取指定分类下的菜品列表"""
    category = data.get("raw_message", "").split(" ")[-1]
    msg = recipes.what_we_have(category)
    await send_message(
        client,
        message_type=data.get("message_type"),
        user_id=data.get("user_id"),
        group_id=data.get("group_id"),
        msg=msg,
    )