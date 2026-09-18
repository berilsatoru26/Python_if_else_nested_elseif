from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GuideLinkResponse(BaseModel):
    id: int
    game: str
    title: str
    url: str
    tags_json: list[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
