from io import StringIO
from contextlib import redirect_stdout
from utils import initialize_database

# here we also want to use some sort of in memory database, a test db, something that is not directly associated with the
# production database
def test_initialize_database_table_creation():
    """Tests that the database table is initialized correctly"""
    conn_str = "sqlite:///:memory:"
    output = StringIO()

    with redirect_stdout(output):
        initialize_database(conn_str)

    assert "Table 'vantaa_open_applications' created." in output.getvalue(), \
            "Database table initialization failed."
