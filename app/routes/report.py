from flask import Blueprint, render_template, session, redirect, url_for, flash, send_file, current_app
from app.models.model import User, Employee
from app.models.Form_16 import generate_form16
from app.models.muster_roll import generate_muster_roll
from app.models.pf_esi import generate_pf_esi_summary
import os

report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
def report():
    if 'user_id' not in session:
        flash('Please log in to access reports.')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('Session invalid. Please log in again.')
        return redirect(url_for('auth.login'))
        
    return render_template('report.html', user=user)

@report_bp.route('/report/generate/<report_type>')
def generate_report(report_type):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    user_role = session.get('user_role')
    docs_dir = os.path.join(current_app.root_path, 'docs')
    
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    if report_type == 'form16':
        filename = f"Form16_{user_id}.pdf"
        filepath = os.path.join(docs_dir, filename)
        
        # Fetch data for the logged-in user or a default employee
        current_user = User.query.get(user_id)
        employee = Employee.query.filter_by(email=current_user.email).first()
        
        # If admin or no matching employee, use the first employee found
        if not employee:
            employee = Employee.query.first()
            
        data = {}
        if employee:
            annual_salary = employee.basic_salary * 12
            data = {
                'name': employee.name,
                'pan': employee.pan if employee.pan else "Not Found",
                'uan': employee.uan if employee.uan else "Not Found",
                'period': "FY 2025-26",
                'amount_paid': f"Rs. {annual_salary:,.2f}",
                'tax_deducted': f"Rs. {annual_salary * 0.05:,.2f}", # Assumed 5%
                'tax_deposited': f"Rs. {annual_salary * 0.05:,.2f}",
                'taxable_salary': f"Rs. {max(0, annual_salary - 50000):,.2f}" # Standard deduction
            }
        
        generate_form16(filepath, data)
        
    elif report_type == 'muster':
        if user_role != 'admin':
            flash('Unauthorized: Only admins can generate Muster Roll.')
            return redirect(url_for('report.report'))
            
        filename = f"MusterRoll_{user_id}.pdf"
        filepath = os.path.join(docs_dir, filename)
        
        employees = Employee.query.all()
        emp_list = []
        for i, emp in enumerate(employees, 1):
            emp_list.append({
                'sl': str(i),
                'name': emp.name,
                'present': '26', # Mock attendance
                'gross': f"{emp.basic_salary:.2f}",
                'deduction': f"{emp.basic_salary * 0.1:.2f}",
                'net': f"{emp.basic_salary * 0.9:.2f}",
                'pf': f"{emp.basic_salary * 0.12:.2f}",
                'esi': f"{emp.basic_salary * 0.0075:.2f}"
            })
            
        generate_muster_roll(filepath, emp_list)
        
    elif report_type == 'pf_esi':
        if user_role != 'admin':
            flash('Unauthorized: Only admins can generate PF & ESI Summary.')
            return redirect(url_for('report.report'))
            
        filename = f"PF_ESI_{user_id}.pdf"
        filepath = os.path.join(docs_dir, filename)
        
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            pf = emp.basic_salary * 0.12
            esi = emp.basic_salary * 0.0075
            emp_list.append({
                'name': emp.name,
                'emp_pf': f"{pf:.2f}",
                'employer_pf': f"{pf:.2f}", # Employer matches 12%
                'total_pf': f"{pf * 2:.2f}",
                'emp_esi': f"{esi:.2f}",
                'employer_esi': f"{esi * (3.25/0.75):.2f}", # Employer 3.25% vs Employee 0.75%
                'total_esi': f"{esi + (esi * (3.25/0.75)):.2f}"
            })
            
        generate_pf_esi_summary(filepath, emp_list)
    else:
        flash('Invalid report type')
        return redirect(url_for('report.report'))
        
    return send_file(filepath, as_attachment=True)