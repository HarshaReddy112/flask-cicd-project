
from app import app

def test_home_route():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.data.decode() == "Welcome to Flask CI/CD Pipeline!"
