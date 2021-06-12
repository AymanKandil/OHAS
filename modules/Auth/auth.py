from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import re
import os
from modules.Auth.user_db import UserDatabase
from models import User


auth = Blueprint(
    'auth', __name__
)


@auth.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    db = UserDatabase(current_app.config["USERS_DB"])
    user = db.check_user_username(username)

    if user:
        if check_password_hash(user[1], password):
            user = User(user[0])
            login_user(user)
            print(f"Successful login {user.username}")
            return redirect("/")
    print("Incorrect username or password", "error")
    return redirect(url_for("auth.login"))


@auth.route("/UserRegister", methods=["POST", "GET"])
def user_register():
    if request.method == "GET":
        return render_template("signup.html")

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    age = request.form.get("age")
    gender = request.form.get("gender")
    chronic = request.form.get("chronic")
    confirm_password = request.form.get("confirm_password")

    if "file" not in request.files:
        return "request does not have file", 409

    shared_file = request.files["file"]

    if shared_file.filename == "":
        return "request does not have file", 409

    if not re.match(
        "^.*\.(doc|DOC|docx|DOCX|txt|TXT|pdf|PDF)$", shared_file.filename
    ):
        return "invalid file type", 409

    filename = secure_filename(shared_file.filename)

    if shared_file and filename:
        shared_file.save(
            os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        )

    db = UserDatabase(current_app.config["USERS_DB"])

    # Validate username
    if not re.match("^[a-zA-z0-9]{2,10}$", username):
        print("Invalid username.", "error")
        return redirect(url_for("auth.user_register"))

    # Valid password
    if not (password_check(password).get("password_ok", False)):
        flash("Your password is not strong enough, make sure it meets"
              "the following requirements:", "error")
        flash("8 or more characters", "error")
        flash("1 or more lowercase letters", "error")
        flash("1 or more uppercase letters", "error")
        flash("1 or more special characters", "error")
        flash("1 or more digits", "error")
        return redirect(url_for("auth.user_register"))
    if confirm_password != password:
        print("Passwords do not match", "error")
        return redirect(url_for("auth.user_register"))

    user = db.check_user(username)

    # Check if user exists
    if user:
        print("Username already taken", "error")
        return redirect(url_for("auth.user_register"))

    # Register user
    print(username, first_name, last_name, email)
    db.insert_patient(
        username, first_name, last_name, email,
        generate_password_hash(password, method="sha256"), gender,
        age, chronic, filename
    )
    print("You were successfully registered, please log in", "success")
    return redirect(url_for("auth.login"))


@auth.route("/DocRegister", methods=["POST", "GET"])
def doc_register():
    if request.method == "GET":
        return render_template("docsignup.html")

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    gender = request.form.get("gender")
    age = request.form.get("age")
    prev_work = request.form.get("prev_work")
    medical_pos= request.form.get("med_pos")
    confirm_password = request.form.get("confirm_password")

    if "file" not in request.files:
        return "request does not have file", 409

    shared_file = request.files["file"]

    if shared_file.filename == "":
        return "request does not have file", 409

    if not re.match(
        "^.*\.(doc|DOC|docx|DOCX|txt|TXT|pdf|PDF)$", shared_file.filename
    ):
        return "invalid file type", 409

    filename = secure_filename(shared_file.filename)

    if shared_file and filename:
        shared_file.save(
            os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        )

    db = UserDatabase(current_app.config["USERS_DB"])

    # Validate username
    if not re.match("^[a-zA-z0-9]{2,10}$", username):
        print("Inavlid username.", "error")
        return redirect(url_for("auth.doc_register"))

    # Valid password
    if not (password_check(password).get("password_ok", False)):
        flash("Your password is not strong enough, make sure it meets"
              "the following requirements:", "error")
        flash("8 or more characters", "error")
        flash("1 or more lowercase letters", "error")
        flash("1 or more uppercase letters", "error")
        flash("1 or more special characters", "error")
        flash("1 or more digits", "error")
        return redirect(url_for("auth.doc_register"))
    if confirm_password != password:
        print("Passwords do not match", "error")
        return redirect(url_for("auth.doc_register"))

    user = db.check_user(username)

    # Check if user exists
    if user:
        print("Username already taken", "error")
        return redirect(url_for("auth.doc_register"))

    # Register user
    print(username, first_name, last_name, email)
    db.insert_doctor(
        username, first_name, last_name, email,
        generate_password_hash(password, method="sha256"), gender,
        age, prev_work, medical_pos, filename
    )
    print("You were successfully registered, please log in", "success")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def password_check(password):
    """
    Source: https://stackoverflow.com/a/32542964/6340707
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(
        r"[ ?@!#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password
    ) is None

    # overall result
    password_ok = not (
        length_error or digit_error or uppercase_error or
        lowercase_error or symbol_error
    )

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }
