import pytest

from games.domainmodel.model import Game, User, Genre, Review


@pytest.fixture()
def sample_game():
    return Game(101010, "Test Game")


@pytest.fixture()
def test_user():
    return User("testuser", "123ABCDEFGHi")


def search_game_title(in_memory_repo, sample_game):
    sample_game.add_genre(Genre("Test Genre"))
    in_memory_repo.add_game(sample_game)
    assert len(in_memory_repo.get_games_by_genre(Genre("Test Genre"))) == 1


def test_genre_count_addition(in_memory_repo, sample_game):
    initial_count = len(in_memory_repo.get_genres())
    sample_game.add_genre(Genre("Test Genre"))
    in_memory_repo.add_game(sample_game)
    assert len(in_memory_repo.get_genres()) == initial_count + 1


def test_get_unique_genres(in_memory_repo):
    assert len(in_memory_repo.get_genres()) == 1


def test_get_games_count(in_memory_repo):
    assert in_memory_repo.get_number_of_games() == 4


def test_add_game(in_memory_repo, sample_game):
    initial_count = in_memory_repo.get_number_of_games()

    in_memory_repo.add_game(sample_game)

    assert in_memory_repo.get_number_of_games() == initial_count + 1


def test_retrieve_game(in_memory_repo, sample_game):
    in_memory_repo.add_game(sample_game)
    assert in_memory_repo.get_games()[0] == Game(1228870, "Bartlow's Dread Machine")


def test_add_user(in_memory_repo):
    in_memory_repo.add_user(test_user)
    assert len(in_memory_repo.get_users()) == 6


def test_get_user(in_memory_repo, test_user):
    in_memory_repo.add_user(test_user)
    assert in_memory_repo.get_users()[-1] == test_user


def test_get_users(in_memory_repo):
    assert len(in_memory_repo.get_users()) == 5
