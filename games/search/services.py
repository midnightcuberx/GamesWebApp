from games.adapters.repository import AbstractRepository


def get_all_games(repo: AbstractRepository):
    return repo.get_games()


def get_all_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_all_publishers(repo: AbstractRepository):
    return repo.get_publishers()


def get_matching_games(query, selected_genre, selected_publisher, games):
    matching_games = []

    for game in games:
        if (query in game.title.lower() and (selected_genre.genre_name is None or selected_genre in game.genres)
                and (selected_publisher.publisher_name is None or selected_publisher == game.publisher)):
            matching_games.append(game)

    return matching_games


def get_total_pages(matching_games, amount):
    per_page = amount
    total_results = len(matching_games)
    total_pages = (total_results + per_page - 1) // per_page

    return total_pages


def search_games(query, selected_genre, selected_publisher, repo: AbstractRepository):
    all_games = repo.get_games()
    matching_games = get_matching_games(query, selected_genre, selected_publisher, all_games)

    return matching_games


def get_results_for_page(matching_games, page, amount):
    per_page = amount
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    results_on_current_page = matching_games[start_idx:end_idx]

    return results_on_current_page
