from flask_migrate import Migrate
from flask import Flask,render_template,request, redirect
from exts import db
from models import UserModel
from models import TaskModel
from blueprints.user import bp as user_bp
from blueprints.task import bp as task_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Admin123@localhost:5432/onlineTaskManagement"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(task_bp)

app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run()

