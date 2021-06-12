from flask import Blueprint, render_template, current_app, abort
from flask_login import current_user

from modules.Auth.user_db import UserDatabase
from models import ACCESS

profile = Blueprint(
    'profile', __name__
)


@profile.route("/<username>")
def docprofile_view(username):
    try:
        access = current_user.access
    except Exception:
        access = 4

    db = UserDatabase(current_app.config["USERS_DB"])
    user = db.check_user_username(username)
    if not user:
        abort(404)

    if user[-1] == ACCESS.get("doctor"):
        doctor = db.check_doctor(username)
        data = {
            "doctor": doctor,
            "initials": get_initials(doctor)
        }
        return render_template("docprofile.html", **data)
    elif user[-1] == ACCESS.get("user"):
        if access == 3 or access == 1:
            patient = db.check_patient(username)
            data = {
                "patient": patient,
                "initials": get_initials(patient)
            }
            return render_template("user-profile.html", **data)

    abort(404)


def get_initials(user):
    initials = ""
    if user[1]:
        initials += user[1][0].upper()
    if user[2]:
        initials += user[2][0].upper()
    return initials
