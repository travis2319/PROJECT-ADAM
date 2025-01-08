from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chatbot_dtc_explanation():
    """
    Test the chatbot DTC explanation endpoint.
    """
    response = client.post("/chatbot/dtc-explanation", json={"dtc_code": "P0420"})
    assert response.status_code == 200
    assert "explanation" in response.json()
