from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Float,
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import (
    Publisher,
    Game,
    User,
    Review,
    Wishlist,
    Genre,
)

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("user_name", String(255), primary_key=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("bio", String(255), nullable=True),
)

publishers_table = Table(
    "publishers",
    metadata,
    Column("publisher_name", String(255), primary_key=True, nullable=False),
)

genres_table = Table(
    "genres",
    metadata,
    Column("genre_name", String(255), primary_key=True, nullable=False),
)

games_table = Table(
    "games",
    metadata,
    Column("game_id", Integer, primary_key=True),
    Column("game_title", Text, nullable=False),
    Column("game_price", Float, nullable=False),
    Column("release_date", String(50), nullable=False),
    Column("game_description", String(255), nullable=True),
    Column("game_image_url", String(255), nullable=True),
    Column("game_website_url", String(255), nullable=True),
    Column("publisher_name", ForeignKey("publishers.publisher_name")),
)


reviews_table = Table(
    "reviews",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_name", ForeignKey("users.user_name")),
    Column("game_id", ForeignKey("games.game_id")),
    Column("rating", Integer, nullable=False),
    Column("comment", String, nullable=False),
)

games_genre_table = Table(
    "game_genres",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("game_id", ForeignKey("games.game_id")),
    Column("genre_name", ForeignKey("genres.genre_name")),
)

wishlist_table = Table(
    "wishlist",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("users.user_name")),
)

wishlist_game_table = Table(
    "game_wishlist",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("wishlist_id", ForeignKey("wishlist.id")),
    Column("game_id", ForeignKey("games.game_id")),
)

user_favouritesgames_table = Table(
    "user_favourites",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("users.user_name")),
    Column("game_id", ForeignKey("games.game_id")),
)


def map_model_to_tables():
    mapper(
        Publisher,
        publishers_table,
        properties={
            "_Publisher__publisher_name": publishers_table.c.publisher_name,
        },
    )

    mapper(
        Game,
        games_table,
        properties={
            "_Game__game_id": games_table.c.game_id,
            "_Game__game_title": games_table.c.game_title,
            "_Game__price": games_table.c.game_price,
            "_Game__release_date": games_table.c.release_date,
            "_Game__description": games_table.c.game_description,
            "_Game__image_url": games_table.c.game_image_url,
            "_Game__website_url": games_table.c.game_website_url,
            "_Game__publisher": relationship(Publisher),
            "_Game__genres": relationship(Genre, secondary=games_genre_table),
            "_Game__reviews": relationship(
                Review, back_populates="_Review__game"
            ),
        },
    )

    mapper(
        Genre,
        genres_table,
        properties={
            "_Genre__genre_name": genres_table.c.genre_name,
        },
    )

    mapper(
        Review,
        reviews_table,
        properties={
            "_Review__user": relationship(
                User, back_populates="_User__reviews"
            ),
            "_Review__game": relationship(
                Game, back_populates="_Game__reviews"
            ),
            "_Review__rating": reviews_table.c.rating,
            "_Review__comment": reviews_table.c.comment,
        },
    )

    mapper(
        Wishlist,
        wishlist_table,
        properties={
            "_Wishlist__user": relationship(
                User, back_populates="_User__wishlist"
            ),
            "_Wishlist__list_of_games": relationship(
                Game, secondary=wishlist_game_table
            ),
        },
    )

    mapper(
        User,
        users_table,
        properties={
            "_User__username": users_table.c.user_name,
            "_User__password": users_table.c.password,
            "_User__bio": users_table.c.bio,
            "_User__reviews": relationship(
                Review, back_populates="_Review__user"
            ),
            "_User__favourite_games": relationship(
                Game,
                secondary=user_favouritesgames_table,
            ),
            "_User__wishlist": relationship(
                Wishlist, back_populates="_Wishlist__user", uselist=False
            ),
        },
    )
