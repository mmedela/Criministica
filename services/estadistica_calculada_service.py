from sqlalchemy.orm import Session
from sqlalchemy import func
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
    total_delitos = db.query(func.sum(EstadisticaDelito.cantidad_hechos)) \
                      .filter(EstadisticaDelito.provincia_id == provincia_id) \
                      .scalar() or 0
    
    provincia = db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()
    poblacion = provincia.poblacion if provincia else 0

    return (total_delitos / poblacion) * 100000 if poblacion > 0 else 0


def calcular_porcentaje_delitos_provincia(db: Session, provincia_id: int):
    total_delitos_provincia = db.query(func.sum(EstadisticaDelito.cantidad_hechos)) \
                                .filter(EstadisticaDelito.provincia_id == provincia_id) \
                                .scalar() or 0

    total_delitos_nacionales = db.query(func.sum(EstadisticaDelito.cantidad_hechos)).scalar() or 0

    return (total_delitos_provincia / total_delitos_nacionales) * 100 if total_delitos_nacionales > 0 else 0