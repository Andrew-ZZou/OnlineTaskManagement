from flask import Blueprint, render_template,request, redirect,url_for,flash,session
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


@bp.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        form = UpdateForm(request.form)
        if form.validate():
            new_firstName = request.form.get('firstName')
            new_lastName = request.form.get('lastName')
            new_phone = request.form.get('phone')
            new_email = request.form.get('email')
            new_password = request.form.get('password')

            user.firstName = new_firstName
            user.lastName = new_lastName
            user.phone = new_phone
            user.email = new_email
            user.password = generate_password_hash(new_password)

            try:
                db.session.commit()
                flash("User updated successfully")
                return redirect(url_for("task.dashboard"))
            except:
                flash("User update failed")
                return redirect(url_for("index"))
        else:
            print(form.errors)
            return redirect(url_for("task.dashboard"))
