from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from sqlalchemy.orm import Session
from DB.models.Crime import Crime
from schemas.crime_schema import CrimeCreate, CrimeUpdate

def get_all_crimes_service(db: Session):
    return db.query(Crime).all()

def get_crime_by_id_service(db: Session, crime_id: int):
    return db.query(Crime).filter(Crime.crime_code_snic_id == crime_id).first()

def create_crime_service(db: Session, crime_data: CrimeCreate):
    new_crime = Crime(**crime_data.dict())
    db.add(new_crime)
    db.commit()
    db.refresh(new_crime)
    return new_crime

def update_crime_service(db: Session, crime_id: int, crime_data: CrimeUpdate):
    crime = get_crime_by_id_service(db, crime_id)
    if crime:
        for key, value in crime_data.dict(exclude_unset=True).items():
            setattr(crime, key, value)
        db.commit()
        db.refresh(crime)
    return crime

def delete_crime_service(db: Session, crime_id: int):
    crime = get_crime_by_id_service(db, crime_id)
    if crime:
        db.delete(crime)
        db.commit()
    return crime

def create_crimes_service(db: Session, crimes: List[CrimeCreate]):
    try:
        db.bulk_insert_mappings(Crime, [d.dict() for d in crimes])
        db.commit()
        return len(crimes)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error inserting crimes")
                    
def update_crimes_service(db: Session, updates: List[CrimeUpdate]):
    try:
        db.bulk_update_mappings(Crime, [u.dict() for u in updates])
        db.commit()
        return len(updates)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating crimes")
    
def delete_crimes_service(db: Session, crimes_ids: List[int]):
    try:
        stmt = db.delete(Crime).where(Crime.crime_code_snic_id.in_(crimes_ids))
        result = db.execute(stmt)
        db.commit()
        return result.rowcount
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting crimes")


def get_batch_crimes_service(db: Session, crimes_ids: List[int]):
    return db.query(Crime).filter(Crime.crime_code_snic_id.in_(crimes_ids)).all()
    