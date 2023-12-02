from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User
from flask import session


# services that are needed in more than one page
def get_all_games(repo: AbstractRepository):
    return repo.get_games()


def get_all_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_username():
    username = None
    if "username" in session:
        print(session)
        username = session["username"]
    return username


def get_user(user_name: str, repo: AbstractRepository):
    if user_name is None:
        return None
    return repo.get_user(user_name)  # needs working on


def check_valid_session(repo: AbstractRepository):
    username = get_username()
    if username == None:
        session.clear()
        return
    if get_user(username, repo) == None:
        session.clear()


def get_game(game_id, repo: AbstractRepository):
    return repo.get_game(game_id)


def remove_from_wishlist(user: User, game: Game, repo: AbstractRepository):
    repo.remove_from_wishlist(user, game)


def remove_from_favourites(user: User, game: Game, repo: AbstractRepository):
    repo.remove_from_favourites(user, game)


def get_sublist(super_list, length, repo: AbstractRepository):
    return repo.get_sublist(super_list, length)
