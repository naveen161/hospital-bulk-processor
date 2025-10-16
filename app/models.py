from pydantic import BaseModel

class HospitalResult(BaseModel):
    row: int
    hospital_id: int
    name: str
    status: str
