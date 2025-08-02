import pytest
import json
from unittest.mock import patch, Mock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_data_success(client):
    """Test successful API call to /api/data."""
    # Mock the external API response
    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ]
    mock_response.raise_for_status.return_value = None
    
    with patch('backend.server.requests.get', return_value=mock_response):
        response = client.get('/api/data')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['name'] == 'John Doe'
        assert data[1]['email'] == 'jane@example.com'

def test_get_data_external_api_failure(client):
    """Test handling of external API failure."""
    with patch('backend.server.requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection error")
        
        response = client.get('/api/data')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Connection error' in data['error']

def test_get_data_http_error(client):
    """Test handling of HTTP errors from external API."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("404 Not Found")
    
    with patch('backend.server.requests.get', return_value=mock_response):
        response = client.get('/api/data')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

def test_cors_headers(client):
    """Test that CORS headers are properly set."""
    response = client.get('/api/data')
    # CORS headers should be present due to Flask-CORS
    assert 'Access-Control-Allow-Origin' in response.headers

def test_invalid_endpoint(client):
    """Test that invalid endpoints return 404."""
    response = client.get('/api/invalid')
    assert response.status_code == 404
