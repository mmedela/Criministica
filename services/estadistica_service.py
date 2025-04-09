from sqlalchemy.orm import Session
from DB.models.EstadisticaDelito import CrimeStatistics
from DB.models.Province import Province
from DB.models.Crime import Crime
from schemas.estadistica_schema import EstadisticaCreate, EstadisticaUpdate

def get_estadisticas(db: Session, provincia_id=None, delito_id=None, anio=None, limit=None, offset=0):
    query = (
        db.query(
            CrimeStatistics.id,
            CrimeStatistics.year,
            Province.province_name.label("provincia"),
            Crime.crime_code_snic_name.label("delito"),
            CrimeStatistics.act_quantity,
        )
        .join(Province, CrimeStatistics.province_id == Province.province_id)
        .join(Crime, CrimeStatistics.crime_code_snic_id == Crime.crime_code_snic_id)
    )

    if provincia_id:
        query = query.filter(CrimeStatistics.province_id  == provincia_id)
    if delito_id:
        query = query.filter(CrimeStatistics.crime_code_snic_id == delito_id)
    if anio:
        query = query.filter(CrimeStatistics.year == anio)

    return query.offset(offset).limit(limit).all()

def get_estadistica_by_id(db: Session, estadistica_id: int):
    return db.query(CrimeStatistics).filter(CrimeStatistics.id == estadistica_id).first()

def create_estadistica(db: Session, estadistica_data: EstadisticaCreate):
    new_estadistica = CrimeStatistics(**estadistica_data.dict())
    db.add(new_estadistica)
    db.commit()
    db.refresh(new_estadistica)
    return new_estadistica

def update_estadistica(db: Session, estadistica_id: int, estadistica_data: EstadisticaUpdate):
    estadistica = get_estadistica_by_id(db, estadistica_id)
    if estadistica:
        for key, value in estadistica_data.dict(exclude_unset=True).items():
            setattr(estadistica, key, value)
        db.commit()
        db.refresh(estadistica)
    return estadistica

def delete_estadistica(db: Session, estadistica_id: int):
    estadistica = get_estadistica_by_id(db, estadistica_id)
    if estadistica:
        db.delete(estadistica)
        db.commit()
    return estadistica
