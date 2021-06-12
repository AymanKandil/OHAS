from flask import Blueprint, render_template, current_app, redirect, url_for
from flask.globals import request
from flask_login import login_required

from models import requires_access_level, ACCESS
from modules.Auth.user_db import UserDatabase


userportal = Blueprint('userportal', __name__)


@userportal.route("/")
@login_required
@requires_access_level([2])
def userportal_dashboard_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    docdata=db.get_docusers()
    data={docdata}

    return render_template("userportal.html", doctordata=data)
