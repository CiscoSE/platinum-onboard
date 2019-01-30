import pytest
from flask import Flask


@pytest.fixture(scope="session")
def temp_database(tmpdir_factory):
    """ Initalize the Database """
    tmpdb = str(tmpdir_factory.mktemp('temp'))+"/testdb.sqlite"
    return tmpdb


