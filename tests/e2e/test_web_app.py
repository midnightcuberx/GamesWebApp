import pytest
from games.utilities import utilities


from flask import session


def test_register(client):
    response_code = client.get("/authentication/register").status_code
    assert response_code == 200

    response = client.post("/authentication/register", data={"username": "testUser1", "password": "testUserpassword1"})
    assert response.headers["Location"] == "/authentication/login"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("test", "test", b"Your password must be at least 8 characters, and contain an upper case letter, lower case " b"letter and a digit"),
        ("testUser1", "testUserpassword1", b"username is already taken"),
        ("test", "test1234", b"Your password must be at least 8 characters, and contain an upper case letter, lower case " b"letter and a digit"),
    ),
)
def test_register_with_invalid_input(client, username, password, message, auth):
    auth.register()

    response = client.post("/authentication/register", data={"username": username, "password": password})

    assert message in response.data


def test_login(client, auth):
    # create user
    response = auth.register()

    # check if redirects to login page
    assert response.headers["Location"] == "/authentication/login"

    # check if we can get login page
    response_code = client.get("/authentication/login").status_code

    # test login
    response = auth.login()

    # test if successful and redirected to home page
    assert response_code == 200
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["username"] == "testUser1"


def test_get_username_not_logged_in(client):
    with client:
        client.get("/")
        assert utilities.get_username() == None


def test_get_username_logged_in(client, auth):
    with client:
        auth.register()
        auth.login()
        client.get("/")
        assert session["username"] == utilities.get_username()


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Deer Journey" in response.data


def test_login_required_to_review(client):
    response = client.post("/games/review/1995240")
    assert response.headers["Location"] == "/authentication/login"


def test_review_valid(client, auth):
    auth.register()
    auth.login()

    response = client.get("/games/1995240?page=2")

    response = client.post("/games/review/1995240", data={"review_comment": "Who likes this game??", "rating": 1})
    assert response.headers["Location"] == "/games/1995240"


@pytest.mark.parametrize(
    ("comment", "rating", "messages"),
    (
        ("fuck this game its bad?", 3, (b"Your comment must not contain profanity")),
        ("wa", 3, (b"lengthen this text")),
        ("This game is pretty good", 0, b"greater than or equal to 1."),
    ),
)
def test_review_game_with_invalid_input(client, auth, comment, rating, messages):
    auth.register()
    auth.login()

    response = client.post("/games/review/1995240", data={"comment": comment, "rating": rating})
    for message in messages:
        assert message in response.data


def test_add_to_wishlist_login_required(client, auth):
    response = client.post("/games/addtowishlist/1995240")
    assert response.headers["Location"] == "/authentication/login"


def test_add_to_favourites_login_required(client, auth):
    response = client.post("/games/addtofavourites/1995240")
    assert response.headers["Location"] == "/authentication/login"


def test_show_all_favourites(client, auth):
    auth.register()
    auth.login()
    client.get("/games/addtofavourites/1995240")
    response = client.get("/user/favourites")
    assert b"Deer Journey" in response.data


def test_show_all_wishlist(client, auth):
    auth.register()
    auth.login()
    client.get("/games/addtowishlist/1995240")
    response = client.get("/user/wishlist")

    assert b"Deer Journey" in response.data


def test_game_no_reviews(client):
    response = client.get("/games/855010")
    assert response.status_code == 200
    assert b"Two Seventy" in response.data


def test_game_wtih_max_reviews(client):
    response = client.get("/games/1995240")
    assert response.status_code == 200

    assert b"DAAAAmmmn I loooove this game iti s sooo funnnn!!" in response.data
    assert b"I hate this game, not playing ever again" in response.data
    assert b"mid gmae not worth my money" in response.data


def test_games_by_genre(client):
    response = client.get("/genre/Action")
    assert response.status_code == 200
    assert b"10 Second Ninja X" in response.data
    assert b"A Blind Legend" in response.data
    assert b"ANARCHY" in response.data


def test_games_by_genre_result_limit(client):
    response = client.get("/genre/Action?num=6&method=name")
    assert response.status_code == 200
    assert b"10 Second Ninja X" in response.data
    assert b"A Blind Legend" in response.data
    assert b"ANARCHY" in response.data
    assert b"Adventure of Great Wolf" not in response.data
