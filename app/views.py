from flask import Blueprint, render_template, request, flash, redirect
from flask_login import current_user

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)

@views.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("chat.html", user=current_user)





