from app.settings import APP_TITLE


def test_healthcheck(client):
    response = client.get("/health")

    assert response.status_code == 200

    # Parses the body of response as JSON and returns a Python dict
    data = response.json()

    assert data["status_code"] == 200
    assert data["message"] == f"{APP_TITLE} app is up and running!"
