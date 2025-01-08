import pytest
from fastapi.testclient import TestClient
from main import app
from models.emissions import EmissionsModel
import pandas as pd

client = TestClient(app)

# Sample test data
sample_data = pd.DataFrame({
    "emission_value": [50, 150, 70],
    "other_sensor": [0.5, 0.8, 0.6],
})

@pytest.fixture
def emissions_model():
    return EmissionsModel()

def test_fetch_emissions_data():
    """
    Test the /emissions/data endpoint.
    """
    response = client.get("/emissions/data")
    assert response.status_code == 200
    assert "data" in response.json()

def test_emissions_model_training(emissions_model):
    """
    Test training the emissions model.
    """
    emissions_model.train(sample_data)
    assert emissions_model.best_model is not None
