from sqlalchemy.orm import Session
from DB.models.CrimeStatistics import CrimeStatistics
from DB.models.Province import Province
from DB.models.Crime import Crime
from schemas.statistics_schema import StatisticsCreate, StatisticsUpdate

def get_statistics(db: Session, province_id=None, crime_id=None, year=None, limit=None, offset=0):
    query = (
        db.query(
            CrimeStatistics.id,
            CrimeStatistics.year,
            Province.province_name.label("province"),
            Crime.crime_code_snic_name.label("crime"),
            CrimeStatistics.act_quantity,
        )
        .join(Province, CrimeStatistics.province_id == Province.province_id)
        .join(Crime, CrimeStatistics.crime_code_snic_id == Crime.crime_code_snic_id)
    )

    if province_id:
        query = query.filter(CrimeStatistics.province_id  == province_id)
    if crime_id:
        query = query.filter(CrimeStatistics.crime_code_snic_id == crime_id)
    if year:
        query = query.filter(CrimeStatistics.year == year)

    return query.offset(offset).limit(limit).all()

def get_statistic_by_id(db: Session, statistic_id: int):
    return db.query(CrimeStatistics).filter(CrimeStatistics.id == statistic_id).first()

def create_statistic(db: Session, statistic_data: StatisticsCreate):
    new_statistic = CrimeStatistics(**statistic_data.dict())
    db.add(new_statistic)
    db.commit()
    db.refresh(new_statistic)
    return new_statistic

def update_statistic(db: Session, statistic_id: int, statistic_data: StatisticsUpdate):
    statistic = get_statistic_by_id(db, statistic_id)
    if statistic:
        for key, value in statistic_data.dict(exclude_unset=True).items():
            setattr(statistic, key, value)
        db.commit()
        db.refresh(statistic)
    return statistic

def delete_statistics(db: Session, statistic_id: int):
    statistic = get_statistic_by_id(db, statistic_id)
    if statistic:
        db.delete(statistic)
        db.commit()
    return statistic
