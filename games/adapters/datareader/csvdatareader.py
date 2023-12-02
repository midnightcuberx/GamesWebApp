import csv
import os
import math
from datetime import datetime

from games.domainmodel.model import Genre, Game, Publisher, Review, User


class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self._games_by_genre = {}
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()

    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]
                    game.image_url = row["Header image"]

                    publisher = Publisher(row["Publishers"])
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        if genre_name not in self._games_by_genre:
                            self._games_by_genre[genre_name] = []

                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)

                    self.__dataset_of_games.append(game)

                    for genre in game.genres:
                        self._games_by_genre[genre.genre_name].append(game)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    def get_sublist(self, super_list, l=10):
        return [super_list[i * l : (i + 1) * l] for i in range(math.ceil(len(super_list) / l))]

    @property
    def games_by_genre(self):
        for l in self._games_by_genre:
            self._games_by_genre[l].sort(key=lambda x: x.title)
        return self._games_by_genre

    @property
    def dataset_of_games(self, sort_mode="name") -> list:
        return sorted(self.__dataset_of_games, key=lambda x: x.title)

    @property
    def dataset_of_publishers(self) -> set:
        return sorted(self.__dataset_of_publishers, key=lambda x: x.publisher_name)

    @property
    def dataset_of_genres(self) -> set:
        return sorted(self.__dataset_of_genres, key=lambda x: x.genre_name)

    def get_sorted_dataset(self, sort_mode="name", l=None) -> list:
        if l is None:
            l = self.__dataset_of_games
        # returns list of game objects sorted based on parameter sort_mode
        if sort_mode == "name":
            return sorted(l, key=lambda x: x.title)
        elif sort_mode == "date":
            return sorted(l, key=lambda x: datetime.strptime(x.release_date, "%b %d, %Y"), reverse=False)
        elif sort_mode == "latest":
            return sorted(l, key=lambda x: datetime.strptime(x.release_date, "%b %d, %Y"), reverse=True)
        elif sort_mode == "price":
            return sorted(l, key=lambda x: x.price)

        return sorted(l, key=lambda x: x.title)


class ReviewCSVReader:
    @staticmethod
    def load_reviews(file_path):
        reviews = []

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:

                user = User(row['reviewer'], "Test1234")
                game_id = int(row["game-id"])
                rating = int(row["rating"])
                comment = str(row["comment"])

                review = [user, game_id, rating, comment]

                reviews.append(review)

        return reviews


class UserCSVReader:
    @staticmethod
    def load_users(file_path):
        users = []

        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                username = row["username"]
                password = row["password"]

                user = User(username, password)

                users.append(user)

        return users
