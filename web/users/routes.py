from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from web import db, bcrypt
from web.models import User, Post
from web.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from web.users.utils import save_picture, send_reset_email
from web.users.utils import top_contributions

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Your Account has been created! You can now proceed to Log In!",
            category="success",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "register.html",
        form=form,
        title="Register",
        top_contributions=top_contributions(),
    )


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("main.home"))
        else:
            flash(
                "Login Attempt Unsuccessful! Please check Email and Password!",
                category="danger",
            )
    return render_template(
        "login.html", form=form, title="Log In", top_contributions=top_contributions()
    )


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(
            "Your Account Details have been successfully modified!", category="success"
        )
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html",
        title="Account",
        image_file=image_file,
        form=form,
        top_contributions=top_contributions(),
    )


@users.route("/user/<username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template(
        "user_posts.html", posts=posts, user=user, top_contributions=top_contributions()
    )


@users.route("/reset_password", methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email with instruction was sent to corresponding email.",
            category="info",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "reset_request.html",
        title="Reset Password",
        form=form,
        top_contributions=top_contributions(),
    )


@users.route("/reset_password/<token>", methods=["POST", "GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token!", category="warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(
            f"Your Password has been changed successfully! You can now proceed to Log In!",
            category="success",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "reset_token.html",
        title="Reset Password",
        form=form,
        top_contributions=top_contributions(),
    )
