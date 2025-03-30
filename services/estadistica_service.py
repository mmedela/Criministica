from sqlalchemy.orm import Session
from ..DB.models.EstadisticaDelito import EstadisticaDelito
from schemas.estadistica_schema import EstadisticaCreate, EstadisticaUpdate

def get_estadisticas(db: Session, provincia_id: int = None, delito_id: int = None, anio: int = None):
    query = db.query(EstadisticaDelito)
    if provincia_id:
        query = query.filter(EstadisticaDelito.provincia_id == provincia_id)
    if delito_id:
        query = query.filter(EstadisticaDelito.codigo_delito_snic_id == delito_id)
    if anio:
        query = query.filter(EstadisticaDelito.anio == anio)
    return query.all()

def get_estadistica_by_id(db: Session, estadistica_id: int):
    return db.query(EstadisticaDelito).filter(EstadisticaDelito.id == estadistica_id).first()

def create_estadistica(db: Session, estadistica_data: EstadisticaCreate):
    new_estadistica = EstadisticaDelito(**estadistica_data.dict())
    db.add(new_estadistica)
    db.commit()
    db.refresh(new_estadistica)
    return new_estadistica

def update_estadistica(db: Session, estadistica_id: int, estadistica_data: EstadisticaUpdate):
    estadistica = get_estadistica_by_id(db, estadistica_id)
    if estadistica:
        for key, value in estadistica_data.dict(exclude_unset=True).items():
            setattr(estadistica, key, value)
        db.commit()
        db.refresh(estadistica)
    return estadistica

def delete_estadistica(db: Session, estadistica_id: int):
    estadistica = get_estadistica_by_id(db, estadistica_id)
    if estadistica:
        db.delete(estadistica)
        db.commit()
    return estadistica
