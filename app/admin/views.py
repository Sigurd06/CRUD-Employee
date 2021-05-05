from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db
from .forms import DepartmentForm, EmployeeAssignForm, RoleForm
from ..models import Department, Employee, Role

def check_admin():
    """
    Impedir que los no administradores accedan a la página
    """
    if not current_user.is_admin:
        abort(403)

@admin.route('/departamentos', methods=['GET', 'POST'])
@login_required
def list_departments():
    check_admin()

    departments  = Department.query.all()
    return render_template('admin/departments/departments.html',
                           departments=departments , title="Departamentos")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    check_admin()
    add_department = True
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)
        try:
            # add 
            db.session.add(department)
            db.session.commit()
            flash('Ha agregado exitosamente un nuevo departamento.')
        except:
            # in case department name already exists
            flash('Error: el nombre del departamento ya existe.')

        # redirect page
        return redirect(url_for('admin.list_departments'))

    # load  template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Agrega Departamento")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('Ha editado correctamente el departamento.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('Ha eliminado correctamente el departamento.')

    # redirect to  page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


# ROLES CRUD

@admin.route('/roles')
@login_required
def list_roles():
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add
            db.session.add(role)
            db.session.commit()
            flash('Ha agregado con éxito un nuevo rol.')
        except:
            # in case role name already exists
            flash('Error: el nombre del rol ya existe.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Agregar Rol')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('Ha editado correctamente el rol')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Editar Rol")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('Has eliminado correctamente el rol.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# EMPLOYEES
@admin.route('/employees')
@login_required
def list_employees():
    
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Empleados')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('Ha asignado correctamente un departamento y una función.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Asignar empleado')
