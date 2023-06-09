import uuid
from pydantic import BaseModel, Field
from typing import Optional


class Song(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    attributes: object = Field(None)
    duration: int = Field(...)
    rating: float = Field(...)
    url: str = Field(None)
    playlist_id: str = Field(None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Forest of Jnana and Vidya",
                "attributes": [
                    "Genshin Impact"
                ],
                "duartion": 65,
                "rating": 4.5,
                "url": "public/songs/a-call-to-the-soul.mp3",
                "playlist_id": 2
            }
        }

class SongUpdate(BaseModel):
    name: Optional[str]
    attributes: Optional[object]
    duration: Optional[int]
    rating: Optional[float]
    url: Optional[str]
    playlist_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Forest of Jnana and Vidya",
                "attributes": [
                    "Genshin Impact"
                ],
                "duartion": 65,
                "rating": 4.5,
                "url": "public/songs/a-call-to-the-soul.mp3",
                "playlist_id": 2
            }
        }