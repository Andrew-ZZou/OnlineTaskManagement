from flask import Blueprint, render_template,request, redirect,url_for,flash
from sqlalchemy.testing.suite.test_reflection import users
from exts import db

from forms import RegisterForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user', __name__, url_prefix="/user")

#landing page
@bp.route('/')
def index():
    return render_template('index.html', methods=['GET', 'POST'])


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
            return redirect(url_for("user.index"))
        else:
            print(form.errors)
            return redirect(url_for("user.registration"))
