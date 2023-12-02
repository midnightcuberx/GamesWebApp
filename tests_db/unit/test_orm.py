import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import Publisher, Genre, Game, User, Review, Wishlist


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "Test1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_name from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()

    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_name from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_game(empty_session):
    game_data = {
        'game_id': 123456,
        'game_title': "Game Title",
        'game_price': 59.99,
        'release_date': "Nov 12, 2007",
        'game_description': "A description of the game.",
        'game_image_url': "https://example.com/game_image.jpg",
        'publisher_name': "Game Publisher"
    }

    empty_session.execute(
        'INSERT INTO games (game_id, game_title, game_price, release_date, game_description, game_image_url, publisher_name) VALUES '
        '(:game_id, :game_title, :game_price, :release_date, :game_description, :game_image_url, :publisher_name)',
        game_data
    )

    row = empty_session.execute('SELECT game_id FROM games').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("Multiplayer"), ("Story_Driven")'
    )
    rows = list(empty_session.execute('SELECT genre_name from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_game_genre_association(empty_session, game_id, genre_names):
    stmt = 'INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)'
    for genre_name in genre_names:
        empty_session.execute(stmt, {'game_id': game_id, 'genre_name': genre_name})


def insert_reviewed_game(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO reviews (user_name, game_id, rating, comment) VALUES '
        '(:user_name, :game_id, 5, "Great game!")',
        {'user_name': user_key, 'game_id': game_key}
    )

    row = empty_session.execute('SELECT id from reviews').fetchone()
    return row[0]


def make_game():
    game = Game(123456, "Real game trust me")
    game.price = 59.99
    game.release_date = "Nov 12, 2007"
    game.description = "A description of the game."
    game.image_url = "https://example.com/game_image.jpg"
    game.publisher = Publisher("Game Publisher")

    return game


def make_user():
    user = User("Andrew", "Test1111")
    return user


def make_genre():
    genre = Genre("real genre")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "Test1234"))
    users.append(("Cindy", "Test1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "Test1234"),
        User("Cindy", "Test1111")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "Test1111")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "Test1111"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "Test1234")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_game(empty_session):
    game_key = insert_game(empty_session)
    expected_game = make_game()
    fetched_Game = empty_session.query(Game).one()

    assert expected_game == fetched_Game
    assert game_key == fetched_Game.game_id


def test_loading_of_genre_game(empty_session):
    game_key = insert_game(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_game_genre_association(empty_session, game_key, genre_keys)

    game = empty_session.query(Game).get(game_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert genre in game.genres


def test_loading_of_reviewed_game(empty_session):
    insert_reviewed_game(empty_session)
    rows = empty_session.query(Game).all()

    assert len(rows) > 0
    game = rows[0]
    assert len(game.reviews) > 0

    review = game.reviews[0]

    assert review.rating == 5
    assert review.comment == "Great game!"


def test_saving_of_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__username == "Andrew").one()

    review_text = "Some new review text."
    review = Review(user, game, 5, review_text)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, game_id, 5, comment FROM reviews'))

    assert rows == [(user_key, game_key, 5, review_text)]


def test_saving_of_game(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT game_id, game_title, game_price, release_date, game_description, game_image_url, publisher_name FROM games'))

    assert rows == [(123456,
                     "Real game trust me",
                     59.99,
                     "Nov 12, 2007",
                     "A description of the game.",
                     "https://example.com/game_image.jpg",
                     "Game Publisher"
                     )]



def test_saving_of_game_with_genre(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()

    genre_name = "Adventure"
    empty_session.execute('INSERT INTO genres (genre_name) VALUES (:genre_name)', {'genre_name': genre_name})

    game_id = game.game_id
    empty_session.execute('INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)',
                          {'game_id': game_id, 'genre_name': genre_name})


    fetched_game = empty_session.query(Game).one()
    assert genre_name in [genre.genre_name for genre in fetched_game.genres]

def test_save_commented_article(empty_session):
    game = make_game()
    user = make_user()


    review_text = "Some new review text."
    review = Review(user, game, 5, review_text)


    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]

    rows = list(empty_session.execute('SELECT user_name FROM users'))
    user_key = rows[0][0]

    rows = list(empty_session.execute('SELECT user_name, game_id, 5, comment FROM reviews'))

    assert rows == [(user_key, game_key, 5, review_text)]