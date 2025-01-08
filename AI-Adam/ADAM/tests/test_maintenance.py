import pytest
from fastapi.testclient import TestClient
from main import app
from models.maintenance import MaintenanceModel
import pandas as pd

client = TestClient(app)

# Sample test data
sample_data = pd.DataFrame({
    "wear_and_tear": [50, 80, 90],
    "other_param": [0.2, 0.6, 0.9],
})

@pytest.fixture
def maintenance_model():
    return MaintenanceModel()

def test_fetch_maintenance_data():
    """
    Test the /maintenance/data endpoint.
    """
    response = client.get("/maintenance/data")
    assert response.status_code == 200
    assert "data" in response.json()

def test_maintenance_model_training(maintenance_model):
    """
    Test training the maintenance model.
    """
    maintenance_model.train(sample_data)
    assert hasattr(maintenance_model, "model")
