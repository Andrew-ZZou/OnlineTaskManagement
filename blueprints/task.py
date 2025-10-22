from flask import Blueprint, session
from flask import render_template
from flask_login import current_user

from models import UserModel

bp = Blueprint('task', __name__, url_prefix="/dashboard")

#add task page
@bp.route('/home')
def home():
    return render_template('home.html')

#dashboard page
@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')