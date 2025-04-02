from typing import List
from sqlalchemy.orm import Session
from DB.models.Delito import Delito
from schemas.delito_schema import DelitoCreate, DelitoUpdate

def get_all_delitos_service(db: Session):
    return db.query(Delito).all()

def get_delito_by_id_service(db: Session, delito_id: int):
    return db.query(Delito).filter(Delito.codigo_delito_snic_id == delito_id).first()

def create_delito_service(db: Session, delito_data: DelitoCreate):
    new_delito = Delito(**delito_data.dict())
    db.add(new_delito)
    db.commit()
    db.refresh(new_delito)
    return new_delito

def update_delito_service(db: Session, delito_id: int, delito_data: DelitoUpdate):
    delito = get_delito_by_id_service(db, delito_id)
    if delito:
        for key, value in delito_data.dict(exclude_unset=True).items():
            setattr(delito, key, value)
        db.commit()
        db.refresh(delito)
    return delito

def delete_delito_service(db: Session, delito_id: int):
    delito = get_delito_by_id_service(db, delito_id)
    if delito:
        db.delete(delito)
        db.commit()
    return delito

def create_delitos_service(db: Session, delitos: List[DelitoCreate]):
        try:
            db.bulk_insert_mappings(Delito, [d.dict() for d in delitos])
            db.commit()
            return len(delitos)
        except Exception:
            db.rollback()
            return -1
                    
def update_delitos_service(db: Session, updates: List[DelitoUpdate]):
    try:
        db.bulk_update_mappings(Delito, [u.dict() for u in updates])
        db.commit()
        return len(updates)
    except Exception:
        db.rollback()
        return -1
    
def delete_delitos_service(db: Session, delito_ids: List[int]):
    try:
        stmt = db.delete(Delito).where(Delito.codigo_delito_snic_id.in_(delito_ids))
        result = db.execute(stmt)
        db.commit()
        return result.rowcount
    except Exception:
        db.rollback()
        return -1

def get_batch_delitos_service(db: Session, delito_ids: List[int]):
    return db.query(Delito).filter(Delito.codigo_delito_snic_id.in_(delito_ids)).all()
    