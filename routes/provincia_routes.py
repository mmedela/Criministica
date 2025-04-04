from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from DB.init_db import session
from services.provincia_service import (
    delete_provincias_batch,
    get_provincias,
    get_provincia,
    create_provincia,
    get_provincias_batch,
    update_provincia,
    delete_provincia,
    actualizar_poblacion_desde_csv,
    update_provincias_batch
)
from schemas.provincia_schema import ProvinciaCreate, ProvinciaResponse, ProvinciaUpdate
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

@router.post("/cargar_poblacion")
async def cargar_poblacion(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    result = actualizar_poblacion_desde_csv(db, content.decode("utf-8"))
    return result

@router.put("/{provincia_id}", response_model=ProvinciaResponse)
def modificar_provincia(provincia_id: int, provincia: ProvinciaUpdate, db: Session = Depends(get_db)):
    return update_provincia(db, provincia_id, provincia)

@router.delete("/{provincia_id}")
def eliminar_provincia(provincia_id: int, db: Session = Depends(get_db)):
    delete_provincia(db, provincia_id)
    return {"message": "Provincia eliminada exitosamente"}


@router.put("/batch", response_model=int)
def actualizar_provincias_batch(updates: List[ProvinciaUpdate], db: Session = Depends(get_db)):
    updated_count = update_provincias_batch(db, updates)
    return updated_count

@router.delete("/batch", response_model=int)
def eliminar_provincias_batch(provincia_ids: List[int], db: Session = Depends(get_db)):
    deleted_count = delete_provincias_batch(db, provincia_ids)
    return deleted_count

@router.get("/batch", response_model=List[ProvinciaResponse])
def obtener_provincias_batch(provincia_ids: List[int]= Query(...), db: Session = Depends(get_db)):
    provincias = get_provincias_batch(db, provincia_ids)
    return provincias