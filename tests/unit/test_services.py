import pytest
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Game, Genre, Publisher, User, Review
from games.genres import services as genre_services
from games.search import services as search_services
from games.home import services as home_services
from games.authentication import services as authentication_services

from werkzeug.security import generate_password_hash

from games.games import services as game_services
from games.utilities import utilities as utilities


# Utilities services tests
def test_get_all_games_util(in_memory_repo):
    result = utilities.get_all_games(in_memory_repo)
    assert len(result) == 4


def test_get_all_genres_util(in_memory_repo):
    result = utilities.get_all_genres(in_memory_repo)
    assert len(result) == 1


def test_get_number_of_games(in_memory_repo):
    result = utilities.get_number_of_games(in_memory_repo)
    assert result == 4


# Home services tests
def test_get_latest_games(in_memory_repo):
    result = home_services.get_sorted_games("latest", in_memory_repo)
    assert result[0].game_id == 1228870 and result[1].game_id == 410320 and result[2].game_id == 311120 and result[3].game_id == 7940


def test_get_home_genres(in_memory_repo):
    result = home_services.get_genres(in_memory_repo)
    assert len(result) == 1


# Games services tests
def test_get_sorted_games_latest(in_memory_repo):
    result = game_services.get_sorted_games("latest", in_memory_repo)
    assert result[0].game_id == 1228870 and result[1].game_id == 410320 and result[2].game_id == 311120 and result[3].game_id == 7940


def test_get_sorted_games_alphabetical(in_memory_repo):
    result = game_services.get_sorted_games("name", in_memory_repo)
    assert result[0].game_id == 1228870 and result[1].game_id == 7940 and result[2].game_id == 410320 and result[3].game_id == 311120


# def test_get_game(in_memory_repo):
#     result = game_services.get_game(1228870, in_memory_repo)
#     assert result.game_id == 1228870


def test_get_sublist(in_memory_repo):
    super_list = [1, 2, 3, 4, 5]
    result = game_services.get_sublist(super_list, 3, in_memory_repo)
    assert len(result) == 2


def test_get_number_of_pages(in_memory_repo):
    result = game_services.get_number_of_pages(6, in_memory_repo)
    assert result == 1


# Genre services tests
def test_get_sorted_games(in_memory_repo):
    result = genre_services.get_sorted_games("name", "Action", in_memory_repo)
    assert result[0].game_id == 1228870 and result[1].game_id == 7940 and result[2].game_id == 410320 and result[3].game_id == 311120


def test_get_sublist(in_memory_repo):
    super_list = [1, 2, 3, 4, 5]
    result = genre_services.get_sublist(super_list, 3, in_memory_repo)
    assert len(result) == 2


def test_get_genres(in_memory_repo):
    result = genre_services.get_genres(in_memory_repo)
    assert len(result) == 1


# Search services tests
def test_get_all_games(in_memory_repo):
    result = search_services.get_all_games(in_memory_repo)
    assert len(result) == 4


def test_get_all_genres(in_memory_repo):
    result = search_services.get_all_genres(in_memory_repo)
    assert len(result) == 1


def test_get_all_publishers(in_memory_repo):
    result = search_services.get_all_publishers(in_memory_repo)
    assert len(result) == 4


def test_get_matching_games_query(in_memory_repo):
    search_query = "Call".lower()
    selected_genre = Genre("")
    selected_publisher = Publisher("")
    result = search_services.search_games(search_query, selected_genre, selected_publisher, in_memory_repo)
    assert len(result) == 1


def test_get_matching_games_genre(in_memory_repo):
    search_query = ""
    selected_genre = Genre("Action")
    selected_publisher = Publisher("")
    result = search_services.search_games(search_query, selected_genre, selected_publisher, in_memory_repo)
    assert len(result) == 4


def test_get_matching_games_publisher(in_memory_repo):
    search_query = ""
    selected_genre = Genre("")
    selected_publisher = Publisher("Buka Entertainment")
    result = search_services.search_games(search_query, selected_genre, selected_publisher, in_memory_repo)
    assert len(result) == 1


def test_get_matching_games_not_found(in_memory_repo):
    search_query = "NotRealGame".lower()
    selected_genre = Genre("")
    selected_publisher = Publisher("")
    result = search_services.search_games(search_query, selected_genre, selected_publisher, in_memory_repo)
    assert len(result) == 0


def test_get_total_pages(in_memory_repo):
    matching_games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    result = search_services.get_total_pages(matching_games, 20)
    assert result == 2


def test_get_total_pages_upper_bound(in_memory_repo):
    matching_games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    result = search_services.get_total_pages(matching_games, 20)
    assert result == 1


def test_get_total_pages_lower_bound(in_memory_repo):
    matching_games = [1]
    result = search_services.get_total_pages(matching_games, 20)
    assert result == 1


def test_search_games(in_memory_repo):
    selected_genre = Genre("Action")
    selected_publisher = Publisher("")
    query = ""
    result = search_services.search_games(query, selected_genre, selected_publisher, in_memory_repo)
    assert len(result) == 4


