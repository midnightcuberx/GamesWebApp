from flask import Blueprint, render_template, request
from games import Genre
from games.domainmodel.model import Publisher
import games.adapters.repository as repo
import games.search.services as services
import games.utilities.utilities as utilities

search_blueprint = Blueprint("search_bp", __name__)


@search_blueprint.route("")
def search():
    utilities.check_valid_session(repo.repo_instance)
    
    games_list = services.get_all_games(repo.repo_instance)
    genres = services.get_all_genres(repo.repo_instance)
    publishers = services.get_all_publishers(repo.repo_instance)
    username = utilities.get_username()
    return render_template("search.html", games_list=games_list, dataset_of_genres=genres, dataset_of_publishers=publishers, page=0, total_pages=0, username=username)


@search_blueprint.route("/search", methods=["GET"])
def perform_search():
    utilities.check_valid_session(repo.repo_instance)
    
    search_query = request.args.get("query", "").lower()
    selected_genre = Genre(request.args.get("genre", ""))
    selected_publisher = Publisher(request.args.get("publisher", ""))
    matching_games = services.search_games(search_query, selected_genre, selected_publisher, repo.repo_instance)

    page = request.args.get("page", type=int, default=1)
    results_on_current_page = services.get_results_for_page(matching_games, page, 20)
    total_pages = services.get_total_pages(matching_games, 20)

    username = utilities.get_username()

    genres = services.get_all_genres(repo.repo_instance)
    publishers = services.get_all_publishers(repo.repo_instance)
    return render_template("search.html", games=results_on_current_page, dataset_of_publishers=publishers, dataset_of_genres=genres, page=page, total_pages=total_pages, username=username)
