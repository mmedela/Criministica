from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from sqlalchemy.orm import Session
from DB.models.Province import Province
from schemas.province_schema import ProvinceCreate, ProvinceUpdate
from sqlalchemy.exc import IntegrityError
import csv
from io import StringIO

def get_provinces_service(db: Session):
    return db.query(Province).all()

def get_province_service(db: Session, province_id: int):
    return db.query(Province).filter(Province.province_id == province_id).first()

def create_province_service(db: Session, province: ProvinceCreate):
    new_province = Province(
        province_id=province.province_id, 
        population=province.population,  
        province_name=province.province_name
    )
    db.add(new_province)
    try:
        db.commit()
        db.refresh(new_province)
        return new_province
    except IntegrityError:
        db.rollback()
        return None

def update_province_service(db: Session, province_id: int, province_data: ProvinceUpdate):
    province = db.query(Province).filter(Province.province_id == province_id).first()
    if not province:
        return None
    
    province.province_name = province_data.province_name
    
    if province_data.population is not None:
        province.population = province_data.population
    
    db.commit()
    db.refresh(province)
    return province

def delete_province_service(db: Session, province_id: int):
    province = db.query(Province).filter(Province.province_id == province_id).first()
    if not province:
        return None
    db.delete(province)
    db.commit()
    return province

def update_population_with_csv_service(db: Session, file_content: str):
    
    PROVINCE_ID = 0
    PROVINCE_POPULATION = 1
    reader = csv.reader(StringIO(file_content))
    next(reader, None)

    updated_provinces = 0
    for row in reader:
        if len(row) < 2:
            continue
        try:
            province_id = int(row[PROVINCE_ID])
            population = int(row[PROVINCE_POPULATION])
        except ValueError:
            continue 
        province = db.query(Province).filter(Province.province_id == province_id).first()
        if province:
            province.population = population
            updated_provinces += 1

    db.commit()
    return {"message": f"Population updated successfully for {updated_provinces} provinces"}

def update_provinces_batch_service(db: Session, updates: List[ProvinceUpdate]) -> int:
    try:
        db.bulk_update_mappings(Province, [update.dict() for update in updates])
        db.commit()
        return len(updates)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating provinces: {e}")

def delete_provinces_batch_service(db: Session, province_ids: List[int]) -> int:
    try:
        stmt = db.delete(Province).where(Province.province_id.in_(province_ids))
        result = db.execute(stmt)
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="No provinces found to delete")
        return result.rowcount
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting provinces: {e}")

def get_provinces_batch_service(db: Session, provinces_ids: List[int]) -> List[Province]:
    provinces = db.query(Province).filter(Province.province_id.in_(provinces_ids)).all()
    if not provinces:
        raise HTTPException(status_code=404, detail="No provinces found")
    return provinces