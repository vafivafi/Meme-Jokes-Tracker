from db import setting
from models import JokeOrm
from log import logger


class CRUD():
    def __init__(self):
        pass

    async def add_joke(self, addjoke: str):
        try:    
            async with setting.async_session_factory() as session:
                new_joke = JokeOrm(text = addjoke.text)
                session.add(new_joke)
                await session.commit()
        except Exception as e:
            logger.error(f"Неизвестная ошибка {e}")
            

crud = CRUD()