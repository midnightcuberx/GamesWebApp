import pytest

from games import create_app
from games.adapters import memory_repository
from games.adapters.repository_populate import populate
from games.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(repo, "tests/data/")
    return repo


@pytest.fixture
def client():
    my_app = create_app(
        {
            "TESTING": True,
            "TEST_DATA_PATH": "tests/data/",
            "WTF_CSRF_ENABLED": False,
            "REPOSITORY": "memory",
        }
    )

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self, username="testUser1", password="testUserpassword1"):
        return self.__client.post(
            "/authentication/register",
            data={"username": username, "password": password},
        )

    def login(self, username="testUser1", password="testUserpassword1"):
        return self.__client.post(
            "/authentication/login",
            data={"username": username, "password": password},
        )

    def logout(self):
        return self.__client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
