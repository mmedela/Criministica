from sqlalchemy.orm import Session
from sqlalchemy import func, case
from DB.models.CrimeStatistics import CrimeStatistics
from DB.models.Crime import Crime
from DB.models.Province import Province

def calcular_total_delitos(db: Session, provincia_id: int = None, anio: int = None):
    query = db.query(func.sum(CrimeStatistics.act_quantity))
    
    if provincia_id:
        query = query.filter(CrimeStatistics.province_id == provincia_id)
    
    if anio:
        query = query.filter(CrimeStatistics.year == anio)
    
    total_delitos = query.scalar() or 0
    return total_delitos


def calcular_tasa_criminalidad(db: Session, provincia_id: int):
    resultados = (
        db.query(
           CrimeStatistics.year,
            func.round(
                case(
                    (Province.population > 0, (func.sum(CrimeStatistics.act_quantity) / Province.population) * 100000),
                    else_=0
                ), 2
            ).label("tasa_criminalidad")
        )
        .join(Province, Province.province_id == CrimeStatistics.province_id)
        .filter(CrimeStatistics.province_id == provincia_id)
        .group_by(CrimeStatistics.year, Province.population)
        .all()
    )
    return {str(anio): float(tasa) for anio, tasa in resultados}


def calcular_porcentaje_delitos_provincia(db: Session, provincia_id: int):
    total_delitos_provincia = db.query(func.sum(CrimeStatistics.act_quantity)) \
                                .filter(CrimeStatistics.province_id == provincia_id) \
                                .scalar() or 0

    total_delitos_nacionales = db.query(func.sum(CrimeStatistics.act_quantity)).scalar() or 0

    return (total_delitos_provincia / total_delitos_nacionales) * 100 if total_delitos_nacionales > 0 else 0