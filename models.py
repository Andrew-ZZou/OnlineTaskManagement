from exts import db

# user model
class UserModel(db.Model):
    # def __init__(self, first_name, last_name, email, phone, password):
    __tablename__ = 'users'
    #id can link to student ID if there is any
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False,unique=True)
    password = db.Column(db.String(80), nullable=False)

#task model
class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    review = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(80), nullable=False)
    priority = db.Column(db.String(80), nullable=False)

# Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)




