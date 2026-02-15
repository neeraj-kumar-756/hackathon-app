from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models.model import User, Employee, db
from datetime import datetime

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/employee', methods=['GET', 'POST'])
def employee_dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the employee dashboard.')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        if session.get('user_role') != 'admin':
            flash('Unauthorized: Only admins can add employees.')
            return redirect(url_for('employee.employee_dashboard'))

        try:
            name = request.form.get('name')
            email = request.form.get('email')
            designation = request.form.get('designation')
            department = request.form.get('department')
            salary = float(request.form.get('salary'))
            join_date = datetime.strptime(request.form.get('join_date'), '%Y-%m-%d').date()
            pan = request.form.get('pan')
            uan = request.form.get('uan')
            pf_number = request.form.get('pf_number')
            esi_number = request.form.get('esi_number')

            new_emp = Employee(name=name, email=email, designation=designation, department=department, basic_salary=salary, joining_date=join_date, pan=pan, uan=uan, pf_number=pf_number, esi_number=esi_number)
            db.session.add(new_emp)
            db.session.commit()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Employee added successfully!',
                    'employee': {
                        'name': new_emp.name,
                        'email': new_emp.email,
                        'designation': new_emp.designation,
                        'joining_date': new_emp.joining_date.strftime('%Y-%m-%d'),
                        'basic_salary': new_emp.basic_salary
                    }
                })

            flash('Employee added successfully!')
            return redirect(url_for('dashboard.dashboard'))
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': str(e)}), 500
            flash(f'Error adding employee: {str(e)}')
            return redirect(url_for('dashboard.dashboard'))

    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Session invalid. Please log in again.')
        return redirect(url_for('auth.login'))
        
    employees = Employee.query.all()
    return render_template('employee.html', user=user, employees=employees)