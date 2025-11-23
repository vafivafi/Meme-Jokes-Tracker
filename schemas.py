from pydantic import BaseModel

class JokeSchema(BaseModel):
    text: str