from flask import Flask, render_template
from .domainmodel.model import Game, Genre, Review, User
from .games import games
from .home import home
from .genres import genres
from .search import search
from .authentication import authentication
from .user import user
from .adapters import database_repository
from .adapters.memory_repository import MemoryRepository
from .adapters.repository_populate import populate
from .adapters.orm import metadata, map_model_to_tables

# imports from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object("config.Config")

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config["TEST_DATA_PATH"]

    if app.config["REPOSITORY"] == "memory":
        repo.repo_instance = MemoryRepository()
        populate(repo.repo_instance, "games/adapters/data/")
    elif app.config["REPOSITORY"] == "database":
        database_uri = app.config["SQLALCHEMY_DATABASE_URI"]

        database_echo = app.config["SQLALCHEMY_ECHO"]

        database_engine = create_engine(
            database_uri,
            connect_args={"check_same_thread": False},
            poolclass=NullPool,
            echo=database_echo,
        )

        session_factory = sessionmaker(
            autocommit=False, autoflush=True, bind=database_engine
        )

        repo.repo_instance = database_repository.SqlAlchemyRepository(
            session_factory
        )

        if (
            app.config["TESTING"] == "True"
            or len(database_engine.table_names()) == 0
        ):
            print("REPOPULATING DATABASE...")
            clear_mappers()
            metadata.create_all(
                database_engine
            )  # Conditionally create database tables.
            for table in reversed(
                metadata.sorted_tables
            ):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            populate(repo.repo_instance, "games/adapters/data/")
            print("REPOPULATING DATABASE... FINISHED")

        else:
            map_model_to_tables()

    with app.app_context():
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(games.games_blueprint, url_prefix="/games")
        app.register_blueprint(genres.genre_blueprint, url_prefix="/genre")
        app.register_blueprint(search.search_blueprint, url_prefix="/search")
        app.register_blueprint(
            authentication.auth_blueprint, url_prefix="/authentication"
        )
        app.register_blueprint(user.user_blueprint, url_prefix="/user")

    return app
