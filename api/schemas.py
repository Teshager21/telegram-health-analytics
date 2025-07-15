from pydantic import BaseModel

# from typing import List


class TopProduct(BaseModel):
    product: str
    mentions: int


class ChannelActivity(BaseModel):
    channel_name: str
    day: str
    messages: int


class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
