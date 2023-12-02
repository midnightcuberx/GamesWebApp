import abc
from typing import List

from games.domainmodel.model import Game, User, Genre, Review, Wishlist


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f"RepositoryException: {message}")


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_review(self, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_wishlist(self, user: User, game: Game):
        raise NotImplementedError
    
    @abc.abstractmethod
    def remove_from_wishlist(self, user: User, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_favourites(self, user: User, game: Game):
        raise NotImplementedError
    
    @abc.abstractmethod
    def remove_from_favourites(self, user: User, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def change_bio(self, user: User, bio: str):
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_sublist(self, super_list, l):
        raise NotImplementedError

    @abc.abstractmethod
    def get_sorted_dataset(self, sort_mode, l) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_sorted_reviews_for_game(self, game: Game, sort_option: str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, u: str) -> User:
        raise NotImplementedError
