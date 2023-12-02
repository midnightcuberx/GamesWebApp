import pytest
import os
from games.domainmodel.model import (
    Publisher,
    Genre,
    Game,
    Review,
    User,
    Wishlist,
)
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def test_publisher_init():
    publisher1 = Publisher("Publisher A")
    assert repr(publisher1) == "<Publisher Publisher A>"
    assert publisher1.publisher_name == "Publisher A"

    publisher2 = Publisher("")
    assert publisher2.publisher_name is None

    publisher3 = Publisher(123)
    assert publisher3.publisher_name is None

    publisher4 = Publisher(" Wild Rooster   ")
    assert publisher4.publisher_name == "Wild Rooster"

    publisher4.publisher_name = "Century Game"
    assert repr(publisher4) == "<Publisher Century Game>"


def test_publisher_eq():
    publisher1 = Publisher("Publisher A")
    publisher2 = Publisher("Publisher A")
    publisher3 = Publisher("Publisher B")
    assert publisher1 == publisher2
    assert publisher1 != publisher3
    assert publisher3 != publisher2
    assert publisher3 == publisher3


def test_publisher_lt():
    publisher1 = Publisher("Wild Rooster")
    publisher2 = Publisher("Century Game")
    publisher3 = Publisher("Big Fish Games")
    assert publisher1 > publisher2
    assert publisher2 > publisher3
    assert publisher1 > publisher3
    publisher_list = [publisher3, publisher2, publisher1]
    assert sorted(publisher_list) == [publisher3, publisher2, publisher1]


def test_publisher_hash():
    publishers = set()
    publisher1 = Publisher("Wild Rooster")
    publisher2 = Publisher("Century Game")
    publisher3 = Publisher("Big Fish Games")
    publishers.add(publisher1)
    publishers.add(publisher2)
    publishers.add(publisher3)
    assert len(publishers) == 3
    assert (
        repr(sorted(publishers))
        == "[<Publisher Big Fish Games>, <Publisher Century Game>, <Publisher Wild "
        "Rooster>]"
    )
    publishers.discard(publisher1)
    assert (
        repr(sorted(publishers))
        == "[<Publisher Big Fish Games>, <Publisher Century Game>]"
    )


def test_publisher_name_setter():
    publisher = Publisher("Wild Rooster")
    publisher.publisher_name = "   Big Fish Games  "
    assert repr(publisher) == "<Publisher Big Fish Games>"

    publisher.publisher_name = ""
    assert publisher.publisher_name is None

    publisher.publisher_name = 123
    assert publisher.publisher_name is None


def test_genre_initialization():
    genre1 = Genre("Adventure")
    assert repr(genre1) == "<Genre Adventure>"
    genre2 = Genre(" Action ")
    assert repr(genre2) == "<Genre Action>"
    genre3 = Genre(300)
    assert repr(genre3) == "<Genre None>"
    genre5 = Genre(" Early Access  ")
    assert genre5.genre_name == "Early Access"
    genre1 = Genre("")
    assert genre1.genre_name is None


def test_genre_name_setter():
    genre1 = Genre("Genre A")
    assert genre1.genre_name == "Genre A"

    genre1 = Genre("")
    assert genre1.genre_name is None

    genre1 = Genre(123)
    assert genre1.genre_name is None


def test_genre_eq():
    genre1 = Genre("Action")
    genre2 = Genre("Indie")
    genre3 = Genre("Sports")
    assert genre1 == genre1
    assert genre1 != genre2
    assert genre2 != genre3
    assert genre1 != "Adventure"
    assert genre2 != 105


def test_genre_hash():
    genre1 = Genre("Action")
    genre2 = Genre("Indie")
    genre3 = Genre("Sports")
    genre_set = set()
    genre_set.add(genre1)
    genre_set.add(genre2)
    genre_set.add(genre3)
    assert sorted(genre_set) == [genre1, genre2, genre3]
    genre_set.discard(genre2)
    genre_set.discard(genre1)
    assert sorted(genre_set) == [genre3]


def test_genre_lt():
    genre1 = Genre("Action")
    genre2 = Genre("Indie")
    genre3 = Genre("Sports")
    assert genre1 < genre2
    assert genre2 < genre3
    assert genre3 > genre1
    genre_list = [genre3, genre2, genre1]
    assert sorted(genre_list) == [genre1, genre2, genre3]


def test_game_initialization():
    game1 = Game(1, "Super Soccer Blast")
    assert repr(game1) == "<Game 1, Super Soccer Blast>"
    game2 = Game(101, "     DuckMan    ")
    assert repr(game2) == "<Game 101, DuckMan>"
    with pytest.raises(ValueError):
        game3 = Game(-123, "Super Soccer Blast")
    game4 = Game(123, " ")
    assert game4.title is None


