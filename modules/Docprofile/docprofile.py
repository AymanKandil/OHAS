from flask import Blueprint, render_template
from flask_login import login_required

docprofile = Blueprint(
    'docprofile', __name__
)


@docprofile.route("/")
@login_required
@requires_access_level([3])
def docprofile_view():
    return render_template("docprofile.html")
