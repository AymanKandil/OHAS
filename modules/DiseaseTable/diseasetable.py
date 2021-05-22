from flask import Blueprint, render_template
from flask_login import login_required

diseasetable = Blueprint(
    'diseasetable', __name__
)

@diseasetable.route("/")
@login_required
@requires_access_level([2])
def diseasetable_view():
    return render_template("diseaseslist.html")

@diseasetable.route("/admintable")
@login_required
@requires_access_level([3, 1])
def admin_diseasetable_view():
    return render_template("docdiseaselist.html")