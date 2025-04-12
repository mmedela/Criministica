import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from init_db import session
from models.Province import Province
from models.Crime import Crime
from models.CrimeStatistics import CrimeStatistics
from sqlalchemy.exc import IntegrityError
from config import CSV_ROUTE
import os

df = pd.read_csv(os.path.join(os.path.dirname(__file__), CSV_ROUTE), na_values=['', 'NULL'])

db_session = session()

PROVINCE_ID_COLUMN = 'provincia_id'
PROVINCE_NAME_COLUMN = 'provincia_nombre'
CRIME_CODE_SNIC_ID = 'codigo_delito_snic_id'
CRIME_CODE_SNIC_NAME = 'codigo_delito_snic_nombre'
YEAR  = 'anio'
ACT_QUANTITY  = 'cantidad_hechos'
VICTIM_QUANTITY  = 'cantidad_victimas'
MALE_VICTIMS_QUANTITY  = 'cantidad_victimas_masc'
FEMALE_VICTIMS_QUANTITY  = 'cantidad_victimas_fem'
VICTIM_QUANTITY_SD  = 'cantidad_victimas_sd'
ACT_RATE  = 'tasa_hechos'
VICTIM_RATE  = 'tasa_victimas'
MALE_VICTIMS_RATE  = 'tasa_victimas_masc'
FEMALE_VICTIMS_RATE  = 'tasa_victimas_fem'


def upsert_provinces(row):
    stmt = insert(Province).values(
        province_id=row[PROVINCE_ID_COLUMN],
        province_name=row[PROVINCE_NAME_COLUMN]
    ).on_conflict_do_nothing(index_elements=['province_id'])
    db_session.execute(stmt)

def upsert_crimes(row):
    stmt = insert(Crime).values(
        crime_code_snic_id=row[CRIME_CODE_SNIC_ID],
        crime_code_snic_name=row[CRIME_CODE_SNIC_NAME]
    ).on_conflict_do_nothing(index_elements=['crime_code_snic_id'])
    db_session.execute(stmt)

def upsert_statistics(row, province, crime):
    def to_number(val):
        return val if pd.notnull(val) else None

    stmt = insert(CrimeStatistics).values(
        province_id=province.province_id,
        crime_code_snic_id=crime.crime_code_snic_id,
        year=row[YEAR],
        act_quantity=to_number(row[ACT_QUANTITY]),
        victim_quantity=to_number(row[VICTIM_QUANTITY]),
        male_victims_quantity=to_number(row[MALE_VICTIMS_QUANTITY]),
        female_victims_quantity=to_number(row[FEMALE_VICTIMS_QUANTITY]),
        victim_quantity_sd=to_number(row[VICTIM_QUANTITY_SD]),
        act_rate=to_number(row[ACT_RATE]),
        victim_rate=to_number(row[VICTIM_RATE]),
        male_victims_rate=to_number(row[MALE_VICTIMS_RATE]),
        female_victims_rate=to_number(row[FEMALE_VICTIMS_RATE])
    ).on_conflict_do_nothing(
        index_elements=['province_id', 'crime_code_snic_id', 'year']
    )
    db_session.execute(stmt)

def cargar_datos():
    for _, row in df.iterrows():
        upsert_provinces(row)
        upsert_crimes(row)
        
        province = db_session.query(Province).get(row[PROVINCE_ID_COLUMN])
        crime = db_session.query(Crime).get(row[CRIME_CODE_SNIC_ID])
        
        upsert_statistics(row, province, crime)

    try:
        db_session.flush()  
        db_session.commit()
        print("successful commit.")
    except IntegrityError as e:
        db_session.rollback()
        print(f"Integrity error trying to insert row: {e}")
    finally:
        db_session.close()

if __name__ == "__main__":
    cargar_datos()
    
