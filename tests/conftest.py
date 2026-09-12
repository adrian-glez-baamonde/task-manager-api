import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Task                                     # necesario para registrar la tabla en Base.metadata


TEST_DATABASE_URL = "sqlite:///./test.db"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()                                  # crea una sesión usando el sessionmaker de test
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine_test)                  # crea las tablas antes del test
    app.dependency_overrides[get_db] = override_get_db          # sustituye la dependencia real
    yield
    Base.metadata.drop_all(bind=engine_test)                    # borra las tablas después del test