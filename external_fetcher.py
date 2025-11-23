import aiohttp
import asyncio
from schemas import JokeSchema
from db import setting
from models import JokeOrm
from log import logger

class Jokes():
    try:    
        def __init__(self):
            self.url = "https://v2.jokeapi.dev/joke/Any"

        async def joke_website(self):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as resp:
                    data = await resp.json()
                    if data.get("type") == "single":
                        self.joke_text = data["joke"]
                    elif data.get("type") == "twopart":
                        self.joke_text = f"{data['setup']} — {data['delivery']}"
                    else:
                        self.joke_text = f"Нет шутки в ответе: {data}"


                    async with setting.async_session_factory() as db_session:
                        joke = JokeOrm(text = self.joke_text)
                        db_session.add(joke)
                        await db_session.commit()
                        logger.info("Функция joke_website завершила работу нормально")
    except Exception as e:
        logger.error(f"Неизвестная ошибка {e}")
 

jokes = Jokes()