import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.database.base import Base
from app.main import app


# Isolated in-memory database for testing.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture
def client():

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_create_disease(client):

    payload = {
        "name": "Distrofia muscular de Duchenne",
        "slug": "distrofia-muscular-duchenne",
        "summary": "Información educativa sobre esta enfermedad.",
        "description": (
            "La distrofia muscular de Duchenne es "
            "una enfermedad genética poco frecuente."
        ),
    }

    response = client.post(
        "/api/v1/diseases",
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]


def test_get_diseases(client):

    response = client.get("/api/v1/diseases")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_disease_not_found(client):

    response = client.get("/api/v1/diseases/999")

    assert response.status_code == 404


def test_invalid_disease_payload(client):

    response = client.post(
        "/api/v1/diseases",
        json={"name": "AB"},
    )

    assert response.status_code == 422