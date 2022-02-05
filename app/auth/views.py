from . import auth
from flask import jsonify, redirect, render_template, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from app.forms import Register, Login
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = Register()

    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.username = form.username.data
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        
        db.session.add(user)
        db.session.commit()

                

        return redirect(url_for(".login"))
    return render_template("register.html", form=form)    



@auth.route('/login', methods=["GET", "POST"])
def login():

    form = Login()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 

        if not user:
            flash("Invalid Email", "danger")
            return redirect(url_for(".login"))

        if not check_password_hash(user.password, form.password.data):
            flash("Invalid Password", "danger")
            return redirect(url_for(".login"))

        idstr = str(user.id)
        session.modified = True
        session['id'] = idstr
        session['name'] = user.name
        session['username'] = user.username


        login_user(user)
        return redirect(url_for('main'))

    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
   