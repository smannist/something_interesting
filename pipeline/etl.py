import pandas as pd
import requests
from sqlalchemy import create_engine, orm
from datetime import date

from pipeline.const import API_URL
from pipeline.models import VantaaOpenApplications
from pipeline.raw_schema import VOASchemaRaw
from pipeline.transform_schema import VOASchemaTransform


class SimpleExtractor:
    def __init__(self):
        self.api_url = API_URL

    def fetch_data(self):
        return requests.get(
            url=self.api_url,
            headers={"Content-Type": "application/json"},
        )

    def extract(self) -> pd.DataFrame:
        response = self.fetch_data()
        response.raise_for_status()
        # with pandantic the schemas (models) have extra functionality parse_df which can be used for easy validation
        return VOASchemaRaw.parse_df(
            dataframe=pd.DataFrame(response.json()),
            errors="raise"
        )

    def __call__(self) -> pd.DataFrame:
        return self.extract()


class SimpleTransformer:
    def __init__(self):
        self.rename_schema = {
            "id": "id",
            "ammattiala": "field",
            "tyotehtava": "job_title",
            "tyoavain": "job_key",
            "osoite": "address",
            "haku_paattyy_pvm": "application_end_date",
            "x": "longitude_wgs84",
            "y": "latitude_wgs84",
            "linkki": "link",
        }

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        # Rename based on the defined schema and drop irrelevant fields
        return df.rename(columns=self.rename_schema)[self.rename_schema.values()]

    def _transform_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        # Transfrom dates from strings to date objects
        df["application_end_date"] = df["application_end_date"].apply(
            lambda datestr: date.fromisoformat(datestr) if pd.notna(datestr) else None
        )
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return VOASchemaTransform.parse_df(
            dataframe=df.pipe(self._rename_columns).pipe(self._transform_dates),
            errors="raise"
        )

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.transform(df=df)


class SimpleLoader:
    def __init__(self, conn_str: str):
        # Setup Engine
        self.engine = create_engine(conn_str)

    def load(self, df: pd.DataFrame) -> pd.DataFrame:
        # Load data into database inside session
        session = orm.sessionmaker(bind=self.engine)
        with session() as sess:
            sess.bulk_save_objects(
                [VantaaOpenApplications(**row) for row in df.to_dict(orient="records")]
            )
            sess.commit()

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        self.load(df=df)


def run_etl(conn_str: str):
    # Initialise ETL parts
    extractor = SimpleExtractor()
    transformer = SimpleTransformer()
    loader = SimpleLoader(conn_str=conn_str)

    # Run parts
    df = extractor()
    df = transformer(df=df)
    loader(df=df)

    print("Data loaded to database succesfully")
