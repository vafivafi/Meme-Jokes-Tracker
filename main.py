from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from db import setting
from models import Base
import uvicorn
from external_fetcher import jokes
from crud import crud
from schemas import JokeSchema, VoteCchema
from log import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with setting.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/jokes/random", tags=["jokes"], summary="Получить рандомную шутку")
async def random_jokes():
    try:    
        await jokes.joke_website()
        logger.info("Функция random_jokes завершила работу нормально")
        return {"joke" : jokes.joke_text, "ok" : True}
    except HTTPException as e:
        logger.error(f"Ошибка FastAPI {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка {e}")

@app.post("/jokes", tags=["jokes"], summary="Получить шутку от пользователя")
async def add_jokes(addjoke: JokeSchema):
    try:    
        await crud.add_joke(addjoke)
        logger.info("Функция add_jokes завершила работу нормально")
        return {"message": "шутка добавлена", "joke": addjoke}
    except HTTPException as e:
        logger.error(f"Ошибка FastAPI {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка {e}")

@app.patch("/jokes/{id}/vote", tags=["jokes"], summary="Обновить айди у шутки")
async def update_rating(id: int, vote: VoteCchema):
    joke = await crud.pathc_joke(id, vote.vote)
    if not joke:
        logger.warning(f"Шутка с id = {id} не найдена")
        raise HTTPException(status_code=404, detail="Шутка не найдена")
    logger.info("Функция update_rating выполнила свою работу")
    return {"message": "Рейтинг обновлен", "joke": joke.text, "rating": joke.rating}






if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
 