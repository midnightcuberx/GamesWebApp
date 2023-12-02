from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User
import games.utilities.utilities as utilities
import math


def get_wishlist(user: User):
    return user.wishlist.list_of_games


def get_favourite_games(user: User):
    return user.favourite_games


def get_reviewed_games(user: User):
    reviewed_games = []
    reviews = user.reviews
    for review in user.reviews:
        reviewed_games.append(review.game)
    return reviewed_games


def get_number_of_pages(games_per_page, super_list):
    return math.ceil(len(super_list) / games_per_page)


def get_bio(user: User):
    return user.bio


def update_bio(new_bio, user: User, repo: AbstractRepository):
    repo.change_bio(user, new_bio)
