from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from app.models.model import User, Employee, db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('auth.login'))
    
    if session.get('user_role') != 'admin':
        flash('Access denied. Redirected to Employee Dashboard.')
        return redirect(url_for('employee.employee_dashboard'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Session invalid. Please log in again.')
        return redirect(url_for('auth.login'))
        
    employees = Employee.query.all()
    return render_template('dashboard.html', user=user, employees=employees)