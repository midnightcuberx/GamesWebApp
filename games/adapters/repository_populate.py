from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Genre, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader, ReviewCSVReader, UserCSVReader

def load_reviews(repo, csv_path: str):
    reviews_filename = csv_path + "reviews.csv"
    reviews = ReviewCSVReader.load_reviews(reviews_filename)
    for values in reviews:
        user_username = values[0]
        game_title = values[1]

        user = repo.get_user(user_username.username)
        game = repo.get_game(game_title)

        reviewed = Review(user, game, values[2], values[3])
        repo.add_review(reviewed)
        user.add_review(reviewed)
        game.add_review(reviewed)


def load_users(repo, csv_path: str):
    users_filename = csv_path + "users.csv"
    users = UserCSVReader.load_users(users_filename)
    for user in users:
        repo.add_user(user)


def populate(repo: AbstractRepository, csv_path: str):
    reader = GameFileCSVReader(csv_path + "games.csv")

    reader.read_csv_file()
    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)
    load_users(repo, csv_path)
    load_reviews(repo, csv_path)

