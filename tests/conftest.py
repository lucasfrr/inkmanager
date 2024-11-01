import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from inkmanager.app import app
from inkmanager.database import get_session
from inkmanager.models import table_registry
from inkmanager.settings import Settings


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(Settings().DATABASE_URL)
    table_registry.metadata.create_all(engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with Session() as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)
