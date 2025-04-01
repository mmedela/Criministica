from sqlalchemy.orm import Session
from DB.models.Provincia import Provincia
from schemas.provincia_schema import ProvinciaCreate, ProvinciaUpdate
from sqlalchemy.exc import IntegrityError
import csv
from io import StringIO

def get_provincias(db: Session):
    return db.query(Provincia).all()

def get_provincia(db: Session, provincia_id: int):
    return db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()

def create_provincia(db: Session, provincia: ProvinciaCreate):
    new_provincia = Provincia(
        provincia_id=provincia.provincia_id, 
        poblacion=provincia.poblacion,  
        provincia_nombre=provincia.provincia_nombre
    )
    db.add(new_provincia)
    try:
        db.commit()
        db.refresh(new_provincia)
        return new_provincia
    except IntegrityError:
        db.rollback()
        return None

def update_provincia(db: Session, provincia_id: int, provincia_data: ProvinciaUpdate):
    provincia = db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()
    if not provincia:
        return None
    
    provincia.provincia_nombre = provincia_data.provincia_nombre
    
    if provincia_data.poblacion is not None:
        provincia.poblacion = provincia_data.poblacion
    
    db.commit()
    db.refresh(provincia)
    return provincia

def delete_provincia(db: Session, provincia_id: int):
    provincia = db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()
    if not provincia:
        return None
    db.delete(provincia)
    db.commit()
    return provincia

def actualizar_poblacion_desde_csv(db: Session, file_content: str):
    reader = csv.reader(StringIO(file_content))
    next(reader, None)  # Saltar encabezado si existe

    actualizadas = 0
    for row in reader:
        if len(row) < 2:
            continue
        try:
            provincia_id = int(row[0])
            poblacion = int(row[1])
        except ValueError:
            print(int(row(0)))
            print(int(row(1)))
            continue  # Ignorar filas con datos inválidos

        provincia = db.query(Provincia).filter(Provincia.provincia_id == provincia_id).first()
        if provincia:
            provincia.poblacion = poblacion
            actualizadas += 1

    db.commit()
    return {"message": f"Población actualizada para {actualizadas} provincias"}