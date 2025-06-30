import pytest
from src.db.database import engine, Base, SessionLocal
from src.controller.user_controller import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind = engine, checkfirst=True)
    yield
    Base.metadata.drop_all(bind = engine)


@pytest.fixture()   
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture()
def user_data():
    return {
        "user_name": "TestUser",
        "email": "testuser@mail.com",
        "password": "Password123/",
        "status": True
    }