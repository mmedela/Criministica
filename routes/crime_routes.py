from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete
from sqlalchemy.orm import Session
from DB.init_db import session
from DB.models.Crime import Crime
from services.crimes_service import (
    get_all_crimes_service,
    get_crime_by_id_service,
    create_crime_service,
    delete_crime_service,
    update_crime_service,
    get_batch_crimes_service,
    delete_crimes_service,
    update_crimes_service,
    create_crimes_service
)
from schemas.crime_schema import CrimeCreate, CrimeResponse, CrimeUpdate
from typing import List

router = APIRouter(prefix="/crimes", tags=["Delitos"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CrimeResponse])
def list_crimes(db: Session = Depends(get_db)):
    return get_all_crimes_service(db)

@router.get("/{crime_id}", response_model=CrimeResponse)
def get_crime(crime_id: int, db: Session = Depends(get_db)):
    crime = get_crime_by_id_service(db, crime_id)
    if not crime:
        raise HTTPException(status_code=404, detail="Crime not found")
    return crime

@router.post("/", response_model=CrimeResponse)
def create_crime(crime: CrimeCreate, db: Session = Depends(get_db)):
    return create_crime_service(db, crime)


@router.post("/batch", status_code=201)
def create_crimes(crimes: List[CrimeCreate], db: Session = Depends(get_db)):
    crimes = create_crimes_service(db, crimes)
    return {"message": f"{crimes} crimes added successfully"}

@router.put("/batch")
def update_crimes(updates: List[CrimeUpdate], db: Session = Depends(get_db)):
    result = update_crimes_service(db, updates)
    return {"message": f"{result} crimes updated successfully"}

@router.delete("/batch")
def delete_crimes(crimes_ids: List[int], db: Session = Depends(get_db)):
    rows_deleted = delete_crimes_service(crimes_ids, db)
    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail="No crimes found to delete")
    return {"message": f"{rows_deleted} crimes deleted successfully"}

@router.get("/batch", response_model=List[CrimeCreate])
def get_batch_crimes(crimes_ids: List[int] = Query(...), db: Session = Depends(get_db)):
    crimes = get_batch_crimes_service(crimes_ids, db)
    if not crimes:
        raise HTTPException(status_code=404, detail="No crimes found")
    return crimes

@router.put("/{crime_id}", response_model=CrimeResponse)
def modificar_delito(crime_id: int, crime: CrimeUpdate, db: Session = Depends(get_db)):
    return update_crime_service(db, crime_id, crime)

@router.delete("/{crime_id}")
def eliminar_delito(crime_id: int, db: Session = Depends(get_db)):
    delete_crime_service(db, crime_id)
    return {"message": "Delito eliminado exitosamente"}
