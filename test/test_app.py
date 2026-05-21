import pytest

from src.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_receptor_success(client, mocker):
    mock_db = mocker.patch('src.app.collection.insert_one')
    mock_db.return_value.inserted_id = "12345"

    payload = {
        "uid": "TEST-01",
        "unixtime": 123456789,
        "temp": 25.5
    }

    response = client.post('/receptor', json=payload)
    
    assert response.status_code == 201
    assert response.get_json()["status"] == "salvo"

def test_receptor_invalid_json(client):
    response = client.post(
        '/receptor', 
        data="esto-nao-e-um-json", 
        content_type='application/json'
    )
    assert response.status_code == 400
    assert "error" in response.get_json()