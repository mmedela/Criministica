from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete
from sqlalchemy.orm import Session
from DB.init_db import session
from DB.models.Delito import Delito
from services.delito_service import (
    get_all_delitos_service,
    get_delito_by_id_service,
    create_delito_service,
    delete_delito_service,
    update_delito_service,
    get_batch_delitos_service,
    delete_delitos_service,
    update_delitos_service,
    create_delitos_service
)
from schemas.delito_schema import DelitoCreate, DelitoResponse, DelitoUpdate
from typing import List

router = APIRouter(prefix="/delitos", tags=["Delitos"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[DelitoResponse])
def listar_delitos(db: Session = Depends(get_db)):
    return get_all_delitos_service(db)

@router.get("/{delito_id}", response_model=DelitoResponse)
def obtener_delito(delito_id: int, db: Session = Depends(get_db)):
    delito = get_delito_by_id_service(db, delito_id)
    if not delito:
        raise HTTPException(status_code=404, detail="Delito no encontrado")
    return delito

@router.post("/", response_model=DelitoResponse)
def agregar_delito(delito: DelitoCreate, db: Session = Depends(get_db)):
    return create_delito_service(db, delito)

@router.put("/{delito_id}", response_model=DelitoResponse)
def modificar_delito(delito_id: int, delito: DelitoUpdate, db: Session = Depends(get_db)):
    return update_delito_service(db, delito_id, delito)

@router.delete("/{delito_id}")
def eliminar_delito(delito_id: int, db: Session = Depends(get_db)):
    delete_delito_service(db, delito_id)
    return {"message": "Delito eliminado exitosamente"}

@router.post("/batch", status_code=201)
def create_delitos(delitos: List[DelitoCreate], db: Session = Depends(get_db)):
    delitos = create_delitos_service(db, delitos)
    return {"message": f"{delitos} delitos added successfully"}

@router.put("/batch")
def update_delitos(updates: List[DelitoUpdate], db: Session = Depends(get_db)):
    result = update_delitos_service(db, updates)
    return {"message": f"{result} delitos updated successfully"}

@router.delete("/batch")
def delete_delitos_service(delito_ids: List[int], db: Session = Depends(get_db)):
    rows_deleted = delete_delitos_service(delito_ids, db)
    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail="No delitos found to delete")
    return {"message": f"{rows_deleted} delitos deleted successfully"}

@router.get("/batch", response_model=List[DelitoCreate])
def get_batch_delitos_service(delito_ids: List[int] = Query(...), db: Session = Depends(get_db)):
    delitos = get_batch_delitos_service(delito_ids, db)
    if not delitos:
        raise HTTPException(status_code=404, detail="No delitos found")
    return delitos