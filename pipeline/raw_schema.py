from pydantic import Field, HttpUrl, StrictInt
from pandantic import BaseModel
from typing import Optional

class VOASchemaRaw(BaseModel):
    id: StrictInt = Field(
        ...,
        description="Database document identifier"
    )
    ammattiala: str = Field(
        ...,
        description="Field of the job application"
    )
    tyotehtava: str = Field(
        ..., 
        description="Job title"
    )
    tyoavain: str = Field(
        ...,
        description="Job indentifier key"
    )
    osoite: str = Field(
        ...,
        description="Address location of the job"
    )
    haku_paattyy_pvm: Optional[str] = Field(
        None,
        description="Job application end date"
    )
    x: float = Field(
        ..., 
        description="X coordinate in wgs84 format"
    )
    y: float = Field(
        ..., 
        description="Y coordinate in wgs84 format"
    )
    linkki: HttpUrl = Field(
        ...,
        description="Link to the job posting"
    )
