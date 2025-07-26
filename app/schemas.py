from pydantic import BaseModel, Field
from typing import Optional

class SongBase(BaseModel):
    """Schema base para Song"""
    SONG_NAME: str = Field(..., min_length=1, max_length=255, description="Nombre de la canción")
    SONG_PATH: str = Field(..., min_length=1, max_length=500, description="Ruta o URL de la canción")
    PLAYS: int = Field(default=0, ge=0, description="Número de reproducciones")

class SongCreate(SongBase):
    """Schema para crear una canción"""
    pass

class SongUpdate(BaseModel):
    """Schema para actualizar una canción"""
    SONG_NAME: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre de la canción")
    SONG_PATH: Optional[str] = Field(None, min_length=1, max_length=500, description="Ruta o URL de la canción")
    PLAYS: Optional[int] = Field(None, ge=0, description="Número de reproducciones")


class SongResponse(BaseModel):
    id: int
    name: str
    path: str
    plays: int
    class Config:
        orm_mode = True

class SongListResponse(BaseModel):
    songs: list[SongResponse]
    total: int
    page: int
    size: int
    
class MessageResponse(BaseModel):
    """Schema para mensajes de respuesta"""
    message: str