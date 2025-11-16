from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

API_KEY = "dev-secret-key"  # Should match your settings or .env
HEADERS = {"X-API-Key": API_KEY}


def test_auth_required_documents():
    resp = client.get("/documents/")
    assert resp.status_code == 401
    resp = client.get("/documents/", headers=HEADERS)
    assert resp.status_code in (200, 422)  # 422 if no docs exist


def test_auth_required_ai():
    resp = client.post("/ai/query", json={"question": "Test?"})
    assert resp.status_code == 401
    resp = client.post("/ai/query", json={"question": "Test?"}, headers=HEADERS)
    assert resp.status_code in (200, 422)


def test_document_retrieval():
    # This test assumes at least one document exists or will handle 404 gracefully
    resp = client.get("/documents/", headers=HEADERS)
    if resp.status_code == 200 and resp.json():
        doc_id = resp.json()[0]["id"]
        resp2 = client.get(f"/documents/{doc_id}", headers=HEADERS)
        assert resp2.status_code in (200, 404)
    else:
        assert resp.status_code in (200, 422)


def test_mock_llm(monkeypatch):
    # Patch ai_service.query_llm to return a fixed answer
    from app.services.ai_service import AIService

    async def fake_query_llm(self, prompt):
        return "mocked-answer"

    monkeypatch.setattr(AIService, "query_llm", fake_query_llm)
    resp = client.post("/ai/query", json={"question": "Test?"}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["answer"] == "mocked-answer"
