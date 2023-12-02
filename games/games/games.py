import math
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    session,
    abort
)

from games.authentication.authentication import login_required
from games.domainmodel.model import Game, Review, User
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    NumberRange,
)

import games.search.services as search_services
import games.games.services as services
import games.utilities.utilities as utilities
import games.adapters.repository as repo
import games.authentication.services as auth_services

games_blueprint = Blueprint("games_bp", __name__)

sort_type = None
games_per_page = None


@games_blueprint.route("", methods=["GET"])
def games():
    utilities.check_valid_session(repo.repo_instance)

    global sort_type
    global games_per_page

    games_per_page_data = request.args.get("numberSelect")
    sort_type_data = request.args.get("sortSelect")

    if not sort_type_data is None:
        sort_type = sort_type_data
    if sort_type is None:
        sort_type = "name"

    if not games_per_page_data is None:
        games_per_page = int(games_per_page_data)
    if games_per_page is None:
        games_per_page = 12

    sorted_games = services.get_sorted_games(sort_type, repo.repo_instance)
    sublist = services.get_sublist(
        sorted_games, games_per_page, repo.repo_instance
    )
    dataset_of_genres = utilities.get_all_genres(repo.repo_instance)
    number_of_pages = services.get_number_of_pages(
        games_per_page, repo.repo_instance
    )

    username = utilities.get_username()

    current_page = request.args.get("page", type=int, default=1)
    if not current_page:
        current_page = 1

    return render_template(
        "games.html",
        dataset_of_genres=dataset_of_genres,
        page=current_page,
        last=number_of_pages,
        divided_list=sublist,
        sort_type=sort_type,
        games_per_page=games_per_page,
        username=username,
    )


@games_blueprint.route("/<game_id>")
def view_game(game_id):
    utilities.check_valid_session(repo.repo_instance)

    if game_id is not None:
        dataset_of_genres = utilities.get_all_genres(repo.repo_instance)
        dataset_of_games = utilities.get_all_games(repo.repo_instance)
        username = utilities.get_username()
        try:
            game = utilities.get_game(game_id, repo.repo_instance)

            if game is None:
                abort(404)

            genres_list = [g.genre_name for g in game.genres]

            if username is None:
                in_wishlist = False
                in_favourites = False
            else:
                user = utilities.get_user(username, repo.repo_instance)
                in_wishlist = services.in_wishlist(user, game)
                in_favourites = services.in_favourites(user, game)

            page = request.args.get("page", type=int, default=1)
            sort_option = request.args.get("sort_option", "")
            sorted_reviews = services.get_sorted_reviews(
                game, sort_option, repo.repo_instance
            )

            results_on_current_page = search_services.get_results_for_page(
                sorted_reviews, page, 3
            )
            total_pages = search_services.get_total_pages(sorted_reviews, 3)
            avg_rating = services.get_game_average_reviews(game)

            return render_template(
                "game_info.html",
                dataset_of_genres=dataset_of_genres,
                game=game,
                genres=", ".join(genres_list),
                username=username,
                in_wishlist=in_wishlist,
                in_favourites=in_favourites,
                reviews=results_on_current_page,
                page=page,
                total_pages=total_pages,
                avg_rating=avg_rating,
            )
        except ValueError:
            return redirect("")
    return redirect("")


@games_blueprint.route("/review/<game_id>", methods=["GET", "POST"])
@login_required
def review_game(game_id):
    utilities.check_valid_session(repo.repo_instance)

    username = utilities.get_username()

    game = utilities.get_game(game_id, repo.repo_instance)

    form = ReviewForm()
    current_user = utilities.get_user(username, repo.repo_instance)

    if form.validate_on_submit():
        comment_text = form.review_comment.data
        rating = form.rating.data
        for i in range(len(current_user.reviews)):
            if current_user.reviews[i].game == game:
                print("already reviewed")
                return redirect(
                    url_for("games_bp.view_game", game_id=game.game_id)
                )

        review = Review(current_user, game, rating, comment_text)
        services.add_review(review, repo.repo_instance)
        return redirect(url_for("games_bp.view_game", game_id=game.game_id))

    return render_template(
        "review.html", game=game, form=form, username=username
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = "Field must not contain profanity"
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review_comment = TextAreaField(
        "Comment",
        [
            DataRequired(),
            Length(min=4, message="Your comment is too short"),
            ProfanityFree(message="Your comment must not contain profanity"),
        ],
    )
    rating = IntegerField(
        "Rating (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
    game_id = HiddenField("Game id")
    submit = SubmitField("Submit")


@games_blueprint.route("/addtowishlist/<game_id>", methods=["GET", "POST"])
@login_required
def add_to_wishlist(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    services.add_to_wishlist(current_user, game, repo.repo_instance)

    return redirect(url_for("games_bp.view_game", game_id=game_id))


@games_blueprint.route("/addtofavourites/<game_id>", methods=["GET", "POST"])
@login_required
def add_to_favourites(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    services.add_to_favourites(current_user, game, repo.repo_instance)

    return redirect(url_for("games_bp.view_game", game_id=game_id))


@games_blueprint.route("/removefromwishlist/<game_id>", methods=["GET", "POST"])
@login_required
def remove_from_wishlist(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    utilities.remove_from_wishlist(current_user, game, repo.repo_instance)

    return redirect(url_for("games_bp.view_game", game_id=game_id))


@games_blueprint.route(
    "/removefromfavourites/<game_id>", methods=["GET", "POST"]
)
@login_required
def remove_from_favourites(game_id):
    username = utilities.get_username()
    current_user = utilities.get_user(username, repo.repo_instance)
    game = utilities.get_game(game_id, repo.repo_instance)

    utilities.remove_from_favourites(current_user, game, repo.repo_instance)

    return redirect(url_for("games_bp.view_game", game_id=game_id))
