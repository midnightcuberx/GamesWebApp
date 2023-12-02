from datetime import date, datetime

import pytest

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import (
    Publisher,
    Genre,
    Game,
    User,
    Review,
    Wishlist,
)
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("Dave", "123456789")
    repo.add_user(user)
    assert repo.get_user("Dave") == user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user("mjackson")
    assert user == User("mjackson", "vpwJv4A7%#9b")


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user("Not real user in db")
    assert user is None


def test_repository_can_retrieve_games_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_games = repo.get_number_of_games()
    assert number_of_games == 877


def test_repository_can_add_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_games = repo.get_number_of_games()

    game_id = number_of_games + 1

    game = Game(game_id, "Real game trust me")
    game.price = 59.99
    game.release_date = "Nov 12, 2007"
    game.description = "A description of the game."
    game.image_url = "https://example.com/game_image.jpg"
    game.publisher = Publisher("Game Publisher")

    repo.add_game(game)

    assert repo.get_game(game_id) == game


def test_repository_can_retrieve_game_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = repo.get_game(1995240)

    assert game.title == "Deer Journey"
    # checking game data is expected
    assert len(game.reviews) == 5
    assert game.reviews[0].user.username == "thorke"

    assert Genre("Adventure") in game.genres


def test_repository_does_not_retrieve_a_non_existent_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = repo.get_game(123123123)
    assert game is None


def test_repository_can_get_games_by_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_sorted_dataset("date", repo.get_games())
    first = games[0]
    assert first.title == "Xpand Rally"


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genres = repo.get_genres()
    assert len(genres) == 24


def test_repository_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = repo.get_game(7940)
    user = User("TestUser", "TestPassword1234")
    review = Review(user, game, 5, "this is a test review")
    repo.add_review(review)
    assert game.reviews[0] == review
    # check if review is added to user and game.
    assert len(game.reviews) == 1
    assert len(user.reviews) == 1


def test_repository_add_wishlist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = repo.get_game(7940)
    user = User("TestUser", "TestPassword1234")
    repo.add_to_wishlist(user, game)
    assert user.wishlist.list_of_games[0] == game


def test_repository_add_favourites(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = repo.get_game(7940)
    user = User("TestUser", "TestPassword1234")
    repo.add_to_favourites(user, game)
    assert user.favourite_games[0] == game


def test_repository_change_user_bio(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("TestUser", "TestPassword1234")
    repo.add_user(user)
    new_bio = "this is a new bio hehehe"
    repo.change_bio(user, new_bio)
    assert user.bio == new_bio


def test_get_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_publishers()) == 798


def test_get_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_games_by_genre("Adventure")) == 344


def test_repository_get_sorted_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = repo.get_game(1995240)
    results = repo.get_sorted_reviews_for_game(game, "comment_length-descend")
    assert (
        len(results[0].comment) >= len(results[1].comment)
        and len(results[1].comment) >= len(results[2].comment)
        and len(results[2].comment) >= len(results[3].comment)
    )
