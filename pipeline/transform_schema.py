from pydantic import Field, HttpUrl, StrictInt
from pandantic import BaseModel
from typing import Optional
from datetime import date

class VOASchemaTransform(BaseModel):
    id: StrictInt = Field(
        ...,
        description="Database document identifier"
    )
    field: str = Field(
        ...,
        description="Field of the job application"
    )
    job_title: str = Field(
        ..., 
        description="Job title"
    )
    job_key: str = Field(
        ...,
        description="Job indentifier key"
    )
    application_end_date: str = Field(
        ...,
        description="Address location of the job"
    )
    application_end_date: Optional[date] = Field(
        None,
        description="Job application end date"
    )
    longitude_wgs84: float = Field(
        ..., 
        description="X coordinate in wgs84 format"
    )
    latitude_wgs84: float = Field(
        ..., 
        description="Y coordinate in wgs84 format"
    )
    link: HttpUrl = Field(
        ...,
        description="Link to the job posting"
    )
