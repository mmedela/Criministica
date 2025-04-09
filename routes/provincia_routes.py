from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from DB.init_db import session
from services.province_service import (
    delete_provinces_batch_service,
    get_provinces_service,
    get_province_service,
    create_province_service,
    get_provinces_batch_service,
    update_province_service,
    delete_province_service,
    update_population_with_csv_service,
    update_provinces_batch_service
)
from schemas.province_schema import ProvinceCreate, ProvinceResponse, ProvinceUpdate
from typing import List

router = APIRouter(prefix="/provincias", tags=["Provincias"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProvinceResponse])
def listar_provincias(db: Session = Depends(get_db)):
    return get_provinces_service(db)

@router.get("/tabla_poblaciones", response_class=HTMLResponse)
def get_provincias_tabla_poblacion(db: Session = Depends(get_db)):
    print("hola")
    provincias = listar_provincias(db)
    html = ""
    for provincia in provincias:
        poblacion_formateada = f"{provincia.population:,}".replace(",", ".")
        html += f"""
        <tr>
        <td class="px-4 py-2">{provincia.province_name}</td>
        <td class="px-4 py-2">{poblacion_formateada}</td>
        </tr>
        <tr>
            <td colspan="2">
                <hr class="my-2" style="border-top: 1px solid #ddd;">
            </td>
        </tr>
        """

    if not html:
        html = """
        <tr>
            <td colspan="2" class="text-center px-4 py-2">No se encontraron provincias.</td>
        </tr>
        """

    return HTMLResponse(content=html)

@router.get("/{provincia_id}", response_model=ProvinceResponse)
def obtener_provincia(provincia_id: int, db: Session = Depends(get_db)):
    provincia = get_province_service(db, provincia_id)
    if not provincia:
        raise HTTPException(status_code=404, detail="Provincia no encontrada")
    return provincia

@router.post("/", response_model=ProvinceResponse)
def agregar_provincia(provincia: ProvinceCreate, db: Session = Depends(get_db)):
    return create_province_service(db, provincia)

@router.post("/cargar_poblacion")
async def cargar_poblacion(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    result = update_population_with_csv_service(db, content.decode("utf-8"))
    return result

@router.put("/{provincia_id}", response_model=ProvinceResponse)
def modificar_provincia(provincia_id: int, provincia: ProvinceUpdate, db: Session = Depends(get_db)):
    return update_province_service(db, provincia_id, provincia)

@router.delete("/{provincia_id}")
def eliminar_provincia(provincia_id: int, db: Session = Depends(get_db)):
    delete_province_service(db, provincia_id)
    return {"message": "Provincia eliminada exitosamente"}


@router.put("/batch", response_model=int)
def actualizar_provincias_batch(updates: List[ProvinceUpdate], db: Session = Depends(get_db)):
    updated_count = update_provinces_batch_service(db, updates)
    return updated_count

@router.delete("/batch", response_model=int)
def eliminar_provincias_batch(provincia_ids: List[int], db: Session = Depends(get_db)):
    deleted_count = delete_provinces_batch_service(db, provincia_ids)
    return deleted_count

@router.get("/batch", response_model=List[ProvinceResponse])
def obtener_provincias_batch(provincia_ids: List[int]= Query(...), db: Session = Depends(get_db)):
    provincias = get_provinces_batch_service(db, provincia_ids)
    return provincias

