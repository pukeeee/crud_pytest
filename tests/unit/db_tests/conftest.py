import pytest
from src.db.database import engine, Base, SessionLocal


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # Создать все таблицы
    Base.metadata.create_all(bind = engine)
    yield
    # После теста удалить все таблицы
    # Base.metadata.drop_all(bind = engine)


@pytest.fixture()   
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def user_data():
    return {
        "user_name": "TestUser",
        "email": "testuser@mail.com",
        "password": "Password123/",
        "start_date": 20240628,
        "status": True
    }