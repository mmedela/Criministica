from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from DB.init_db import session
from services.estadistica_service import (
    get_estadisticas,
    get_estadistica_by_id,
    create_estadistica,
    update_estadistica,
    delete_estadistica
)
from schemas.estadistica_schema import EstadisticaCreate, EstadisticaResponse, EstadisticaUpdate

router = APIRouter(prefix="/estadisticas-delitos", tags=["Estadísticas de Delitos"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[EstadisticaResponse])
def listar_estadisticas(
    db: Session = Depends(get_db),
    provincia_id: Optional[int] = Query(None),
    delito_id: Optional[int] = Query(None),
    anio: Optional[int] = Query(None)
):
    return get_estadisticas(db, provincia_id, delito_id, anio)

@router.get("/{estadistica_id}", response_model=EstadisticaResponse)
def obtener_estadistica(estadistica_id: int, db: Session = Depends(get_db)):
    estadistica = get_estadistica_by_id(db, estadistica_id)
    if not estadistica:
        raise HTTPException(status_code=404, detail="Estadística no encontrada")
    return estadistica

@router.post("/", response_model=EstadisticaResponse)
def agregar_estadistica(estadistica: EstadisticaCreate, db: Session = Depends(get_db)):
    return create_estadistica(db, estadistica)

@router.put("/{estadistica_id}", response_model=EstadisticaResponse)
def modificar_estadistica(estadistica_id: int, estadistica: EstadisticaUpdate, db: Session = Depends(get_db)):
    return update_estadistica(db, estadistica_id, estadistica)

@router.delete("/{estadistica_id}")
def eliminar_estadistica(estadistica_id: int, db: Session = Depends(get_db)):
    delete_estadistica(db, estadistica_id)
    return {"message": "Estadística eliminada exitosamente"}