import wtforms
from wtforms.validators import Email, Length, ValidationError, EqualTo
from models import UserModel

# form: check all datas from webpages
class RegisterForm(wtforms.Form):
    firstName = wtforms.StringField(validators=[Length(max=80, message="Invalid first name")])
    lastName = wtforms.StringField(validators=[Length(max=80, message="Invalid last name")])
    email = wtforms.StringField(validators=[Email(message="Invalid email")])
    phone = wtforms.StringField(validators=[Length(min=1, max=50,message="Invalid phone number")])
    password =wtforms.StringField(validators=[Length(min=6, message="Invalid password")])
    confirm = wtforms.StringField(validators=[EqualTo("password")])

#ensure no same email address has been registered
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email = email).first()
        if user:
            raise wtforms.ValidationError("Email already been registered")


class UpdateForm(wtforms.Form):
    firstName = wtforms.StringField(validators=[Length(max=80, message="Invalid first name")])
    lastName = wtforms.StringField(validators=[Length(max=80, message="Invalid last name")])
    email = wtforms.StringField(validators=[Email(message="Invalid email")])
    phone = wtforms.StringField(validators=[Length(min=1, max=50,message="Invalid phone number")])
    password =wtforms.StringField(validators=[Length(min=6, message="Invalid password")])
    confirm = wtforms.StringField(validators=[EqualTo("password")])

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Invalid email")])
    password = wtforms.StringField(validators=[Length(min=6, message="Invalid password")])

class TaskForm(wtforms.Form):
    description = wtforms.StringField(validators=[Length(max=200, message="Invalid description")])
    status = wtforms.SelectField(choices=[("Yet-to-Do", "Yet-to-Do"), ("On-Going", "On-Going"),("Completed","Completed")])
    priority = wtforms.SelectField(choices=[("Low", "Low"), ("Medium", "Medium"),("High","High")])
    title_id = wtforms.StringField(validators=[Length(max=80, message="Invalid user id")])

class TitleForm(wtforms.Form):
    titleName = wtforms.StringField(validators=[Length(max=80, message="Invalid title")])
    reviewNote = wtforms.StringField(validators=[Length(max=200, message="Invalid review")])
    user_id = wtforms.StringField(validators=[Length(max=80, message="Invalid user id")])
