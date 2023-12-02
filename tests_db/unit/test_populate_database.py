from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'game_wishlist', 'games', 'genres', 'publishers',
                                           'reviews', 'user_favourites', 'users', 'wishlist']

def test_database_populate_select_genres(database_engine):

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["genres"]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert all_genre_names == ['Action']

def test_database_populate_select_all_users(database_engine):

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["users"]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['FirsttestUser1', 'SecondtestUser2', 'ThirdtestUser3', 'WagatestUser4', 'babagatestUser5']

def test_database_populate_games(database_engine):

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["games"]])
        result = connection.execute(select_statement)

        all_game_names = []
        for row in result:
            all_game_names.append(row['game_title'])

        assert all_game_names == ['Call of Duty® 4: Modern Warfare®', 'The Stalin Subway: Red Veil', 'EARTH DEFENSE FORCE 4.1 The Shadow of New Despair', "Bartlow's Dread Machine"]

def test_database_populate_publishers(database_engine):

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["publishers"]])
        result = connection.execute(select_statement)

        all_publisher_names = []
        for row in result:
            all_publisher_names.append(row['publisher_name'])

        assert all_publisher_names == ['Beep Games, Inc.', 'Activision', 'D3PUBLISHER', 'Buka Entertainment']



def test_database_populate_reviews(database_engine):

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["reviews"]])
        result = connection.execute(select_statement)

        all_user_reviews = []
        for row in result:
            all_user_reviews.append(row['user_name'])

        assert all_user_reviews == ['FirsttestUser1', 'SecondtestUser2', 'ThirdtestUser3', 'WagatestUser4', 'babagatestUser5']

def test_database_populate_game_genres(database_engine):

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables["game_genres"]])
        result = connection.execute(select_statement)

        all_game_id = []
        all_genre_name = []
        for row in result:
            all_game_id.append(row['game_id'])
            all_genre_name.append(row['genre_name'])

        assert all_game_id == [1228870, 7940, 410320, 311120] and all_genre_name == ['Action', 'Action', 'Action', 'Action']
