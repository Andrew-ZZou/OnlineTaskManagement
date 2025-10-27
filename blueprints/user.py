import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from sqlalchemy.sql.functions import user
from sqlalchemy.testing.pickleable import User
from sqlalchemy.testing.suite.test_reflection import users
from exts import db
from forms import RegisterForm, UpdateForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, current_user, login_required,LoginManager

bp = Blueprint('user', __name__, url_prefix="/user")

#registration page
@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            firstName = form.firstName.data
            lastName = form.lastName.data
            email = form.email.data
            phone = form.phone.data
            password = form.password.data
            newUser = UserModel(firstName = firstName, lastName = lastName, phone = phone, email=email, password=generate_password_hash(password))

            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            print(form.errors)
            return redirect(url_for("user.registration"))

#user details update page
@bp.route('/update', methods=['GET', 'POST'])
def update():
    user_id = session.get('user_id')
    # get posted user data
    user_update = db.session.execute(db.select(UserModel).filter_by(id=user_id)).scalar_one()

    if user_update:
        if request.method == 'GET':
            return render_template("update.html")
        else:
            form = UpdateForm(request.form)
            if form.validate():
                new_firstName = request.form['firstName']
                new_lastName = request.form['lastName']
                new_phone = request.form['phone']
                new_email = request.form['email']
                new_password = request.form['password']

                user_update.firstName = new_firstName
                user_update.lastName = new_lastName
                user_update.phone = new_phone
                user_update.email = new_email
                user_update.password = generate_password_hash(new_password)

                db.session.commit() # update user data
                flash("User updated successfully")
                return redirect(url_for("task.dashboard"))
    else:
        flash("Cannot find user")
        return redirect(url_for("task.dashboard"))