def test_game_title_setter():
    game1 = Game(1, "Super Soccer Blast")
    game1.title = "Dark Throne"
    assert game1.title == "Dark Throne"
    game1.title = " "
    assert game1.title is None


def test_game_price_setter():
    game = Game(1, "Domino House")
    game.price = 2.99
    assert game.price == 2.99
    with pytest.raises(ValueError):
        game.price = -1


def test_game_release_date_setter():
    game = Game(1, "Super Soccer Blast")
    game.release_date = "Oct 21, 2008"
    assert game.release_date == "Oct 21, 2008"
    with pytest.raises(ValueError):
        game.release_date = "21/08/2008"


def test_game_description_setter():
    game = Game(1, "Domino House")
    game.description = "This is a domino game"
    assert game.description == "This is a domino game"
    game.description = ""
    assert game.description is None


def test_game_image_url_setter():
    game = Game(1, "Domino House")
    game.image_url = "https://domino.com/image.jpg"
    assert game.image_url == "https://domino.com/image.jpg"
    game.image_url = " "
    assert game.image_url is None


def test_game_website_url_setter():
    game = Game(1, "Deer Journey")
    game.website_url = "https://deerjourney.com"
    assert game.website_url == "https://deerjourney.com"
    game.website_url = " "
    assert game.website_url is None


def test_game_eq():
    game1 = Game(1, "Domino House")
    game2 = Game(1, "Super Soccer Blast")
    game3 = Game(101, "     DuckMan    ")
    assert game1 == game1
    assert game2 == game2
    assert game1 == game2
    assert game1 != game3
    assert game2 != 30
    assert game3 != " Deer Journey"


def test_game_hash():
    game1 = Game(1, "Domino House")
    game2 = Game(2, "Super Soccer Blast")
    game3 = Game(3, "     DuckMan    ")
    game_set = set()
    game_set.add(game1)
    game_set.add(game2)
    game_set.add(game3)
    assert sorted(game_set) == [game1, game2, game3]
    game_set.discard(game2)
    game_set.discard(game1)
    assert sorted(game_set) == [game3]


def test_game_lt():
    game1 = Game(1, "Domino House")
    game2 = Game(2, "Super Soccer Blast")
    game3 = Game(3, "     DuckMan    ")
    assert game1 < game2
    assert game2 < game3
    assert game3 > game1
    genre_list = [game3, game2, game1]
    assert sorted(genre_list) == [game1, game2, game3]


def test_game_add_remove_genre():
    game1 = Game(1, "Super Soccer Blast")
    genre1 = Genre("Adventure")
    game1.add_genre(genre1)
    assert genre1 in game1.genres
    assert len(game1.genres) == 1

    genre2 = Genre("Sports")
    game1.add_genre(genre2)
    assert len(game1.genres) == 2
    game1.remove_genre(genre2)
    game1.remove_genre(genre1)
    assert genre2 not in game1.genres
    assert len(game1.genres) == 0


