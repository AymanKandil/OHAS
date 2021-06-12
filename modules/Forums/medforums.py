from flask import (
    Blueprint, render_template, redirect, url_for, request, flash,
    current_app
)
from flask_login import login_required, current_user
from modules.Auth.user_db import UserDatabase
import numpy as np
from itertools import chain, product
from models import requires_access_level

medforums = Blueprint(
    'medforums', __name__
)

@medforums.route("/")
@login_required
def medforums_view():
    db = UserDatabase(current_app.config["USERS_DB"])
    ddata=db.get_blogs()
    return render_template("blogsforums.html", d=ddata)

@medforums.route("/adminblogs")
@login_required
@requires_access_level([1, 3])
def admin_medforums_view():
    db = UserDatabase(current_app.config["USERS_DB"])

    loggeduser = current_user.get_id()

    blog_data= db.get_blogs_admin(loggeduser)
    

    return render_template("doctorBlogs.html", bdata=blog_data)

@medforums.route("/addblog", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def addblog():
    db = UserDatabase(current_app.config["USERS_DB"])

    loggeduser = current_user.get_id()  

    blog_name= request.form.get("blog-title")
    blog= request.form.get("blog-text")
    blog_date= request.form.get("date")
   
    db.insert_blog(blog_name, blog, blog_date, loggeduser)

    return redirect(url_for('medforums.admin_medforums_view'))

@medforums.route("/updateblog", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def updateblog():
    db = UserDatabase(current_app.config["USERS_DB"])


    blog_id= request.form.get("blog_id")
    blog_name= request.form.get("new-blog-title")
    blog= request.form.get("new-blog-text")
    blog_date= request.form.get("new-date")
   
    db.update_blog(blog_name, blog, blog_date, blog_id)

    return redirect(url_for('medforums.admin_medforums_view'))

@medforums.route("/deleteblog", methods=["POST"])
@login_required
@requires_access_level([1, 3])
def deleteblog():
    db = UserDatabase(current_app.config["USERS_DB"])

    blogid=request.form.get('blogID')
    db.delete_blog(blogid)
   

    return redirect(url_for('medforums.admin_medforums_view'))

@medforums.route("/<blog_id>")
@login_required
@requires_access_level([1, 3])
def single_medforums_view(blog_id):
    db = UserDatabase(current_app.config["USERS_DB"])
    bbdata=db.get_blogs_ID(blog_id)
    return render_template("blogview.html", data=bbdata)