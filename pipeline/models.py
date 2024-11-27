from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

from pipeline.const import TABLE_NAME 

# Define the base model class
Base = declarative_base()


# Define the model
class VantaaOpenApplications(Base):
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    field = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    job_key = Column(String, nullable=False)
    address = Column(String, nullable=False)
    longitude_wgs84 = Column(Float, nullable=False)
    latitude_wgs84 = Column(Float, nullable=False)
    application_end_date = Column(Date, nullable=True)
    link = Column(String, nullable=False)
