import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games.adapters import database_repository, repository_populate
from games.adapters.orm import metadata, map_model_to_tables


TEST_DATA_PATH_DATABASE_FULL = "games/adapters/data/"
TEST_DATA_PATH_DATABASE_LIMITED = "tests/data/"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///games-test.db'

@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    repository_populate.populate(repo_instance, TEST_DATA_PATH_DATABASE_LIMITED)
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    repository_populate.populate(repo_instance, TEST_DATA_PATH_DATABASE_FULL)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)