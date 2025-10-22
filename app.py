from flask_migrate import Migrate
from flask import Flask,render_template,request, redirect,url_for,flash,session,g
from exts import db
from blueprints.user import bp as user_bp
from blueprints.task import bp as task_bp
from forms import LoginForm
from models import UserModel
from werkzeug.security import  check_password_hash


app = Flask(__name__)

app.config ['SECRET_KEY'] = "ABCabc123123"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin123@localhost:5432/onlineTaskManagement"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(task_bp)


#landing/login page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()

            if not user:
                flash('Can not find email address','error')
                return redirect(url_for("index"))

            if check_password_hash(user.password, password):

                session['user_id'] = user.id
                return redirect(url_for("task.dashboard"))
            else:
                flash('Wrong password','error')
                return redirect(url_for("index"))
        else:
            print(form.errors)
            return redirect(url_for("index"))

@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)

    else:
        setattr(g, "user", None)


@app.context_processor
def inject_user():
    return {"user" : g.user}


app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run()

