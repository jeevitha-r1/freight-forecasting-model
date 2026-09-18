from pydantic import BaseModel


class VoyageRequest(BaseModel):
    vessel_id: str
    origin_id: str
    destination_id: str