from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField,ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee

class RegistrationForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email()])
    username = StringField('Usuario', validators=[DataRequired()])
    first_name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password', message='La contraseña no coinciden')
                                        ])
    confirm_password = PasswordField('Confirma tu Contraseña')
    submit = SubmitField('Registro')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Correo electrónico ya está en uso.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('El nombre de usuario ya está en uso.')
        
class LoginForm(FlaskForm):
    
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Login')

    