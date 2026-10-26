import os
import tempfile

# Configure the app before it is imported: a throwaway SQLite file and a test secret.
_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = f"sqlite:///{_db.name}"
os.environ.setdefault("JWT_SECRET", "test-secret")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_header(client):
    import uuid

    username = f"user_{uuid.uuid4().hex[:8]}"
    client.post("/register", json={"username": username, "password": "s3cret-pass"})
    token = client.post("/login", json={"username": username, "password": "s3cret-pass"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
