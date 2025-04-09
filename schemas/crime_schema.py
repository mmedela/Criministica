from pydantic import BaseModel

class CrimeBase(BaseModel):
    crime_code_snic_name: str

class CrimeCreate(CrimeBase):
    pass

class CrimeUpdate(CrimeBase):
    pass

class CrimeResponse(CrimeBase):
    crime_code_snic_id: int
    
    class Config:
        from_attributes = True
