import argparse
import os
from pipeline import initialize_database, run_etl, reset_enviroment
from typing import Literal

DB_FOLDER = "db"
DB_PATH = f"{DB_FOLDER}/applications.db"

class PipelineArguments(argparse.Namespace):
    method: Literal["init", "reset", "etl"]


def main():
    # Check Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", type=str, default="etl", help="Method argument")
    args: PipelineArguments = parser.parse_args()
    conn_str = f"sqlite:///{DB_PATH}"

    # Run method
    match args.method:
        case "init":
            # Create Folder for database if it does not exist
            if not os.path.exists(DB_FOLDER):
                os.makedirs(DB_FOLDER)
            initialize_database(conn_str=conn_str)
        case "reset":
            reset_enviroment(path=DB_PATH)
        case "etl":
            run_etl(conn_str=conn_str)
        case _other:
            raise Exception(f"Method {_other} not recognized.")


if __name__ == "__main__":
    main()
