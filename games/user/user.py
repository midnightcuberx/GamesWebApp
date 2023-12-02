from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
)

from games.authentication.authentication import login_required
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    NumberRange,
)

import games.utilities.utilities as utilities
import games.adapters.repository as repo
import games.user.services as services

user_blueprint = Blueprint("user_bp", __name__)


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = "Field must not contain profanity"
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class BioForm(FlaskForm):
    bio_description = TextAreaField(
        "Bio",
        [
            DataRequired(),
            ProfanityFree(message="Your bio must not contain profanity"),
        ],
    )
    # game_id = HiddenField("Game id")
    submit = SubmitField("Submit")


@user_blueprint.route("/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    utilities.check_valid_session(repo.repo_instance)

    user = utilities.get_user(username, repo.repo_instance)
    if user == None:
        return redirect(url_for("auth_bp.login"))
    if username != session["username"]:
        return redirect(url_for("auth_bp.login"))
    games_in_wishlist = services.get_wishlist(user)[:5]

    games_in_favourites = services.get_favourite_games(user)[:5]

    games_reviewed = services.get_reviewed_games(user)[:5]

    user_bio = services.get_bio(user)

    return render_template(
        "user.html",
        dataset_of_genres=utilities.get_all_genres(repo.repo_instance),
        username=utilities.get_username(),
        wishlist_list=games_in_wishlist,
        favourites_list=games_in_favourites,
        reviews_list=games_reviewed,
        user_bio=user_bio,
    )


@user_blueprint.route("/update_bio/<username>", methods=["GET", "POST"])
@login_required
def update_bio(username):
    utilities.check_valid_session(repo.repo_instance)

    user = utilities.get_user(username, repo.repo_instance)
    if user == None:
        return redirect(url_for("auth_bp.login"))
    games_in_wishlist = services.get_wishlist(user)[:5]

    games_in_favourites = services.get_favourite_games(user)[:5]

    games_reviewed = services.get_reviewed_games(user)[:5]

    user_bio = services.get_bio(user)

    # edit profile

    form = BioForm()

    if form.validate_on_submit():
        bio_text = form.bio_description.data
        services.update_bio(bio_text, user, repo.repo_instance)
        return redirect(url_for("user_bp.user", username=username))

    return render_template(
        "user_bio.html",
        dataset_of_genres=utilities.get_all_genres(repo.repo_instance),
        username=utilities.get_username(),
        wishlist_list=games_in_wishlist,
        favourites_list=games_in_favourites,
        reviews_list=games_reviewed,
        form=form,
        user_bio=user_bio,
    )


games_per_page = None


@user_blueprint.route("/wishlist", methods=["GET"])
@login_required
def wishlist_page():
    utilities.check_valid_session(repo.repo_instance)
    username = utilities.get_username()

    games_per_page_data = request.args.get("numberSelect")

    global games_per_page

    if not games_per_page_data is None:
        games_per_page = int(games_per_page_data)
    if games_per_page is None:
        games_per_page = 12

    user = utilities.get_user(username, repo.repo_instance)
    if user == None:
        return redirect(url_for("auth_bp.login"))

    # None is placeholder for the add button

    games_in_wishlist = [None] + services.get_wishlist(user)

    sublist = utilities.get_sublist(
        games_in_wishlist, games_per_page, repo.repo_instance
    )

    number_of_pages = services.get_number_of_pages(
        games_per_page, games_in_wishlist
    )

    current_page = request.args.get("page", type=int, default=1)
    if not current_page:
        current_page = 1

    return render_template(
        "game_profile_list.html",
        dataset_of_genres=utilities.get_all_genres(repo.repo_instance),
        page=current_page,
        last=number_of_pages,
        divided_list=sublist,
        games_per_page=games_per_page,
        username=username,
        which_list="wishlist",
    )


@user_blueprint.route("/favourites", methods=["GET"])
@login_required
def favourites_page():
    utilities.check_valid_session(repo.repo_instance)
    username = utilities.get_username()

    games_per_page_data = request.args.get("numberSelect")

    global games_per_page

    if not games_per_page_data is None:
        games_per_page = int(games_per_page_data)
    if games_per_page is None:
        games_per_page = 12

    user = utilities.get_user(username, repo.repo_instance)
    if user == None:
        return redirect(url_for("auth_bp.login"))

    # None is placeholder for the add button

    games_in_favourites = [None] + services.get_favourite_games(user)

    sublist = utilities.get_sublist(
        games_in_favourites, games_per_page, repo.repo_instance
    )

    number_of_pages = services.get_number_of_pages(
        games_per_page, games_in_favourites
    )

    current_page = request.args.get("page", type=int, default=1)
    if not current_page:
        current_page = 1

    return render_template(
        "game_profile_list.html",
        dataset_of_genres=utilities.get_all_genres(repo.repo_instance),
        page=current_page,
        last=number_of_pages,
        divided_list=sublist,
        games_per_page=games_per_page,
        username=username,
    )


@user_blueprint.route("/removefromwishlist/<game_id>", methods=["GET", "POST"])
@login_required
def remove_from_wishlist(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    utilities.remove_from_wishlist(current_user, game, repo.repo_instance)

    return redirect(url_for("user_bp.user", username=username))


@user_blueprint.route(
    "/wishlist/removefromwishlist/<game_id>", methods=["GET", "POST"]
)
@login_required
def remove_from_wishlist_page(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    utilities.remove_from_wishlist(current_user, game, repo.repo_instance)

    return redirect(url_for("user_bp.wishlist_page"))


@user_blueprint.route(
    "/removefromfavourites/<game_id>", methods=["GET", "POST"]
)
@login_required
def remove_from_favourites(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    utilities.remove_from_favourites(current_user, game, repo.repo_instance)

    return redirect(url_for("user_bp.user", username=username))


@user_blueprint.route(
    "favourites/removefromfavourites/<game_id>", methods=["GET", "POST"]
)
@login_required
def remove_from_favourites_page(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    utilities.remove_from_favourites(current_user, game, repo.repo_instance)

    return redirect(url_for("user_bp.favourites_page", username=username))
