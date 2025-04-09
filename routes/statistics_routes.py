from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from DB.init_db import session
from services.statistic_service import (
    get_statistics,
    get_statistic_by_id,
    create_statistic,
    update_statistic,
    delete_statistics
)
from services.province_service import get_provinces_service
from services.crimes_service import get_all_crimes_service
from schemas.statistics_schema import StatisticsCreate, StatisticsResponse, StatisticsUpdate
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/crimes-statistics", tags=["Crime statistics"])

templates = Jinja2Templates(directory="templates")


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[StatisticsResponse])
def list_Statistics(
    db: Session = Depends(get_db),
    province_id: Optional[int] = Query(None),
    crime_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None)
):
    statistics = get_statistics(db, province_id, crime_id, year)
    return [StatisticsResponse.model_validate(e, from_attributes=True) for e in statistics]


@router.get("/more", response_class=HTMLResponse)
def load_paginated_statistics(
    request: Request,
    db: Session = Depends(get_db),
    offset: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100),
    province_id: Optional[str] = Query(None),
    crime_id: Optional[str] = Query(None),
    year: Optional[str] = Query(None)          
):
    try:
        province_id = int(province_id) if province_id not in (None, "") else None
    except ValueError:
        province_id = None

    try:
        crime_id = int(crime_id) if crime_id not in (None, "") else None
    except ValueError:
        crime_id = None

    try:
        year = int(year) if year not in (None, "") else None
    except ValueError:
        year = None

    statistics = get_statistics(
        db,
        province_id=province_id, 
        crime_id=crime_id,       
        year=year,                 
        limit=limit, 
        offset=offset
    )
    provinces = get_provinces_service(db)
    crimes = get_all_crimes_service(db)
    
    if not statistics:
        raise HTTPException(status_code=404, detail="No statistics found.")
    return templates.TemplateResponse(
        "partial_statistics.html",
        {
            "request": request,
            "statistics": statistics,
            "next_page": offset + limit,
            "provinces": provinces,
            "crimes": crimes,
            "selected_province": province_id,
            "selected_crime": crime_id,
            "selected_year": year
        }
    )

@router.post("/", response_model=StatisticsResponse)
def create_statistic(statistic: StatisticsCreate, db: Session = Depends(get_db)):
    return create_statistic(db, statistic)

@router.get("/{statistic_id}", response_model=StatisticsResponse)
def get_statistic(statistic_id: int, db: Session = Depends(get_db)):
    statistic = get_statistic_by_id(db, statistic_id)
    if not statistic:
        raise HTTPException(status_code=404, detail="Statistic not found")
    return statistic

@router.put("/{statistic_id}", response_model=StatisticsResponse)
def modify_statistic(statistic_id: int, statistic: StatisticsUpdate, db: Session = Depends(get_db)):
    return update_statistic(db, statistic_id, statistic)

@router.delete("/{statistic_id}")
def delete_statistic(statistic_id: int, db: Session = Depends(get_db)):
    delete_statistics(db, statistic_id)
    return {"message": "Statistic not found"}
