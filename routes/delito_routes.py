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

router = APIRouter(prefix="/delitos", tags=["Delitos"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CrimeResponse])
def listar_delitos(db: Session = Depends(get_db)):
    return get_all_crimes_service(db)

@router.get("/{delito_id}", response_model=CrimeResponse)
def obtener_delito(delito_id: int, db: Session = Depends(get_db)):
    delito = get_crime_by_id_service(db, delito_id)
    if not delito:
        raise HTTPException(status_code=404, detail="Delito no encontrado")
    return delito

@router.post("/", response_model=CrimeResponse)
def agregar_delito(delito: CrimeCreate, db: Session = Depends(get_db)):
    return create_crime_service(db, delito)

@router.put("/{delito_id}", response_model=CrimeResponse)
def modificar_delito(delito_id: int, delito: CrimeUpdate, db: Session = Depends(get_db)):
    return update_crime_service(db, delito_id, delito)

@router.delete("/{delito_id}")
def eliminar_delito(delito_id: int, db: Session = Depends(get_db)):
    delete_crime_service(db, delito_id)
    return {"message": "Delito eliminado exitosamente"}

@router.post("/batch", status_code=201)
def create_delitos(delitos: List[CrimeCreate], db: Session = Depends(get_db)):
    delitos = create_crimes_service(db, delitos)
    return {"message": f"{delitos} delitos added successfully"}

@router.put("/batch")
def update_delitos(updates: List[CrimeUpdate], db: Session = Depends(get_db)):
    result = update_crimes_service(db, updates)
    return {"message": f"{result} delitos updated successfully"}

@router.delete("/batch")
def delete_crimes_service(delito_ids: List[int], db: Session = Depends(get_db)):
    rows_deleted = delete_crimes_service(delito_ids, db)
    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail="No delitos found to delete")
    return {"message": f"{rows_deleted} delitos deleted successfully"}

@router.get("/batch", response_model=List[CrimeCreate])
def get_batch_crimes_service(delito_ids: List[int] = Query(...), db: Session = Depends(get_db)):
    delitos = get_batch_crimes_service(delito_ids, db)
    if not delitos:
        raise HTTPException(status_code=404, detail="No delitos found")
    return delitos