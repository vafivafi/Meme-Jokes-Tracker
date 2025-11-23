from pydantic import BaseModel

class JokeSchema(BaseModel):
    text: str

class VoteCchema(BaseModel):
    vote: str