from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import Optional, List

class SongCRUD:
    """Clase para operaciones CRUD de canciones"""
    
    def create_song(self, db: Session, song: schemas.SongCreate) -> models.Song:
        """Crear una nueva canción"""
        db_song = models.Song(
            name=song.SONG_NAME,
            path=song.SONG_PATH,
            plays=song.PLAYS
        )
        db.add(db_song)
        db.commit()
        db.refresh(db_song)
        return db_song
    
    def get_song(self, db: Session, song_id: int) -> Optional[models.Song]:
        """Obtener una canción por ID"""
        return db.query(models.Song).filter(models.Song.id == song_id).first()
    
    def get_songs(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Song]:
        """Obtener lista de canciones con paginación"""
        return db.query(models.Song).order_by(models.Song.id).offset(skip).limit(limit).all()
    
    def get_songs_count(self, db: Session) -> int:
        """Obtener el total de canciones"""
        return db.query(func.count(models.Song.id)).scalar()
    
    def search_songs_by_name(self, db: Session, name: str, skip: int = 0, limit: int = 100) -> List[models.Song]:
        """Buscar canciones por nombre"""
        return db.query(models.Song).filter(
            models.Song.name.contains(name)
        ).order_by(models.Song.id).offset(skip).limit(limit).all()
    
    def update_song(self, db: Session, song_id: int, song_update: schemas.SongUpdate) -> Optional[models.Song]:
        """Actualizar una canción"""
        db_song = self.get_song(db, song_id)
        if db_song:
            update_data = song_update.model_dump(exclude_unset=True)
            # Mapear campos del schema a los del modelo
            field_map = {
                'SONG_NAME': 'name',
                'SONG_PATH': 'path',
                'PLAYS': 'plays'
            }
            for field, value in update_data.items():
                setattr(db_song, field_map.get(field, field), value)
            db.commit()
            db.refresh(db_song)
        return db_song
    
    def delete_song(self, db: Session, song_id: int) -> bool:
        """Eliminar una canción"""
        db_song = self.get_song(db, song_id)
        if db_song:
            db.delete(db_song)
            db.commit()
            return True
        return False
    
    def increment_plays(self, db: Session, song_id: int) -> Optional[models.Song]:
        """Incrementar el contador de reproducciones"""
        db_song = self.get_song(db, song_id)
        if db_song:
            db_song.plays += 1
            db.commit()
            db.refresh(db_song)
        return db_song

# Instancia global del CRUD
song_crud = SongCRUD()