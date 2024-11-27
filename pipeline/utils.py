from sqlalchemy import create_engine
from pipeline.models import VantaaOpenApplications
import os


def initialize_database(conn_str: str):
    try:
        engine = create_engine(conn_str)
        VantaaOpenApplications.metadata.create_all(engine)
        print(f"Table '{VantaaOpenApplications.__tablename__}' created.")
    except Exception as e:
        print(f"Creating the table failed with exception {e}")


def reset_enviroment(path: str):
    try:
        os.remove(path)
        print(f"Enviroment reseted")
    except FileNotFoundError:
        print("Nothing to do...")
    except Exception as e:
        print(f"Deleting database file failed with error {e}")
