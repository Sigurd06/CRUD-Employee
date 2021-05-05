from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from .. import db
from ..models import Employee

@auth.route('/registro', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        db.session.add(employee)
        db.session.commit()
        flash('¡Se ha registrado exitosamente! Ahora puede iniciar sesión.')
        # redirect to the login page
        return redirect(url_for('auth.login'))
    # load template
    return render_template('auth/register.html', form=form, title='Registro')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            #log employee in
            login_user(employee)

            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Correo electrónico o contraseña no válidos.')
    
     # load template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Se ha desconectado con éxito.')

    # redirect to the login page
    return redirect(url_for('auth.login'))