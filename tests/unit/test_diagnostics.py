
def test_health_check(client):
    response = client.get("/diagnostics")
    assert response.status_code == 200
    assert response.json()["message"] == "OK"
