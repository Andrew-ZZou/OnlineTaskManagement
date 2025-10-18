import wtforms
from wtforms.validators import Email, length, equal_to, ValidationError
from models import UserModel

# form: check all datas from webpages
class RegisterForm(wtforms.Form):
    first_name = wtforms.StringField(validators=[wtforms.validators.Length(max=50, message="Invalid first name")])
    last_name = wtforms.StringField(validators=[wtforms.validators.Length(max=50, message="Invalid last name")])
    email = wtforms.StringField(validators=[wtforms.validators.Email(message="Invalid email")])
    phone = wtforms.StringField(validators=[wtforms.validators.Length(max=50,message="Invalid phone number")])
    password = wtforms.StringField(validators=[wtforms.validators.DataRequired(message="Invalid password")])
    password_confirm = wtforms.PasswordField(validators=[wtforms.validators.DataRequired(message="Invalid password")])

#ensure no same email address has been registered
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("Email already registered")
