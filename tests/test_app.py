import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Welcome to the CI Practice Flask App!"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_greet(client):
    response = client.get("/api/greet/Alice")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Hello, Alice!"


def test_greet_empty_name(client):
    response = client.get("/api/greet/%20")
    assert response.status_code == 400


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 2, 3, 5),
        ("subtract", 5, 3, 2),
        ("multiply", 4, 3, 12),
        ("divide", 10, 2, 5),
    ],
)
def test_calculate(client, operation, a, b, expected):
    response = client.post(
        "/api/calculate", json={"operation": operation, "a": a, "b": b}
    )
    assert response.status_code == 200
    assert response.get_json()["result"] == expected


def test_calculate_divide_by_zero(client):
    response = client.post(
        "/api/calculate", json={"operation": "divide", "a": 10, "b": 0}
    )
    assert response.status_code == 400


def test_calculate_invalid_operation(client):
    response = client.post(
        "/api/calculate", json={"operation": "power", "a": 2, "b": 3}
    )
    assert response.status_code == 400


def test_calculate_missing_fields(client):
    response = client.post("/api/calculate", json={"operation": "add"})
    assert response.status_code == 400
