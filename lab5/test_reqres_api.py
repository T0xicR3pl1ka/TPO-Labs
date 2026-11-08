import pytest
import requests

BASE_URL = "https://reqres.in/api"

@pytest.fixture(scope="session")
def api():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()

# --- GET /users/2 (позитивный) ---
class TestGetUser:
    def test_status_code(self, api):
        assert api.get(f"{BASE_URL}/users/2").status_code == 200

    def test_user_id_is_2(self, api):
        assert api.get(f"{BASE_URL}/users/2").json()["data"]["id"] == 2

    def test_email_contains_janet(self, api):
        email = api.get(f"{BASE_URL}/users/2").json()["data"]["email"]
        assert "janet" in email.lower()

# --- GET /users/23 (негативный) ---
class TestGetUserNotFound:
    def test_status_code_is_404(self, api):
        assert api.get(f"{BASE_URL}/users/23").status_code == 404

# --- POST /users (создание) ---
class TestCreateUser:
    payload = {"name": "morpheus", "job": "leader"}

    def test_status_code_is_201(self, api):
        response = api.post(f"{BASE_URL}/users", json=self.payload)
        assert response.status_code == 201

    def test_response_contains_name_and_job(self, api):
        response = api.post(f"{BASE_URL}/users", json=self.payload)
        body = response.json()
        assert body["name"] == "morpheus"
        assert body["job"] == "leader"

# --- PUT /users/2 (обновление) ---
class TestUpdateUser:
    payload = {"name": "morpheus", "job": "zion resident"}

    def test_status_code_is_200(self, api):
        response = api.put(f"{BASE_URL}/users/2", json=self.payload)
        assert response.status_code == 200

    def test_job_is_updated(self, api):
        response = api.put(f"{BASE_URL}/users/2", json=self.payload)
        assert response.json()["job"] == "zion resident"