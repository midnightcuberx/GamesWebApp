import csv
import os
import math


# from bisect import bisect, bisect_left, insort_left
from typing import List
from datetime import datetime

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, User, Genre, Review, Wishlist
from games.adapters.datareader.csvdatareader import (
    GameFileCSVReader,
    ReviewCSVReader,
    UserCSVReader,
)


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = []
        self.__publishers = set()
        self.__genres = set()
        self.__games_by_genre = {}
        self.__users = []

    def add_game(self, game: Game):
        if isinstance(game, Game):
            self.__games.append(game)
            for genre in game.genres:
                if genre not in self.__genres:
                    self.__genres.add(genre)
                    self.__games_by_genre[genre.genre_name] = []
                self.__games_by_genre[genre.genre_name].append(game)
            self.__publishers.add(game.publisher)

    def add_review(self, review: Review):
        if isinstance(review, Review):
            review.user.add_review(review)
            review.game.add_review(review)

    def add_to_wishlist(self, user: User, game: Game):
        user.wishlist.add_game(game)
    
    def remove_from_wishlist(self, user: User, game: Game):
        user.wishlist.remove_game(game)

    def add_to_favourites(self, user: User, game: Game):
        user.add_favourite_game(game)
    
    def remove_from_favourites(self, user: User, game: Game):
        user.remove_favourite_game(game)

    def change_bio(self, user: User, bio: str):
        user.set_bio(bio)

    def get_games(self) -> List[Game]:
        return sorted(self.__games, key=lambda x: x.title)

    def get_number_of_games(self):
        return len(self.__games)

    def get_genres(self):
        return sorted(self.__genres, key=lambda x: x.genre_name)

    def get_publishers(self):
        return sorted(self.__publishers, key=lambda x: x.publisher_name)

    def get_games_by_genre(self, genre):
        return sorted(self.__games_by_genre[genre], key=lambda x: x.title)

    def get_sublist(self, super_list, l=10):
        return [
            super_list[i * l : (i + 1) * l]
            for i in range(math.ceil(len(super_list) / l))
        ]

    def get_sorted_dataset(self, sort_mode="name", l=None) -> list:
        if l is None:
            l = self.__games
        # returns list of game objects sorted based on parameter sort_mode
        if sort_mode == "name":
            return sorted(l, key=lambda x: x.title)
        elif sort_mode == "date":
            return sorted(
                l,
                key=lambda x: datetime.strptime(x.release_date, "%b %d, %Y"),
                reverse=False,
            )
        elif sort_mode == "latest":
            return sorted(
                l,
                key=lambda x: datetime.strptime(x.release_date, "%b %d, %Y"),
                reverse=True,
            )
        elif sort_mode == "price":
            return sorted(l, key=lambda x: x.price)

        return sorted(l, key=lambda x: x.title)

    def get_sorted_reviews_for_game(self, game: Game, sort_option: str):
        if sort_option == "comment_length-ascend":
            return sorted(game.reviews, key=lambda review: len(review.comment))
        elif sort_option == "star_ratings-descend":
            return sorted(
                game.reviews, key=lambda review: review.rating, reverse=True
            )
        if sort_option == "comment_length-descend":
            return sorted(
                game.reviews,
                key=lambda review: len(review.comment),
                reverse=True,
            )
        elif sort_option == "star_ratings-ascend":
            return sorted(game.reviews, key=lambda review: review.rating)
        else:
            return game.reviews

    def get_game(self, game_id) -> Game:
        index = self.__games.index(Game(int(game_id), ""))
        game = self.__games[index]
        return game

    def add_user(self, user: User):
        self.__users.append(user)

    def get_users(self) -> list:
        return self.__users

    def get_user(self, username: str) -> User:
        u = User(username, "abcdefghliasd")
        if u in self.__users:
            return self.__users[self.__users.index(u)]
        return None
