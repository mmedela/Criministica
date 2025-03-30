from sqlalchemy.orm import Session
from DB.models.Delito import Delito
from schemas.delito_schema import DelitoCreate, DelitoUpdate

def get_delitos(db: Session):
    return db.query(Delito).all()

def get_delito_by_id(db: Session, delito_id: int):
    return db.query(Delito).filter(Delito.codigo_delito_snic_id == delito_id).first()

def create_delito(db: Session, delito_data: DelitoCreate):
    new_delito = Delito(**delito_data.dict())
    db.add(new_delito)
    db.commit()
    db.refresh(new_delito)
    return new_delito

def update_delito(db: Session, delito_id: int, delito_data: DelitoUpdate):
    delito = get_delito_by_id(db, delito_id)
    if delito:
        for key, value in delito_data.dict(exclude_unset=True).items():
            setattr(delito, key, value)
        db.commit()
        db.refresh(delito)
    return delito

def delete_delito(db: Session, delito_id: int):
    delito = get_delito_by_id(db, delito_id)
    if delito:
        db.delete(delito)
        db.commit()
    return delito
