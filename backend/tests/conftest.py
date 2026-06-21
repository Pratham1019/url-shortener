import os
import sys
from pathlib import Path

import pytest
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Provide an HTTP client bound to the real FastAPI app."""
    return TestClient(app)
