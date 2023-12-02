from flask import Blueprint, render_template, redirect, url_for, session, request
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm

# from flask_wtf.file import FileRequired, FileField, FileAllowed
from password_validator import PasswordValidator
from games.domainmodel.model import Game
from functools import wraps

# from PIL import Image
# import os

import games.utilities.utilities as utilities
import games.adapters.repository as repo
import games.authentication.services as services

auth_blueprint = Blueprint("auth_bp", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # utilities.check_valid_session(repo.repo_instance)

    form = LoginForm()
    username_error = None
    password_error = None

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data

            services.authenticate_user(username, password, repo.repo_instance)

            session.clear()
            session["username"] = username

            return redirect(url_for("home_bp.home"))

        except services.AuthenticationException:
            try:
                services.get_user(username, repo.repo_instance)
                password_error = "The specified password does not match the username!"
            except services.UnknownUserException:
                username_error = "This username is not registered!"

    # utilities.check_valid_session(repo.repo_instance)

    return render_template(
        "login.html",
        username=utilities.get_username(),
        # user=utilities.get_user(utilities.get_username(), repo.repo_instance),
        # link=None,
        text_type="Login",
        dataset_of_genres=utilities.get_all_genres(repo.repo_instance),
        form=form,
        username_error=username_error,
        password_error=password_error,
    )


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    # utilities.check_valid_session(repo.repo_instance)
    form = RegisterForm()
    username_error = None
    password_error = "Your password must be at least 8 characters, and contain an upper case letter, lower case letter and a digit"

    # doesnt run if password doesnt work. Could move password validating to here instead if we want to display both messages.
    if form.validate_on_submit():
        # print("no1")
        username = form.username.data
        password = form.password.data
        try:
            services.add_user(username, password, repo.repo_instance)
            return redirect(url_for("auth_bp.login"))
        except services.NameNotUniqueException:
            # print("no")
            username_error = "Your username is already taken - please try another one"

    return render_template(
        "login.html",
        text_type="Register",
        dataset_of_genres=utilities.get_all_genres(repo.repo_instance),
        username=utilities.get_username(),
        form=form,
        username_error=username_error,
        password_error=password_error,
    )


@auth_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("home_bp.home"))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "username" not in session:
            return redirect(url_for("auth_bp.login"))
        return view(**kwargs)

    return wrapped_view


"""@auth_blueprint.route("/update", methods=["GET", "POST"])
@login_required
def update():
    form = PhotoForm()
    username = utilities.get_username()
    # user = utilities.get_user(username, repo.repo_instance)

    if form.validate_on_submit():
        f = request.files["photo"]
        print(f)
        f.save(f"games/static/images/{username}.jpg")
        generate_pfp(f"games/static/images/{username}.jpg")
        # user.has_pfp = True

        return redirect(url_for("home_bp.home"))

    return render_template("upload.html", form=form, username=username)  # , #user=user, link=f"games/static/images/{username}.jpg")"""


"""def generate_pfp(image):
    # Opens a image in RGB mode
    im = Image.open(image, mode="r")

    new_height = 500
    new_width = new_height

    width = im.size[0]
    height = im.size[1]

    if width < new_width or height < new_height:
        while width < new_width or height < new_height:
            width *= 2
            height *= 2
    elif width > new_width and height > new_height:
        while width // 2 >= new_width and height // 2 >= new_height:
            width //= 2
            height //= 2

    im = im.resize((width, height))
    # im.show()

    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2

    im1 = im.crop((left, top, right, bottom))

    # im1.show()
    im1.save(image)"""


"""def login_required(view_function):
    # Arguments and keyword arguments from te view function
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("auth_bp.login"))
        # returns the function with the arguments and keyword arguments
        return view_function(*args, **kwargs)

    # return whatever was done in the above function
    return wrapper"""


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = "Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit"
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    username = StringField("Username", [DataRequired(message="Your username is required")], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [DataRequired(message="Your password is required"), PasswordValid("Your password is invalid")], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(message="Your username is required")], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [DataRequired(message="Your password is required")], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


"""class PhotoForm(FlaskForm):
    photo = FileField("Select a file", validators=[FileRequired(), FileAllowed(["jpg", "png"])])
    submit = SubmitField("Submit")"""
