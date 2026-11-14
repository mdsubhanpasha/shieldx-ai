import pytest
from starlette.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'

def test_verify_threat_safe():
    response = client.post('/api/v1/verify-threat', json={'text': 'Hello, how are you doing today?'})
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'SAFE'

def test_verify_threat_flagged():
    response = client.post('/api/v1/verify-threat', json={'text': 'CBI officer arrest warrant account freeze transfer money'})
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'FLAGGED'
    assert data['risk_score'] > 0.9

def test_verify_upi_blacklisted():
    response = client.post('/api/v1/verify-upi', json={'vpa': 'scammer@okaxis', 'amount': 1000, 'mcc': '5411'})
    assert response.status_code == 200
    data = response.json()
    assert data['safe'] == False