def test_user_initialization():
    user1 = User("Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    assert repr(user1) == "<User Shyamli>"
    assert repr(user2) == "<User asma>"
    assert repr(user3) == "<User JeNNy>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User("xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User("    ", "qwerty12345")


def test_user_eq():
    user1 = User("Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    user4 = User("Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User("   Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user3, user1, user2]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User("Shyamli", "pw12345")
    user2 = User("asma", "pw67890")
    user3 = User("JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 > user3
    assert user3 < user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user3, user1, user2]


def test_user_add_remove_favourite_games():
    user1 = User("Shyamli", "pw12345")
    game1 = Game(1, "Domino Game")
    game2 = Game(2, "Deer Journey")
    game3 = Game(3, "Fat City")
    user1.add_favourite_game(game1)
    user1.add_favourite_game(game2)
    user1.add_favourite_game(game3)
    assert (
        repr(user1.favourite_games)
        == "[<Game 1, Domino Game>, <Game 2, Deer Journey>, <Game 3, Fat City>]"
    )
    assert len(user1.favourite_games) == 3
    game4 = Game(1, "Domino Game")
    user1.add_favourite_game(game4)
    assert len(user1.favourite_games) == 3
    user1.remove_favourite_game(game1)
    user1.remove_favourite_game(game2)
    assert repr(user1.favourite_games) == "[<Game 3, Fat City>]"


def test_user_add_remove_reviews():
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    review1 = Review(user, game, 3, "Great game!")
    review2 = Review(user, game, 4, "Superb game!")
    review3 = Review(user, game, 2, "Boring game!")
    assert len(user.reviews) == 0
    user.add_review(review1)
    user.add_review(review2)
    user.add_review(review3)
    assert user.reviews == [review1, review2, review3]
    user.add_review(review1)
    assert len(user.reviews) == 3
    user.add_review(300)
    user.add_review("review")
    user.add_review(None)
    assert len(user.reviews) == 3
    user.remove_review(review2)
    user.remove_review(review1)
    user.remove_review(review1)
    assert user.reviews == [review3]


def test_review_initialization():
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    review = Review(user, game, 4, "Great game!")
    assert review.user == user
    assert review.game == game
    assert review.rating == 4
    assert review.comment == "Great game!"

    with pytest.raises(ValueError):
        review2 = Review(user, game, 6, "Great game!")


def test_review_eq():
    user = User("Shyamli", "pw12345")
    game = Game(1, "Domino Game")
    review1 = Review(user, game, 4, "Great game!")
    review2 = Review(user, game, 4, "Superb game!")
    review3 = Review(user, game, 5, "Boring game!")
    review4 = Review(user, game, 2, "Classic game!")
    assert review1 == review1
    assert review1 != review3
    assert review1 != review4
    assert review1 != review2
    assert review1 != "Classic Game"
    assert review1 != 2


@pytest.fixture
def user():
    return User("Shyamli", "pw12345")


@pytest.fixture
def game():
    return Game(1, "Domino Game")


@pytest.fixture
def wishlist(user):
    return Wishlist(user)


def test_wishlist_initialization(wishlist):
    assert len(wishlist.list_of_games) == 0


def test_add_game(wishlist, game):
    wishlist.add_game(game)
    assert len(wishlist.list_of_games) == 1
    assert wishlist.list_of_games[0] == game


def test_remove_game(wishlist, game):
    wishlist.add_game(game)
    wishlist.remove_game(game)
    assert len(wishlist.list_of_games) == 0


def test_select_game(wishlist, game):
    wishlist.add_game(game)
    assert wishlist.select_game(0) == game


def test_select_game_out_of_index(wishlist):
    assert wishlist.select_game(0) is None


def test_first_game_in_list(wishlist, game):
    wishlist.add_game(game)
    assert wishlist.first_game_in_list() == game


def test_first_game_in_empty_list(wishlist):
    assert wishlist.first_game_in_list() is None


def test_wishlist_iter(wishlist, game):
    wishlist.add_game(game)
    wishlist_iterator = iter(wishlist)
    assert next(wishlist_iterator) == game


# Unit tests for CSVReader
def create_csv_reader():
    dir_name = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    games_file_name = os.path.join(dir_name, "games/adapters/data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    return reader


def test_csv_reader():
    reader = create_csv_reader()
    assert len(reader.dataset_of_games) == 877
    assert len(reader.dataset_of_publishers) == 798
    assert len(reader.dataset_of_genres) == 24


def test_read_csv_file():
    reader = create_csv_reader()
    game = next(iter(reader.dataset_of_games))
    assert game.game_id == 435790
    assert game.title == "10 Second Ninja X"
    assert game.price == 0.99
    assert game.release_date == "Jul 19, 2016"
    assert game.publisher == Publisher("Curve Games")
    assert game.genres == [Genre("Action"), Genre("Indie")]


def test_tracks_dataset():
    reader = create_csv_reader()
    sorted_games = sorted(reader.dataset_of_games)
    sorted_games_str = str(sorted_games[:3])
    assert (
        sorted_games_str
        == "[<Game 3010, Xpand Rally>, <Game 7940, Call of Duty® 4: Modern Warfare®>, <Game 11370, Nikopol: Secrets of the Immortals>]"
    )


def test_publisher_dataset():
    reader = create_csv_reader()
    publishers_set = reader.dataset_of_publishers
    sorted_publishers = sorted(publishers_set)
    sorted_publishers_str = str(sorted_publishers[:3])
    assert (
        sorted_publishers_str
        == "[<Publisher 13-lab,azimuth team>, <Publisher 2Awesome Studio>, <Publisher 2Frogs Software>]"
    )


def test_genres_dataset():
    reader = create_csv_reader()
    genres_set = reader.dataset_of_genres
    sorted_genres = sorted(genres_set)
    sorted_genre_sample = str(sorted_genres[:3])
    assert (
        sorted_genre_sample
        == "[<Genre Action>, <Genre Adventure>, <Genre Animation & Modeling>]"
    )


def test_game_add_remove_reviews():
    user = User("testUser1", "pw12345")
    user2 = User("testUser2", "pw12345")
    game = Game(1, "test Game")
    review1 = Review(user, game, 3, "Great game!")
    review2 = Review(user2, game, 4, "Superb game!")
    not_related_game = (2, "different game")
    not_related_review = Review(user2, game, 4, "Superb game!")
    game.add_review(review1)
    game.add_review(review2)
    assert len(game.reviews) == 2
    game.remove_review(review1)
    assert game.reviews[0] == review2
    game.add_review(review1)
    assert game.reviews[0] == review2 and game.reviews[1] == review1
    game.remove_review(review1)
    game.remove_review(review2)
    assert len(game.reviews) == 0
    game.remove_review(not_related_review)
    assert len(game.reviews) == 0
