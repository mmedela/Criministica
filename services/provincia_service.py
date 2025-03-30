from sqlalchemy.orm import Session
from ..DB.models.Provincia import Provincia
from ..schemas.provincia_schema import ProvinciaCreate, ProvinciaUpdate
from sqlalchemy.exc import IntegrityError

def get_provincias(db: Session):
    return db.query(Provincia).all()

def get_provincia(db: Session, provincia_id: int):
    return db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()

def create_provincia(db: Session, provincia: ProvinciaCreate):
    new_provincia = Provincia(provincia_id=provincia.provincia_id, provincia_nombre=provincia.provincia_nombre)
    db.add(new_provincia)
    try:
        db.commit()
        db.refresh(new_provincia)
        return new_provincia
    except IntegrityError:
        db.rollback()
        return None

def update_provincia(db: Session, provincia_id: int, provincia_data: ProvinciaUpdate):
    provincia = db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()
    if not provincia:
        return None
    provincia.provincia_nombre = provincia_data.provincia_nombre
    db.commit()
    db.refresh(provincia)
    return provincia

def delete_provincia(db: Session, provincia_id: int):
    provincia = db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()
    if not provincia:
        return None
    db.delete(provincia)
    db.commit()
    return provincia