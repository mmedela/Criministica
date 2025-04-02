from sqlalchemy.orm import Session
from sqlalchemy import func, case
from DB.models.EstadisticaDelito import EstadisticaDelito
from DB.models.Delito import Delito
from DB.models.Provincia import Provincia

def calcular_total_delitos(db: Session, provincia_id: int = None, anio: int = None):
    query = db.query(func.sum(EstadisticaDelito.cantidad_hechos))
    
    if provincia_id:
        query = query.filter(EstadisticaDelito.provincia_id == provincia_id)
    
    if anio:
        query = query.filter(EstadisticaDelito.anio == anio)
    
    total_delitos = query.scalar() or 0
    return total_delitos


def calcular_tasa_criminalidad(db: Session, provincia_id: int):
    resultados = (
        db.query(
           EstadisticaDelito.anio,
            func.round(
                case(
                    (Provincia.poblacion > 0, (func.sum(EstadisticaDelito.cantidad_hechos) / Provincia.poblacion) * 100000),
                    else_=0
                ), 2
            ).label("tasa_criminalidad")
        )
        .join(Provincia, Provincia.provincia_id == EstadisticaDelito.provincia_id)
        .filter(EstadisticaDelito.provincia_id == provincia_id)
        .group_by(EstadisticaDelito.anio, Provincia.poblacion)
        .all()
    )
    return {str(anio): float(tasa) for anio, tasa in resultados}


def calcular_porcentaje_delitos_provincia(db: Session, provincia_id: int):
    total_delitos_provincia = db.query(func.sum(EstadisticaDelito.cantidad_hechos)) \
                                .filter(EstadisticaDelito.provincia_id == provincia_id) \
                                .scalar() or 0

    total_delitos_nacionales = db.query(func.sum(EstadisticaDelito.cantidad_hechos)).scalar() or 0

    return (total_delitos_provincia / total_delitos_nacionales) * 100 if total_delitos_nacionales > 0 else 0