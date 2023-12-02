import games.adapters.repository as repo
import games.home.services as services
import games.utilities.utilities as utilities

from flask import Blueprint, render_template

home_blueprint = Blueprint("home_bp", __name__)


@home_blueprint.route("/")
def home():
    utilities.check_valid_session(repo.repo_instance)

    lastest_games = services.get_sorted_games("latest", repo.repo_instance)
    cheapest_games = services.get_sorted_games("price", repo.repo_instance)
    oldest_games = services.get_sorted_games("date", repo.repo_instance)

    section_dict = {"Featured games": lastest_games, "Free-to-play": cheapest_games, "Classic": oldest_games}

    username = utilities.get_username()

    return render_template("index.html", dataset_of_genres=services.get_genres(repo.repo_instance), username=username, section=section_dict, input_class="sliderCard")
