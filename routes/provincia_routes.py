from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..DB.init_db import session
from ..services.provincia_service import (
    get_provincias,
    get_provincia,
    create_provincia,
    update_provincia,
    delete_provincia
)
from ..schemas.provincia_schema import ProvinciaCreate, ProvinciaResponse, ProvinciaUpdate
from typing import List

router = APIRouter(prefix="/provincias", tags=["Provincias"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProvinciaResponse])
def listar_provincias(db: Session = Depends(get_db)):
    return get_provincias(db)

@router.get("/{provincia_id}", response_model=ProvinciaResponse)
def obtener_provincia(provincia_id: int, db: Session = Depends(get_db)):
    provincia = get_provincia(db, provincia_id)
    if not provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return provincia

@router.post("/", response_model=ProvinciaResponse)
def agregar_provincia(provincia: ProvinciaCreate, db: Session = Depends(get_db)):
    return create_provincia(db, provincia)

@router.put("/{provincia_id}", response_model=ProvinciaResponse)
def modificar_provincia(provincia_id: int, provincia: ProvinciaUpdate, db: Session = Depends(get_db)):
    return update_provincia(db, provincia_id, provincia)

@router.delete("/{provincia_id}")
def eliminar_provincia(provincia_id: int, db: Session = Depends(get_db)):
    delete_provincia(db, provincia_id)
    return {"message": "Provincia eliminada exitosamente"}