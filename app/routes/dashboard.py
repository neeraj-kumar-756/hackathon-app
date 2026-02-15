from flask import Blueprint, render_template, session, redirect, url_for
from app.models.model import User, Employee, Payroll, db
from sqlalchemy import func
from datetime import datetime
import calendar

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    # 1. Real-time Stats
    total_employees = Employee.query.count()
    
    now = datetime.now()
    current_month_name = now.strftime('%B')
    current_year = now.year
    
    # Calculate total payroll processed for current month
    payroll_processed = db.session.query(func.sum(Payroll.net_salary)).filter_by(
        month=current_month_name, year=current_year
    ).scalar() or 0.0
    
    # Compliance Issues: Count employees missing critical info (PAN, UAN, etc.)
    compliance_issues = Employee.query.filter(
        (Employee.pan == None) | (Employee.uan == None) | 
        (Employee.pf_number == None) | (Employee.esi_number == None)
    ).count()
    
    # Pending Reports: Active employees minus payrolls generated this month
    payrolls_count = Payroll.query.filter_by(
        month=current_month_name, year=current_year
    ).count()
    pending_reports = max(0, total_employees - payrolls_count)

    # 2. Attendance Trends (Last 6 months)
    attendance_labels = []
    attendance_data = []
    
    for i in range(5, -1, -1):
        # Calculate month/year logic to handle year rollover
        month_idx = (now.month - i - 1) % 12 + 1
        year = now.year + ((now.month - i - 1) // 12)
        month_name = calendar.month_name[month_idx]
        
        attendance_labels.append(month_name[:3]) # Short name (Jan, Feb)
        
        avg_att = db.session.query(func.avg(Payroll.attendance_days)).filter_by(
            month=month_name, year=year
        ).scalar()
        attendance_data.append(round(avg_att, 1) if avg_att else 0)

    # 3. Department Distribution
    dept_results = db.session.query(
        Employee.department, func.count(Employee.id)
    ).group_by(Employee.department).all()
    
    dept_labels = []
    dept_data = []
    
    for dept, count in dept_results:
        dept_labels.append(dept if dept else "Unassigned")
        dept_data.append(count)
        
    if not dept_labels:
        dept_labels = ["No Data"]
        dept_data = [0]

    employees = Employee.query.all()

    return render_template('dashboard.html', user=user, total_employees=total_employees, payroll_processed=f"${payroll_processed:,.2f}", pending_reports=pending_reports, compliance_issues=compliance_issues, attendance_labels=attendance_labels, attendance_data=attendance_data, dept_labels=dept_labels, dept_data=dept_data, employees=employees)