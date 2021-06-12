from flask import Blueprint, render_template, current_app, redirect, url_for
from flask.globals import request
from flask_login import login_required

from models import requires_access_level, ACCESS
from modules.Auth.user_db import UserDatabase


dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/")
@login_required
@requires_access_level([1])
def dashboard_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    users = db.get_users()
    users_sorted = {}
    for user in users:
        current_user= {}
        current_user["id"] = user[0]
        current_user["name"] = user[1]
        current_user["role"]= user[8]
        users_sorted[user[1]] = current_user
        
    
    access = {v: k for k, v in ACCESS.items()}
    
    return render_template("adminportal.html", users=users_sorted, access=access)


@dashboard.route("/role/<username>/update", methods=["POST"])
@login_required
@requires_access_level([1])
def role_update_post(username):
    db = UserDatabase(current_app.config["USERS_DB"])

    # validate access
    access = request.form.get("roleChange")
    try:
        access = int(access)
    except ValueError:
        print("Invalid access value")
    access_model = {v: k for k, v in ACCESS.items()}
    if not access_model.get(access):
        print("Invalid access value")

    print(username, access)
    db.update_role(username, access)
    return redirect(url_for("dashboard.dashboard_view"))

@dashboard.route("/removeS", methods=["POST", "GET"])
@login_required
@requires_access_level([1])
def remove_user_post():
    db = UserDatabase(current_app.config["USERS_DB"])
    nm=request.form.get('n')
    db.remove_user(nm)
    return redirect(url_for("dashboard.dashboard_view"))
