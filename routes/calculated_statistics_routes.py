from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from DB.init_db import session
from services.calculated_statistics_service import (
    calculate_total_crimes,
    calculate_crime_rate,
    calculate_crime_percentage_per_province
)
from typing import Dict

router = APIRouter(prefix="/calculated-crime-statistics", tags=["Calculated crime statistics"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/total", response_model=Dict[str, int])
def get_total_crimes(
    province_id: int = Query(None, description="Province ID"),
    year: int = Query(None, description="Year to filter"),
    db: Session = Depends(get_db)
):
    if province_id is not None and province_id <= 0:
        raise HTTPException(status_code=400, detail="The province ID must be a positive number.")
    if year is not None and (year < 1900 or year > 2100):
        raise HTTPException(status_code=400, detail="The year must be in a valid range (2000-2024).")

    return {"total_crimes": calculate_total_crimes(db, province_id, year)}

@router.get("/crime-rate/{province_id}", response_model=Dict[str, Dict[str, float]])
def get_crime_rate(
    province_id: int,
    db: Session = Depends(get_db)
):
    if province_id <= 0:
        raise HTTPException(status_code=400, detail="The province ID must be a positive number.")

    rate = calculate_crime_rate(db, province_id)
    if rate is None:
        raise HTTPException(status_code=404, detail="No data found for the specified province.")
    return {"crime_rate": rate}

@router.get("/percentage/{province_id}", response_model=Dict[str, float])
def get_crime_percentage_per_province(
    province_id: int,
    db: Session = Depends(get_db)
):
    if province_id <= 0:
        raise HTTPException(status_code=400, detail="The province ID must be a positive number.")

    percentage = calculate_crime_percentage_per_province(db, province_id)
    if percentage is None:
        raise HTTPException(status_code=404, detail="No data found for the specified province.")

    return {"crime_percentage": percentage}