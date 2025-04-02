from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
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
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/estadisticas-delitos", tags=["Estadísticas de Delitos"])

templates = Jinja2Templates(directory="templates")


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
    estadisticas = get_estadisticas(db, provincia_id, delito_id, anio)
    return [EstadisticaResponse.model_validate(e, from_attributes=True) for e in estadisticas]


@router.get("/more", response_class=HTMLResponse)
def cargar_estadisticas_parciales(
    request: Request,
    db: Session = Depends(get_db),
    offset: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100)
):
    estadisticas = get_estadisticas(db, limit=limit, offset=offset)  
    if not estadisticas:
        raise HTTPException(status_code=404, detail="No se encontraron más estadísticas.")
    return templates.TemplateResponse(
        "estadisticas_partial.html", 
        {"request": request, "estadisticas": estadisticas, "next_page": offset + limit}
    )

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
