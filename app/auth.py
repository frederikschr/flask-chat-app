from flask import Blueprint, render_template, flash, url_for, redirect, session
from flask_login import login_user, logout_user, current_user, login_required
from .wtform_fields import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from app import app

auth = Blueprint("auth", __name__)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if not current_user.is_authenticated:
        reg_form = RegistrationForm()

        if reg_form.validate_on_submit():
            username = reg_form.username.data
            email = reg_form.email.data
            password = reg_form.password.data

            hashed_pswd = generate_password_hash(password, method="sha256")

            user = User(username=username, email=email, password=hashed_pswd)

            db.session.add(user)
            db.session.commit()

            flash("Registration was successful", category="success")
            return redirect(url_for("auth.login"))

        else:
            for error in reg_form.errors.values():
                flash(error[0], category="error")

        return render_template("sign-up.html", form=reg_form, user=current_user)

    else:
        logout_user()
        return redirect(url_for("views.index"))

@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Logged in successfully", category="success")
                session["current_room"] = "Lobby"
                return redirect(url_for("views.chat"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash(f"No user named {username}", category="error")

    return render_template("login.html", form=login_form, user=current_user)

@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", category="success")
    return redirect(url_for("views.index"))

@app.login_manager.unauthorized_handler
def unauth_handler():
    return redirect(url_for("views.index"))







