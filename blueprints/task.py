from flask import Blueprint
from flask import render_template

bp = Blueprint('task', __name__, url_prefix="/dashboard")

#add task page
@bp.route('/home')
def home():
    return render_template('home.html')

#dashboard page
@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')