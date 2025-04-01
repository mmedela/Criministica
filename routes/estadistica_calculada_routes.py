from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from DB.init_db import session
from services.estadistica_calculada_service import (
    calcular_total_delitos,
    calcular_tasa_criminalidad,
    calcular_porcentaje_delitos_provincia
)
from typing import Dict

router = APIRouter(prefix="/estadisticas-calculadas-delitos", tags=["Estadísticas Calculadas Delitos"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/total", response_model=Dict[str, int])
def obtener_total_delitos(
    provincia_id: int = Query(None, description="ID de la provincia"),
    anio: int = Query(None, description="Año a filtrar"),
    db: Session = Depends(get_db)
):
    if provincia_id is not None and provincia_id <= 0:
        raise HTTPException(status_code=400, detail="El ID de la provincia debe ser un número positivo.")
    if anio is not None and (anio < 1900 or anio > 2100):
        raise HTTPException(status_code=400, detail="El año debe estar en un rango válido (1900-2100).")

    total = calcular_total_delitos(db, provincia_id, anio)
    return {"total_delitos": total}

@router.get("/tasa-criminalidad/{provincia_id}", response_model=Dict[str, float])
def obtener_tasa_criminalidad(
    provincia_id: int,
    db: Session = Depends(get_db)
):
    if provincia_id <= 0:
        raise HTTPException(status_code=400, detail="El ID de la provincia debe ser un número positivo.")

    tasa = calcular_tasa_criminalidad(db, provincia_id)
    if tasa is None:
        raise HTTPException(status_code=404, detail="No se encontraron datos para la provincia especificada.")

    return {"tasa_criminalidad": tasa}

@router.get("/porcentaje/{provincia_id}", response_model=Dict[str, float])
def obtener_porcentaje_delitos_provincia(
    provincia_id: int,
    db: Session = Depends(get_db)
):
    if provincia_id <= 0:
        raise HTTPException(status_code=400, detail="El ID de la provincia debe ser un número positivo.")

    porcentaje = calcular_porcentaje_delitos_provincia(db, provincia_id)
    if porcentaje is None:
        raise HTTPException(status_code=404, detail="No se encontraron datos para la provincia especificada.")

    return {"porcentaje_delitos": porcentaje}