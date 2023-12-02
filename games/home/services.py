from games.adapters.repository import AbstractRepository


def get_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_sorted_games(method, repo: AbstractRepository):
    return repo.get_sorted_dataset(method)
