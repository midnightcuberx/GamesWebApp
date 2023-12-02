import games.adapters.repository as repo
import games.genres.services as services
import games.utilities.utilities as utilities

from flask import Blueprint, render_template, request, abort
from games.domainmodel.model import Genre


genre_blueprint = Blueprint("genres_bp", __name__)

num = None
method = None


@genre_blueprint.route("/<name>", methods=["GET"])  # , "POST"])
def genre_games(name):
    utilities.check_valid_session(repo.repo_instance)
    
    global num
    global method

    games_per_page = request.args.get("num")
    sort_method = request.args.get("method")

    if games_per_page is not None:
        num = int(games_per_page)
    if num is None:
        num = 20

    if sort_method is not None:
        method = sort_method
    if method is None:
        method = "name"

    dataset_of_genres = services.get_genres(repo.repo_instance)
    sorted_list = services.get_sorted_games(method, name, repo.repo_instance)
    if sorted_list == []:
        abort(404)
    genre_list = services.get_sublist(sorted_list, num, repo.repo_instance)
    length = len(genre_list)

    username = utilities.get_username()

    page = request.args.get("page", type=int, default=1)
    if not page:
        page = 1

    return render_template(
        "genres.html", dataset_of_genres=dataset_of_genres, genre=Genre(name), games=genre_list[page - 1], page=page, last=length, sort_type=method, games_per_page=num, username=username
    )
