from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    message: Message


class OpenAIResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: dict
    choices: List[Choice]
