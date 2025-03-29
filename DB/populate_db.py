import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from models.Base import session
from models.Provincia import Provincia
from models.Delito import Delito
from models.EstadisticaDelito import EstadisticaDelito
from sqlalchemy.exc import IntegrityError
from config import CSV_ROUTE

df = pd.read_csv(CSV_ROUTE, na_values=['', 'NULL'])

db_session = session()

def upsert_provincia(row):
    stmt = insert(Provincia).values(
        provincia_id=row['provincia_id'],
        provincia_nombre=row['provincia_nombre']
    ).on_conflict_do_nothing(index_elements=['provincia_id'])
    db_session.execute(stmt)

def upsert_delito(row):
    stmt = insert(Delito).values(
        codigo_delito_snic_id=row['codigo_delito_snic_id'],
        codigo_delito_snic_nombre=row['codigo_delito_snic_nombre']
    ).on_conflict_do_nothing(index_elements=['codigo_delito_snic_id'])
    db_session.execute(stmt)

def upsert_estadistica(row, provincia, delito):
    def to_number(val):
        return val if pd.notnull(val) else None

    stmt = insert(EstadisticaDelito).values(
        provincia_id=provincia.provincia_id,
        codigo_delito_snic_id=delito.codigo_delito_snic_id,
        anio=row['anio'],
        cantidad_hechos=to_number(row['cantidad_hechos']),
        cantidad_victimas=to_number(row['cantidad_victimas']),
        cantidad_victimas_masc=to_number(row['cantidad_victimas_masc']),
        cantidad_victimas_fem=to_number(row['cantidad_victimas_fem']),
        cantidad_victimas_sd=to_number(row['cantidad_victimas_sd']),
        tasa_hechos=to_number(row['tasa_hechos']),
        tasa_victimas=to_number(row['tasa_victimas']),
        tasa_victimas_masc=to_number(row['tasa_victimas_masc']),
        tasa_victimas_fem=to_number(row['tasa_victimas_fem'])
    ).on_conflict_do_nothing(
        index_elements=['provincia_id', 'codigo_delito_snic_id', 'anio']
    )
    db_session.execute(stmt)

def cargar_datos():
    for _, row in df.iterrows():
        upsert_provincia(row)
        upsert_delito(row)
        
        provincia = db_session.query(Provincia).get(row['provincia_id'])
        delito = db_session.query(Delito).get(row['codigo_delito_snic_id'])
        
        upsert_estadistica(row, provincia, delito)

    try:
        db_session.flush()  
        db_session.commit()
        print("Commit exitoso.")
    except IntegrityError as e:
        db_session.rollback()
        print(f"Error de integridad al agregar datos: {e}")
    finally:
        db_session.close()

if __name__ == "__main__":
    cargar_datos()
    
