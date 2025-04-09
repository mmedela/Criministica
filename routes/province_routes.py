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

router = APIRouter(prefix="/provinces", tags=["Provinces"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProvinceResponse])
def list_provinces(db: Session = Depends(get_db)):
    return get_provinces_service(db)

@router.get("/population_table", response_class=HTMLResponse)
def get_provinces_population_table(db: Session = Depends(get_db)):
    provinces = list_provinces(db)
    table_html = ""
    for province in provinces:
        formated_population = f"{province.population:,}".replace(",", ".")
        table_html += f"""
        <tr>
        <td class="px-4 py-2">{province.province_name}</td>
        <td class="px-4 py-2">{formated_population}</td>
        </tr>
        <tr>
            <td colspan="2">
                <hr class="my-2" style="border-top: 1px solid #ddd;">
            </td>
        </tr>
        """

    if not table_html:
        table_html = """
        <tr>
            <td colspan="2" class="text-center px-4 py-2">No se encontraron provincias.</td>
        </tr>
        """

    return HTMLResponse(content=table_html)

@router.post("/", response_model=ProvinceResponse)
def add_province(province: ProvinceCreate, db: Session = Depends(get_db)):
    return create_province_service(db, province)


@router.post("/upload_population")
async def upload_population(file: UploadFile = File(...), db: Session = Depends(get_db)):
    population_file = await file.read()
    return update_population_with_csv_service(db, population_file.decode("utf-8"))

@router.put("/batch", response_model=int)
def update_provinces_batch(updates: List[ProvinceUpdate], db: Session = Depends(get_db)):
    return update_provinces_batch_service(db, updates)

@router.delete("/batch", response_model=int)
def delete_provinces_batch(provinces_ids: List[int], db: Session = Depends(get_db)):
    return delete_provinces_batch_service(db, provinces_ids)

@router.get("/batch", response_model=List[ProvinceResponse])
def get_provinces_batch(provinces_ids: List[int]= Query(...), db: Session = Depends(get_db)):
    return get_provinces_batch_service(db, provinces_ids)

@router.get("/{province_id}", response_model=ProvinceResponse)
def get_province(province_id: int, db: Session = Depends(get_db)):
    province = get_province_service(db, province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Provinces not found")
    return province

@router.put("/{province_id}", response_model=ProvinceResponse)
def modificar_provincia(province_id: int, province: ProvinceUpdate, db: Session = Depends(get_db)):
    return update_province_service(db, province_id, province)

@router.delete("/{province_id}")
def eliminar_provincia(province_id: int, db: Session = Depends(get_db)):
    delete_province_service(db, province_id)
    return {"message": "Province deleted successfully"}




