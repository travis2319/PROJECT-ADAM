import pytest
from fastapi.testclient import TestClient
from main import app
from models.engine_health import EngineHealthModel
import pandas as pd

client = TestClient(app)

# Sample test data
sample_data = pd.DataFrame({
    "diagnostic_param": [30, 80, 45],
    "other_param": [1, 0, 1],
})

@pytest.fixture
def engine_health_model():
    return EngineHealthModel()

def test_fetch_engine_health_data():
    """
    Test the /engine-health/data endpoint.
    """
    response = client.get("/engine-health/data")
    assert response.status_code == 200
    assert "data" in response.json()

def test_engine_health_model_training(engine_health_model):
    """
    Test training the engine health model.
    """
    engine_health_model.train(sample_data)
    assert hasattr(engine_health_model, "model")
