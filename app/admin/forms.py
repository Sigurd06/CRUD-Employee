from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role

class DepartmentForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class RoleForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar')
    
class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')