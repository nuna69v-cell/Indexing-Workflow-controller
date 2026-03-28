try:
    from fastapi.testclient import TestClient  # noqa: F401

    print("FastAPI TestClient imported")
    from api.main import app  # noqa: F401

    print("api.main imported")
    from api.config import settings  # noqa: F401

    print("api.config imported")
except ImportError as e:
    print(f"Import failed: {e}")
