import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from ..main import app  # Adjust import if needed
from ..services.database import get_session  # Adjust import
from ..models import Store, Shoe

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
DATABASE_URL = "sqlite:///test_db.sqlite"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# Override session dependency
def get_test_session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def setup_db():
    """Setup and teardown the test database."""
    SQLModel.metadata.create_all(engine)  # Create tables before test
    yield
    SQLModel.metadata.drop_all(engine)  # Cleanup after test


@pytest.fixture(scope="module")
def client():
    """Provides a test client for FastAPI app."""
    app.dependency_overrides[get_session] = get_test_session
    return TestClient(app)
