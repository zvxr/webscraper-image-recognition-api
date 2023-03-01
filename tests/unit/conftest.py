from fastapi.testclient import TestClient
import pytest

from app.main import app


#@pytest.fixture(autouse=True)
#def set_unittest_config(monkeypatch):
#    """
#    This is to prevent hitting any resources we do not want to, namely DoseSpot API.
#    """
#    monkeypatch.setenv("ENVIRONMENT", "unittest")
#    get_config(reload=True)


@pytest.fixture()
def client():
    return TestClient(app)
