import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from app.web import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.delenv("APP_API_KEY", raising=False)
    return create_app().test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_lists_operations(client):
    body = client.get("/").get_json()
    assert body["operations"] == ["add", "divide", "multiply", "subtract"]


def test_add_over_http(client):
    body = client.get("/calc/add?a=10&b=5").get_json()
    assert body["result"] == 15


def test_divide_by_zero_is_a_400(client):
    response = client.get("/calc/divide?a=1&b=0")
    assert response.status_code == 400
    assert "divide by zero" in response.get_json()["error"]


def test_unknown_operation_is_a_404(client):
    assert client.get("/calc/power?a=2&b=3").status_code == 404


def test_non_numeric_input_is_a_400(client):
    assert client.get("/calc/add?a=ten&b=5").status_code == 400


def test_api_key_is_enforced_when_set(monkeypatch):
    monkeypatch.setenv("APP_API_KEY", "test-key")
    client = create_app().test_client()
    assert client.get("/calc/add?a=1&b=2").status_code == 401
    ok = client.get("/calc/add?a=1&b=2", headers={"X-API-Key": "test-key"})
    assert ok.status_code == 200
    assert ok.get_json()["result"] == 3
