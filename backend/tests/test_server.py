import pytest
import json
import requests
import requests_mock
from backend.server import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_data_success(client):
    """Test successful API call to /api/data."""
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/users', json=[
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ])
        response = client.get('/api/data')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['name'] == 'John Doe'
        assert data[1]['email'] == 'jane@example.com'

def test_get_data_external_api_failure(client):
    """Test handling of external API failure."""
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/users', exc=requests.exceptions.ConnectionError("Connection error"))
        
        response = client.get('/api/data')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Connection error' in data['error']

def test_get_data_http_error(client):
    """Test handling of HTTP errors from external API."""
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/users', status_code=404, text='Not Found')
        
        response = client.get('/api/data')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data
        # Check for the essential parts of the error, not the exact string
        assert '404 Client Error' in data['error']

def test_cors_headers(client):
    """Test that CORS headers are properly set."""
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/users', json=[])
        response = client.get('/api/data')
        # CORS headers should be present due to Flask-CORS
        assert 'Access-Control-Allow-Origin' in response.headers

def test_invalid_endpoint(client):
    """Test that invalid endpoints return 404."""
    response = client.get('/api/invalid')
    assert response.status_code == 404
