from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app import config, models, schemas
from app.main import app
from app.database import Base, get_db
from app.oauth2 import create_access_token


settings = config.settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_usr}:{settings.db_pwd}@{settings.db_host}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    # Run our code after our test
    Base.metadata.drop_all(bind=engine)
    # Run our code before we run our test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def overide_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overide_get_db

    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    EMAIL = "user123@example.com"
    PASSWORD = "password123"

    user_data = {"email": EMAIL, "password": PASSWORD}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = PASSWORD
    return new_user


@pytest.fixture
def test_user(client):
    EMAIL = "user@example.com"
    PASSWORD = "password123"

    user_data = {"email": EMAIL, "password": PASSWORD}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = PASSWORD
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"],
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2["id"],
        },
    ]
    session.add_all([models.Post(**post) for post in post_data])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
