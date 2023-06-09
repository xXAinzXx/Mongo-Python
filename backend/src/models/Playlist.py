import uuid
from pydantic import BaseModel, Field
from typing import Optional
from src.models.Song import Song

class Playlist(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    songs: list = Field(None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Test",
                "songs": []
            }
        }

class PlaylistCreate(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    songs: list = Field(None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Test",
                "songs": [1,2,3]
            }
        }

class PlaylistUpdate(BaseModel):
    name: Optional[str]
    songs: Optional[list]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Test",
                "songs": []
            }
        }