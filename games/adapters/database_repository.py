import math

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from typing import List
from datetime import datetime

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Genre, Review, Publisher


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # self.__games = []
    # self.__publishers = set()
    # self.__genres = set()
    # self.__games_by_genre = {}
    # self.__users = []

    def add_game(self, game: Game):
        if isinstance(game, Game):
            with self._session_cm as scm:
                for genre in game.genres:
                    if genre not in self.get_genres():
                        scm.session.merge(genre)
                if game.publisher not in self.get_publishers():
                    scm.session.merge(game.publisher)
                scm.session.merge(game)
                scm.commit()

    def add_review(self, new_review: Review):
        if isinstance(new_review, Review):
            with self._session_cm as scm:
                scm.session.merge(new_review)
                scm.commit()

    def add_to_wishlist(self, user: User, game: Game):
        user.wishlist.add_game(game)
        with self._session_cm as scm:
            scm.session.merge(user.wishlist)
            scm.commit()
    
    def remove_from_wishlist(self, user: User, game: Game):
        user.wishlist.remove_game(game)
        with self._session_cm as scm:
            scm.session.merge(user.wishlist)
            scm.commit()

    def add_to_favourites(self, user: User, game: Game):
        user.add_favourite_game(game)
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()
    
    def remove_from_favourites(self, user: User, game: Game):
        user.remove_favourite_game(game)
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def change_bio(self, user: User, bio: str):
        user.set_bio(bio)
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_games(self) -> List[Game]:
        return (
            self._session_cm.session.query(Game)
            .order_by(Game._Game__game_title)
            .all()
        )

    def get_number_of_games(self):
        return self._session_cm.session.query(Game).count()

    def get_genres(self):
        return (
            self._session_cm.session.query(Genre)
            .order_by(Genre._Genre__genre_name)
            .all()
        )

    def get_publishers(self):
        return (
            self._session_cm.session.query(Publisher)
            .order_by(Publisher._Publisher__publisher_name)
            .all()
        )

    def get_games_by_genre(self, genre):
        result = None
        games_with_genre = (
            self._session_cm.session.query(Game)
            .filter(Game._Game__genres.contains(Genre(genre)))
            .order_by(Game._Game__game_title)
            .all()
        )

        if games_with_genre is not None:
            result = games_with_genre

        return result

    def get_sublist(self, super_list, l):
        return [
            super_list[i * l : (i + 1) * l]
            for i in range(math.ceil(len(super_list) / l))
        ]

    def get_sorted_dataset(self, sort_mode="name", l=None) -> list:
        if l is None:
            l = self.get_games()
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

    def get_sorted_reviews_for_game(self, game: Game, sort_option: str) -> list:
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
        try:
            game = (
                self._session_cm.session.query(Game)
                .filter(Game._Game__game_id == game_id)
                .one()
            )
            return game
        except NoResultFound:
            return None

    def add_user(self, user: User):
        if isinstance(user, User):
            with self._session_cm as scm:
                scm.session.merge(user)
                scm.commit()

    def get_users(self) -> list:
        return self._session_cm.session.query(User).all()

    def get_user(self, u: str) -> User:
        result = None

        user = (
            self._session_cm.session.query(User)
            .filter(User._User__username == u)
            .first()
        )

        if user is not None:
            result = user

        return result
