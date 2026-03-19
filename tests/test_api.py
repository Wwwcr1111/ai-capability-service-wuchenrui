from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_text_summary_success() -> None:
    response = client.post(
        "/v1/capabilities/run",
        json={
            "capability": "text_summary",
            "input": {
                "text": "This is a long text for summary.",
                "max_length": 10,
            },
            "request_id": "req-123",
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["data"]["result"] == "This is a ..."
    assert body["meta"]["request_id"] == "req-123"
    assert body["meta"]["capability"] == "text_summary"
    assert isinstance(body["meta"]["elapsed_ms"], int)


def test_text_summary_generates_request_id() -> None:
    response = client.post(
        "/v1/capabilities/run",
        json={
            "capability": "text_summary",
            "input": {"text": "short text"},
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    UUID(body["meta"]["request_id"])


def test_text_summary_empty_text_error() -> None:
    response = client.post(
        "/v1/capabilities/run",
        json={
            "capability": "text_summary",
            "input": {"text": "   "},
        },
    )

    body = response.json()
    assert response.status_code == 400
    assert body["ok"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["meta"]["capability"] == "text_summary"


def test_text_summary_invalid_max_length_error() -> None:
    response = client.post(
        "/v1/capabilities/run",
        json={
            "capability": "text_summary",
            "input": {"text": "hello world", "max_length": 0},
        },
    )

    body = response.json()
    assert response.status_code == 400
    assert body["ok"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"


def test_text_stats_success() -> None:
    response = client.post(
        "/v1/capabilities/run",
        json={
            "capability": "text_stats",
            "input": {"text": "hello world\nsecond line"},
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["data"]["result"] == {
        "char_count": 23,
        "word_count": 4,
        "line_count": 2,
    }


def test_capability_not_found() -> None:
    response = client.post(
        "/v1/capabilities/run",
        json={
            "capability": "unknown_capability",
            "input": {"text": "hello"},
        },
    )

    body = response.json()
    assert response.status_code == 404
    assert body["ok"] is False
    assert body["error"]["code"] == "CAPABILITY_NOT_FOUND"
    assert body["meta"]["capability"] == "unknown_capability"


def test_request_schema_validation_error() -> None:
    response = client.post(
        "/v1/capabilities/run",
        json={
            "input": {"text": "hello"},
        },
    )

    body = response.json()
    assert response.status_code == 422
    assert body["ok"] is False
    assert body["error"]["code"] == "REQUEST_SCHEMA_VALIDATION_ERROR"
    assert body["meta"]["capability"] is None
