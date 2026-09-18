from pydantic import BaseModel


class Vessel(BaseModel):
    id: str
    name: str
    vessel_type: str
    length: float
    draft: float
    capacity: float
    speed: float
    fuel_consumption: float