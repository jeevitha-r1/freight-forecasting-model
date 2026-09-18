from pydantic import BaseModel


class Port(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    max_length: float
    max_draft: float