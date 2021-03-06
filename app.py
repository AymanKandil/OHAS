from flask import Flask, render_template, redirect, send_from_directory
from flask_login import LoginManager
import os

from modules.Auth.auth import auth, UserDatabase
from modules.DashboardAdmin.dashboard import dashboard
from models import User, Anonymous
from modules.DiseaseTable.diseasetable import diseasetable
from modules.Profile.profile import profile
from modules.Forums.medforums import medforums
from modules.UserPortal.userportal import userportal


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, template_folder="./templates", static_folder="./static")

app.config["USERS_DB"] = os.path.join(
    app.root_path, "data", "databases", "users.db"
)


app.config['SECRET_KEY'] = b"\xb85\xf9\x15\xdcO'\x80\xa9\xf9\x19\xd9\x9d\xb7\xfe"
app.config['UPLOAD_FOLDER'] = './'
app.config["DEBUG"] = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(username):
    db = UserDatabase(app.config["USERS_DB"])
    user = db.check_user_username(username)
    if user:
        user = User(user[0])
        return user
    return None


app.register_blueprint(auth)
app.register_blueprint(dashboard, url_prefix="/dashboard")
app.register_blueprint(diseasetable, url_prefix="/diseasetable")
app.register_blueprint(profile, url_prefix="/user")
app.register_blueprint(medforums, url_prefix="/medforums")
#app.register_blueprint(user,url_prefix="/ManageUser")
app.register_blueprint(userportal,url_prefix="/userportal")


@app.login_manager.unauthorized_handler
def unauth_handler():
    return redirect("/login")


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template(
#             '404.html', title='404', message='Path not found'
#         ), 404


@app.route('/media/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config["MEDIA_PATH"], filename)


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/medicalblogs")
# def medicalblogs():
#     return render_template("blogsforums.html")

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')


if __name__ == "__main__":
    app.run(host='', debug=app.config['DEBUG'])
