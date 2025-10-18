from flask import Blueprint, render_template

bp = Blueprint('user', __name__, url_prefix="/user")

#landing page
@bp.route('/')
def index():
    return render_template('index.html')


#registration page
@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')