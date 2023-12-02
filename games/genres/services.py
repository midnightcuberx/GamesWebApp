from games.adapters.repository import AbstractRepository


def get_sorted_games(method, name, repo: AbstractRepository):
    games_by_genre = repo.get_games_by_genre(name)
    return repo.get_sorted_dataset(method, games_by_genre)


def get_sublist(super_list, length, repo: AbstractRepository):
    return repo.get_sublist(super_list, length)


def get_genres(repo: AbstractRepository):
    return repo.get_genres()