def test_search_games_no_results(in_memory_repo):
    selected_genre = Genre("Non existent")
    selected_publisher = Publisher("")
    query = ""
    result = search_services.search_games(query, selected_genre, selected_publisher, in_memory_repo)
    assert len(result) == 0


def test_get_results_for_page_upper_bound():
    matching_games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    result = search_services.get_results_for_page(matching_games, 2, 20)
    assert len(result) == 1


def test_get_results_for_page():
    matching_games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    result = search_services.get_results_for_page(matching_games, 1, 20)
    assert len(result) == 20


def test_get_results_for_page_lower_bound():
    matching_games = [1]
    result = search_services.get_results_for_page(matching_games, 1, 20)
    assert len(result) == 1


def test_get_user(in_memory_repo):
    assert (utilities.get_user("FirsttestUser1", in_memory_repo)) == User("FirsttestUser1", "testUser1231")


def test_get_invaliduser(in_memory_repo):
    assert (utilities.get_user("I AM NOT A REAL USERNAME MUAHAHAHA", in_memory_repo)) is None


def test_get_game_average_reviews(in_memory_repo):
    assert game_services.get_game_average_reviews(in_memory_repo.get_game(1228870)) == 3.25


def test_get_game_average_reviews_single_review(in_memory_repo):
    assert game_services.get_game_average_reviews(in_memory_repo.get_game(311120)) == 2


def test_get_game_average_reviews_no_review(in_memory_repo):
    assert game_services.get_game_average_reviews(in_memory_repo.get_game(7940)) is None


def test_get_game_average_reviews_invalid_game_id(in_memory_repo):
    try:
        game_services.get_game_average_reviews(in_memory_repo.get_game(1010010101010010101))
    except ValueError as e:
        assert "is not in list" in str(e)


def test_get_sorted_reviews_length_ascend(in_memory_repo):
    results = game_services.get_sorted_reviews(in_memory_repo.get_game(1228870), "comment_length-ascend", in_memory_repo)
    assert len(results[0].comment) <= len(results[1].comment) and len(results[1].comment) <= len(results[2].comment) and len(results[2].comment) <= len(results[3].comment)


def test_get_sorted_reviews_length_descend(in_memory_repo):
    results = game_services.get_sorted_reviews(in_memory_repo.get_game(1228870), "comment_length-descend", in_memory_repo)
    assert len(results[0].comment) >= len(results[1].comment) and len(results[1].comment) >= len(results[2].comment) and len(results[2].comment) >= len(results[3].comment)


def test_get_sorted_reviews_star_descend(in_memory_repo):
    results = game_services.get_sorted_reviews(in_memory_repo.get_game(1228870), "star_ratings-descend", in_memory_repo)
    assert results[0].rating >= results[1].rating and results[1].rating >= results[2].rating and results[2].rating >= results[3].rating


def test_get_sorted_reviews_star_ascend(in_memory_repo):
    results = game_services.get_sorted_reviews(in_memory_repo.get_game(1228870), "star_ratings-ascend", in_memory_repo)
    assert results[0].rating <= results[1].rating and results[1].rating <= results[2].rating and results[2].rating <= results[3].rating


def test_get_sorted_reviews_game_no_reviews(in_memory_repo):
    results = game_services.get_sorted_reviews(in_memory_repo.get_game(7940), "star_ratings-ascend", in_memory_repo)
    assert len(results) == 0


def test_add_valid_user(in_memory_repo):
    user = User("testuser", "Testabcdefg123")
    authentication_services.add_user("testuser", "Testabcdefg123", in_memory_repo)
    assert len(in_memory_repo.get_users()) == 6 and in_memory_repo.get_users()[-1] == user


def test_add_invalid_user(in_memory_repo):
    try:
        authentication_services.add_user("testuser", "Testabcdefg123", in_memory_repo)
        authentication_services.add_user("testuser", "Testadbcdefg123", in_memory_repo)
        assert False
    except authentication_services.NameNotUniqueException:
        assert True


def test_get_valid_user(in_memory_repo):
    authentication_services.add_user("testuser", "Testabcdefg123", in_memory_repo)
    try:
        authentication_services.get_user("testuser", in_memory_repo)
    except Exception as e:
        assert False
    assert True


def test_get_invalid_user(in_memory_repo):
    try:
        authentication_services.get_user("testuser1232321", in_memory_repo)
        assert False
    except authentication_services.UnknownUserException:
        assert True


def test_authenticate_user(in_memory_repo):
    try:
        authentication_services.add_user("testuser", "Testabcdefg123", in_memory_repo)
        authentication_services.authenticate_user("testuser", "Testabcdefg123", in_memory_repo)
    except Exception as e:
        assert False
    assert True


def test_utilities_get_user(in_memory_repo):
    assert utilities.get_user("FirsttestUser1", in_memory_repo) == User("FirsttestUser1", "testUser1231")
