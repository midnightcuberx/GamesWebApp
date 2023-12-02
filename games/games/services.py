from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Review
import math

from games.utilities import utilities


def get_sorted_games(sort_type, repo: AbstractRepository):
    return repo.get_sorted_dataset(sort_type)


# def get_game(game_id, repo: AbstractRepository):
#     return repo.get_game(game_id)


def get_sublist(super_list, length, repo: AbstractRepository):
    return repo.get_sublist(super_list, length)


def get_number_of_pages(games_per_page, repo: AbstractRepository):
    return math.ceil(repo.get_number_of_games() / games_per_page)


# def get_user(name, repo: AbstractRepository):
#     return repo.get_user(name)


def add_to_wishlist(user: User, game: Game, repo: AbstractRepository):
    repo.add_to_wishlist(user, game)
    # print(user._User__wishlist)


def in_wishlist(user: User, game: Game):
    return game in user.wishlist


# def remove_from_wishlist(user: User, game: Game):
#     user.wishlist.remove_game(game)


def add_to_favourites(user: User, game: Game, repo: AbstractRepository):
    repo.add_to_favourites(user, game)


def in_favourites(user: User, game: Game):
    return game in user.favourite_games


# def remove_from_favourites(user: User, game: Game):
#     user.remove_favourite_game(game)


def get_sorted_reviews(game: Game, sort_option: str, repo: AbstractRepository):
    return repo.get_sorted_reviews_for_game(game, sort_option)


def add_review(review: Review, repo: AbstractRepository):
    repo.add_review(review)


def get_game_average_reviews(game: Game):
    total = 0
    for review in game.reviews:
        total = total + review.rating
    if total == 0:
        return None
    return total / len(game.reviews)
