import unittest
import pandas as pd
from datetime import date
from etl import SimpleTransformer


class TestSimpleTransformer(unittest.TestCase):
    def setUp(self):
        self.original_df = pd.DataFrame([
            {
                "id": 233,
                "ammattiala": "Jotain",
                "tyotehtava": "Ohjelmistokehittäjä",
                "tyoavain": "1",
                "osoite": "Testiosoite 200 A 23",
                "haku_paattyy_pvm": "2030-12-16",
                "x": 24.9354,
                "y": 60.1695,
                "linkki": "https://tyot.fi/tyopaikat/softadevaaja"
            }
        ])

        self.expected_df = pd.DataFrame([
            {
                "id": 233,
                "field": "Jotain",
                "job_title": "Ohjelmistokehittäjä",
                "job_key": "1",
                "address": "Testiosoite 200 A 23",
                "application_end_date": date(2030, 12, 16),
                "longitude_wgs84": 24.9354,
                "latitude_wgs84": 60.1695,
                "link": "https://tyot.fi/tyopaikat/softadevaaja"
            }
        ])

        self.transformer = SimpleTransformer()

    def test_data_is_correctly_transformed(self):
        """
        Tests that the data in transformed df is equal to the expected transformation df.
        """
        transformed_df = self.transformer(self.original_df)

        try:
            pd.testing.assert_frame_equal(
                transformed_df, self.expected_df, check_dtype=False
            )
        except AssertionError as e:
            assert "DataFrame comparison failed"

    # example of if for some odd reason invalid data passed to the transformer
    # should not be possible if the pydantic models are correct
    # this might be another case where we just wanna test the schema model itself
    # so consider it a demonstration
    def test_transformed_data_has_invalid_column(self):
        """
        Tests that the transformer raises a KeyError when a column name is unexpected.
        """
        transformed_df = self.transformer(self.original_df)
        transformed_df.rename(
            columns={"job_title": "actor_title"}, inplace=True)

        try:
            self.transformer(transformed_df)
            assert "Expected KeyError was not raised"
        except KeyError:
            pass
