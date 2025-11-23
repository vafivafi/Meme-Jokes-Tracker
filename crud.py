from db import setting
from models import JokeOrm
from log import logger
from schemas import JokeSchema
from sqlalchemy import select, values


class CRUD():
    def __init__(self):
        pass

    async def add_joke(self, addjoke: JokeSchema):
        try:    
            async with setting.async_session_factory() as session:
                new_joke = JokeOrm(text = addjoke.text)
                session.add(new_joke)
                await session.commit()
        except Exception as e:
            logger.error(f"Неизвестная ошибка {e}")

    async def pathc_joke(self, id: int, vote: str = None):
        try:
        
            async with setting.async_session_factory() as session:
                stmt = select(JokeOrm).where(JokeOrm.id == id)
                result = await session.execute(stmt)
                joke = result.scalar_one_or_none()

                if not joke:
                    logger.warning(f"Шутка с id = {id} не найдена")
                    return None
                
                if vote == "like":
                    joke.rating += 1

                if vote == "dislike":
                    joke.rating -= 1
                
                await session.commit()
                await session.refresh(joke)
                logger.info("Функция add_joke завершила работу нормально")
                return joke



        except Exception as e:
            logger.error(f"Неизвестная ошибка {e}")
            

crud = CRUD()