from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsItemResponse(BaseModel):
    id: int
    game: str
    category: str
    title: str
    content: str
    url: str
    code_value: str | None
    valid_from: datetime | None
    valid_to: datetime | None
    published_at: datetime

    model_config = ConfigDict(from_attributes=True)
