import unittest
import pandas as pd
from unittest.mock import patch
from pandas.testing import assert_frame_equal
from etl import SimpleExtractor
from requests.exceptions import HTTPError

class TestSimpleExtractor(unittest.TestCase):
    def setUp(self):
        self.test_data = [
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
        ]

    @patch.object(SimpleExtractor, "fetch_data")
    def test_data_passes_the_extractor_if_it_is_in_correct_format(
            self, mock_fetch_data):
        """
        Tests that the data passes the SimpleExtractor in correct format when it is valid.
        """
        mock_fetch_data.return_value = MockResponse(self.test_data, 200)
        df = SimpleExtractor()()
        assert_frame_equal(df, pd.DataFrame(self.test_data), check_dtype=False)

    @patch.object(SimpleExtractor, "fetch_data")
    def test_invalid_response_code_from_server(self, mock_fetch_data):
        """
        Tests that SimpleExtractor raises an HTTPError for a response that does not return 200.
        """
        mock_fetch_data.return_value = MockResponse(self.test_data, 404)

        try:
            SimpleExtractor()()
            assert "Expected HTTPError was not raised"
        except HTTPError:
            pass

    # ... these might be a bit silly with pydantic, but at least it demonstrates that the exceptions are raised as expected
    # also it could be a good idea to instead test the schemas (models) itself to make sure that they are behaving as expected
    @patch.object(SimpleExtractor, "fetch_data")
    def test_data_does_not_pass_the_extractor_with_an_invalid_field(
            self, mock_fetch_data):
        """
        Tests that a ValueError is raised when an invalid field value is present in the data.
        """
        self.test_data[0]["id"] = "this is not an id"
        mock_fetch_data.return_value = MockResponse(self.test_data, 200)

        try:
            SimpleExtractor()()
            assert "Expected ValueError was not raised"
        except ValueError:
            pass

    @patch.object(SimpleExtractor, "fetch_data")
    def test_data_does_not_pass_the_extractor_with_a_missing_field(
            self, mock_fetch_data):
        """
        Tests that a ValueError is raised when a required field is missing.
        """
        self.test_data[0].pop("id", None)
        mock_fetch_data.return_value = MockResponse(self.test_data, 200)

        try:
            SimpleExtractor()()
            assert "Expected ValueError was not raised"
        except ValueError:
            pass

# this class mocks the returned response object since we never want to call the actual api while testing
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise HTTPError(f"HTTP Error: {self.status_code}")
