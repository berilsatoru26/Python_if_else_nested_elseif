from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LinkedAccountCreate(BaseModel):
    game: str = Field(min_length=1, max_length=100)
    provider: str = Field(min_length=1, max_length=100)
    region: str = Field(min_length=1, max_length=50)
    external_account_id: str = Field(min_length=1, max_length=200)


class LinkedAccountResponse(BaseModel):
    id: int
    game: str
    provider: str
    region: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProgressSnapshotResponse(BaseModel):
    id: int
    snapshot_time: datetime
    level: int
    world_level: int
    stats_json: dict

    model_config = ConfigDict(from_attributes=True)


class CharacterResponse(BaseModel):
    id: int
    character_name: str
    rarity: int
    level: int
    element: str
    metadata_json: dict

    model_config = ConfigDict(from_attributes=True)


class AchievementResponse(BaseModel):
    id: int
    achievement_key: str
    title: str
    is_unlocked: bool
    unlocked_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
