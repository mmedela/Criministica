from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from sqlalchemy.orm import Session
from DB.models.Province import Province
from schemas.province_schema import ProvinceCreate, ProvinceUpdate
from sqlalchemy.exc import IntegrityError
import csv
from io import StringIO

def get_provincias(db: Session):
    return db.query(Province).all()

def get_provincia(db: Session, provincia_id: int):
    return db.query(Province).filter(Province.province_id == provincia_id).first()

def create_provincia(db: Session, provincia: ProvinceCreate):
    new_provincia = Province(
        provincia_id=provincia.provincia_id, 
        poblacion=provincia.population,  
        provincia_nombre=provincia.province_name
    )
    db.add(new_provincia)
    try:
        db.commit()
        db.refresh(new_provincia)
        return new_provincia
    except IntegrityError:
        db.rollback()
        return None

def update_provincia(db: Session, provincia_id: int, provincia_data: ProvinceUpdate):
    provincia = db.query(Province).filter(Province.province_id == provincia_id).first()
    if not provincia:
        return None
    
    provincia.province_name = provincia_data.provincia_nombre
    
    if provincia_data.population is not None:
        provincia.population = provincia_data.population
    
    db.commit()
    db.refresh(provincia)
    return provincia

def delete_provincia(db: Session, provincia_id: int):
    provincia = db.query(Province).filter(Province.province_id == provincia_id).first()
    if not provincia:
        return None
    db.delete(provincia)
    db.commit()
    return provincia

def actualizar_poblacion_desde_csv(db: Session, file_content: str):
    reader = csv.reader(StringIO(file_content))
    next(reader, None)

    actualizadas = 0
    for row in reader:
        if len(row) < 2:
            continue
        try:
            provincia_id = int(row[0])
            poblacion = int(row[1])
        except ValueError:
            continue 
        provincia = db.query(Province).filter(Province.province_id == provincia_id).first()
        if provincia:
            provincia.population = poblacion
            actualizadas += 1

    db.commit()
    return {"message": f"Población actualizada para {actualizadas} provincias"}

def update_provincias_batch(db: Session, updates: List[ProvinceUpdate]) -> int:
    try:
        db.bulk_update_mappings(Province, [update.dict() for update in updates])
        db.commit()
        return len(updates)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating provinces: {e}")

def delete_provincias_batch(db: Session, provincia_ids: List[int]) -> int:
    try:
        stmt = db.delete(Province).where(Province.province_id.in_(provincia_ids))
        result = db.execute(stmt)
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="No provinces found to delete")
        return result.rowcount
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting provinces: {e}")

def get_provincias_batch(db: Session, provincia_ids: List[int]) -> List[Province]:
    provincias = db.query(Province).filter(Province.province_id.in_(provincia_ids)).all()
    if not provincias:
        raise HTTPException(status_code=404, detail="No provinces found")
    return provincias