import pytest
from app.main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['message'] == 'URL Shortener API is running'

def test_shorten_url_success(client):
    url_data = {'url': 'https://example.com'}
    response = client.post('/shorten', json=url_data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_url' in data
    assert data['original_url'] == 'https://example.com'

def test_shorten_url_invalid(client):
    url_data = {'url': 'invalid-url'}
    response = client.post('/shorten', json=url_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_redirect_and_stats(client):
    # Step 1: Shorten URL
    url_data = {'url': 'https://google.com'}
    shorten_res = client.post('/shorten', json=url_data)
    assert shorten_res.status_code == 201
    short_url = shorten_res.get_json()['short_url']
    short_code = short_url.rsplit('/', 1)[-1]

    # Step 2: Redirect
    redirect_res = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers['Location'] == 'https://google.com'

    # Step 3: Stats check
    stats_res = client.get(f'/{short_code}/stats')
    assert stats_res.status_code == 200
    stats_data = stats_res.get_json()
    assert stats_data['original_url'] == 'https://google.com'
    assert stats_data['clicks'] == 1
