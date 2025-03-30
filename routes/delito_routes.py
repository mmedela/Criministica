from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DB.init_db import session
from services.delito_service import (
    get_delitos,
    get_delito_by_id,
    create_delito,
    delete_delito,
    update_delito
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
    return get_delitos(db)

@router.get("/{delito_id}", response_model=DelitoResponse)
def obtener_delito(delito_id: int, db: Session = Depends(get_db)):
    delito = get_delito_by_id(db, delito_id)
    if not delito:
        raise HTTPException(status_code=404, detail="Delito no encontrado")
    return delito

@router.post("/", response_model=DelitoResponse)
def agregar_delito(delito: DelitoCreate, db: Session = Depends(get_db)):
    return create_delito(db, delito)

@router.put("/{delito_id}", response_model=DelitoResponse)
def modificar_delito(delito_id: int, delito: DelitoUpdate, db: Session = Depends(get_db)):
    return update_delito(db, delito_id, delito)

@router.delete("/{delito_id}")
def eliminar_delito(delito_id: int, db: Session = Depends(get_db)):
    delete_delito(db, delito_id)
    return {"message": "Delito eliminado exitosamente"}
