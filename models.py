from exts import db

# user model
class UserModel(db.Model):
    # def __init__(self, first_name, last_name, email, phone, password):
    __tablename__ = 'users'
    #id can link to student ID if there is any
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False,unique=True)
    password = db.Column(db.String(200), nullable=False)
    titles =db.relationship('TitleModel', backref='user', lazy=True)

    def __init__(self, firstName, lastName, email, phone, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone
        self.password = password

class TitleModel(db.Model):
    __tablename__ = 'titles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titleName = db.Column(db.String(80), nullable=False)
    reviewNote = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete="CASCADE"), nullable=False)
    tasks = db.relationship('TaskModel', backref='title', lazy='dynamic')

    def __init__(self,titleName, reviewNote, user_id):
        self.titleName = titleName
        self.reviewNote = reviewNote
        self.user_id = user_id

#task model
class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(80), nullable=False)
    priority = db.Column(db.String(80), nullable=False)
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id',ondelete="CASCADE"), nullable=False)# Foreign key

    def __init__(self, description, status, priority, title_id):
        self.description = description
        self.status = status
        self.priority = priority
        self.title_id = title_id





