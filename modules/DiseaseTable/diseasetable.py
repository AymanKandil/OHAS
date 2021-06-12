from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required, current_user
from modules.Auth.user_db import UserDatabase
import numpy as np
from itertools import chain, product
from models import requires_access_level

diseasetable = Blueprint(
    'diseasetable', __name__
)

@diseasetable.route("/")
@login_required
def diseasetable_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    vd_d=db.get_vd()
    bd_d=db.get_bd()
    wd_d=db.get_wd()
    fd_d=db.get_fd()
    return render_template("diseaseslist.html", vd_data=vd_d, bd_data=bd_d, wd_data=wd_d, fd_data=fd_d)

@diseasetable.route("/admintable")
@login_required
@requires_access_level([1,3])
def admin_diseasetable_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    vd_d=db.get_vd()
    bd_d=db.get_bd()
    wd_d=db.get_wd()
    fd_d=db.get_fd()
    return render_template("docdiseaselist.html", vd_data=vd_d, bd_data=bd_d, wd_data=wd_d, fd_data=fd_d)


@diseasetable.route("/adddiseasevd", methods=["POST"])
@login_required
@requires_access_level([1,3])
def add_disease_vd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #adding values for VD table
    diseasename_vd = request.form.get("disease-name-vd")
    cause_vd= request.form.get("cause-vd")
    body_affected_vd = request.form.get("parts-of-body-affected-vd")
    method_vd = request.form.get("method-of-spreading-vd")
    vaccination_vd = request.form.get("type-of-vaccination-vd")
    db.insert_vd(diseasename_vd, cause_vd, body_affected_vd, method_vd, vaccination_vd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/adddiseasebd", methods=["POST"])
@login_required
@requires_access_level([1,3])
def add_disease_bd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #adding values for bd table
    diseasename_bd = request.form.get("disease-name-bd")
    cause_bd= request.form.get("cause-bd")
    body_affected_bd = request.form.get("parts-of-body-affected-bd")
    method_bd = request.form.get("method-of-spreading-bd")
    vaccination_bd = request.form.get("type-of-vaccination-bd")
    db.insert_bd(diseasename_bd, cause_bd, body_affected_bd, method_bd, vaccination_bd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/adddiseasewd", methods=["POST"])
@login_required
@requires_access_level([1,3])
def add_disease_wd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #adding values for wd table
    diseasename_wd = request.form.get("disease-name-wd")
    path_wd= request.form.get("Pathogen-wd")
    mode_wd = request.form.get("mode-wd")
    symptoms_wd = request.form.get("symptoms-wd")
    treatment_wd = request.form.get("treatment-wd")
    db.insert_wd(diseasename_wd, path_wd, mode_wd, symptoms_wd, treatment_wd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/adddiseasefd", methods=["POST"])
@login_required
@requires_access_level([1,3])
def add_disease_fd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #adding values for fd table
    diseasename_fd = request.form.get("disease-name-fd")
    path_fd= request.form.get("Pathogen-fd")
    mode_fd = request.form.get("mode-fd")
    symptoms_fd = request.form.get("symptoms-fd")
    treatment_fd = request.form.get("treatment-fd")
    db.insert_fd(diseasename_fd, path_fd, mode_fd, symptoms_fd, treatment_fd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/updatediseasevd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def update_disease_vd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #update values for VD table
    new_diseasename_vd = request.form.get("new-disease-name-vd")
    new_cause_vd= request.form.get("new-cause-vd")
    new_body_affected_vd = request.form.get("new-parts-of-body-affected-vd")
    new_method_vd = request.form.get("new-method-of-spreading-vd")
    new_vaccination_vd = request.form.get("new-type-of-vaccination-vd")
    db.update_vd( new_cause_vd, new_body_affected_vd, new_method_vd, new_vaccination_vd, new_diseasename_vd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/updatediseasebd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def update_disease_bd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #update values for bd table
    new_diseasename_bd = request.form.get("new-disease-name-bd")
    new_cause_bd= request.form.get("new-cause-bd")
    new_body_affected_bd = request.form.get("new-parts-of-body-affected-bd")
    new_method_bd = request.form.get("new-method-of-spreading-bd")
    new_vaccination_bd = request.form.get("new-type-of-vaccination-bd")
    db.update_bd( new_cause_bd, new_body_affected_bd, new_method_bd, new_vaccination_bd, new_diseasename_bd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/updatediseasewd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def update_disease_wd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #update values for wd table
    new_diseasename_wd = request.form.get("new-disease-name-wd")
    new_path_wd= request.form.get("new-Pathogen-wd")
    new_mode_wd = request.form.get("new-mode-wd")
    new_symptoms_wd = request.form.get("new-symptoms-wd")
    new_treatment_wd = request.form.get("new-treatment-wd")
    db.update_wd( new_path_wd, new_mode_wd, new_symptoms_wd, new_treatment_wd, new_diseasename_wd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/updatediseasefd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def update_disease_fd():
    db = UserDatabase(current_app.config["USERS_DB"])

    #update values for fd table
    new_diseasename_fd = request.form.get("new-disease-name-fd")
    new_path_fd= request.form.get("new-Pathogen-fd")
    new_mode_fd = request.form.get("new-mode-fd")
    new_symptoms_fd = request.form.get("new-symptoms-fd")
    new_treatment_fd = request.form.get("new-treatment-fd")
    db.update_fd( new_path_fd, new_mode_fd, new_symptoms_fd, new_treatment_fd, new_diseasename_fd)

    return redirect(url_for('diseasetable.admin_diseasetable_view'))


@diseasetable.route("/deletediseasevd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def delete_disease_vd():
    db = UserDatabase(current_app.config["USERS_DB"])
    vd_name=request.form.get('vdnamefor')
    db.delete_vd(vd_name)
    
    return redirect(url_for('diseasetable.admin_diseasetable_view'))


@diseasetable.route("/deletediseasebd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def delete_disease_bd():
    db = UserDatabase(current_app.config["USERS_DB"])
    bd_name=request.form.get('bdnamefor')
    db.delete_bd(bd_name)
    
    return redirect(url_for('diseasetable.admin_diseasetable_view'))


@diseasetable.route("/deletediseasewd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def delete_disease_wd():
    db = UserDatabase(current_app.config["USERS_DB"])
    wd_name=request.form.get('wdnamefor')
    db.delete_wd(wd_name)
    
    return redirect(url_for('diseasetable.admin_diseasetable_view'))

@diseasetable.route("/deletediseasefd", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def delete_disease_fd():
    db = UserDatabase(current_app.config["USERS_DB"])
    fd_name=request.form.get('fdnamefor')
    db.delete_fd(fd_name)
    
    return redirect(url_for('diseasetable.admin_diseasetable_view'))
