from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from . import schemas, models
from .database import get_db
from .crud import song_crud
import math

router = APIRouter()

@router.get("/", response_model=schemas.MessageResponse)
async def root():
    """Endpoint raíz del microservicio"""
    return {"message": "Microservicio de Canciones - API REST CRUD"}

@router.get("/health", response_model=schemas.MessageResponse)
async def health_check():
    """Endpoint para verificar el estado del servicio"""
    return {"message": "Service is healthy"}

@router.post("/songs", response_model=schemas.SongResponse, status_code=201)
async def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    """Crear una nueva canción"""
    try:
        db_song = song_crud.create_song(db=db, song=song)
        return db_song
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear la canción: {str(e)}")

@router.get("/songs/{song_id}", response_model=schemas.SongResponse)
async def get_song(song_id: int, db: Session = Depends(get_db)):
    """Obtener una canción por ID"""
    db_song = song_crud.get_song(db=db, song_id=song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return db_song

@router.get("/songs", response_model=schemas.SongListResponse)
async def get_songs(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    search: Optional[str] = Query(None, description="Buscar por nombre de canción"),
    db: Session = Depends(get_db)
):
    """Obtener lista de canciones con paginación y búsqueda"""
    skip = (page - 1) * size
    
    try:
        if search:
            songs = song_crud.search_songs_by_name(db=db, name=search, skip=skip, limit=size)
            # Para simplicidad, usaremos el total general (en producción se debería optimizar)
            total = song_crud.get_songs_count(db=db)
        else:
            songs = song_crud.get_songs(db=db, skip=skip, limit=size)
            total = song_crud.get_songs_count(db=db)
        
        return {
            "songs": songs,
            "total": total,
            "page": page,
            "size": size
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener las canciones: {str(e)}")

@router.put("/songs/{song_id}", response_model=schemas.SongResponse)
async def update_song(song_id: int, song_update: schemas.SongUpdate, db: Session = Depends(get_db)):
    """Actualizar una canción completamente"""
    db_song = song_crud.update_song(db=db, song_id=song_id, song_update=song_update)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return db_song

@router.patch("/songs/{song_id}", response_model=schemas.SongResponse)
async def partial_update_song(song_id: int, song_update: schemas.SongUpdate, db: Session = Depends(get_db)):
    """Actualizar parcialmente una canción"""
    db_song = song_crud.update_song(db=db, song_id=song_id, song_update=song_update)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return db_song

@router.delete("/songs/{song_id}", response_model=schemas.MessageResponse)
async def delete_song(song_id: int, db: Session = Depends(get_db)):
    """Eliminar una canción"""
    success = song_crud.delete_song(db=db, song_id=song_id)
    if not success:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return {"message": f"Canción con ID {song_id} eliminada exitosamente"}

@router.patch("/songs/{song_id}/play", response_model=schemas.SongResponse)
async def play_song(song_id: int, db: Session = Depends(get_db)):
    """Incrementar el contador de reproducciones de una canción"""
    db_song = song_crud.increment_plays(db=db, song_id=song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return db_song