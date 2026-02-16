from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.model import User, Employee, Payroll, Attendance, db
from datetime import datetime

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/payroll')
def payroll_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('user_role') != 'admin':
        flash('Unauthorized access.')
        return redirect(url_for('employee.employee_dashboard'))

    # Fetch payrolls sorted by most recent
    payrolls = Payroll.query.order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    employees = Employee.query.all()
    return render_template('payroll.html', payrolls=payrolls, employees=employees)

@payroll_bp.route('/payroll/generate', methods=['POST'])
def generate_payroll():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('auth.login'))

    try:
        employee_id = request.form.get('employee_id')
        month = request.form.get('month')
        year = int(request.form.get('year'))
        
        # Robust Attendance Fetching
        # 1. Try fetching from Attendance DB
        attendance_record = Attendance.query.filter_by(employee_id=employee_id, month=month, year=year).first()
        
        if attendance_record:
            attendance_days = attendance_record.present_days
        else:
            # 2. Fallback to manual input
            manual_days = request.form.get('attendance_days')
            if manual_days:
                attendance_days = float(manual_days)
            else:
                flash('Error: No attendance record found in DB and no manual input provided.')
                return redirect(url_for('payroll.payroll_dashboard'))

        if attendance_days < 0 or attendance_days > 31:
            flash('Error: Invalid attendance days.')
            return redirect(url_for('payroll.payroll_dashboard'))

        employee = Employee.query.get(employee_id)
        if not employee:
            flash('Employee not found.')
            return redirect(url_for('payroll.payroll_dashboard'))

        # Check if payroll already exists for this period
        existing = Payroll.query.filter_by(employee_id=employee_id, month=month, year=year).first()
        if existing:
            flash(f'Payroll for {employee.name} for {month} {year} already exists.')
            return redirect(url_for('payroll.payroll_dashboard'))

        # --- Payroll Calculation Logic ---
        # Standardizing month to 30 days for calculation
        total_working_days = 30 
        
        # 1. Calculate Earned Basic Salary (Pro-rata based on attendance)
        # Formula: (Basic / 30) * Days Present
        earned_basic = (employee.basic_salary / total_working_days) * attendance_days
        
        # 2. Calculate Deductions
        # PF: 12% of Earned Basic
        pf_deduction = earned_basic * 0.12
        # ESI: 0.75% of Earned Basic
        esi_deduction = earned_basic * 0.0075
        
        # 3. Calculate Net Salary
        net_salary = earned_basic - pf_deduction - esi_deduction

        new_payroll = Payroll(
            employee_id=employee_id,
            month=month,
            year=year,
            attendance_days=attendance_days,
            net_salary=round(net_salary, 2)
        )

        db.session.add(new_payroll)
        db.session.commit()

        flash(f'Payroll generated! Net Salary: Rs. {new_payroll.net_salary}')
    except Exception as e:
        flash(f'Error generating payroll: {str(e)}')

    return redirect(url_for('payroll.payroll_dashboard'))

@payroll_bp.route('/attendance/update', methods=['POST'])
def update_attendance():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        employee_id = request.form.get('employee_id')
        month = request.form.get('month')
        year = int(request.form.get('year'))
        present_days = float(request.form.get('present_days'))

        attendance = Attendance.query.filter_by(employee_id=employee_id, month=month, year=year).first()
        if attendance:
            attendance.present_days = present_days
        else:
            attendance = Attendance(employee_id=employee_id, month=month, year=year, present_days=present_days)
            db.session.add(attendance)
        
        db.session.commit()
        flash('Attendance record updated successfully.')
    except Exception as e:
        flash(f'Error updating attendance: {str(e)}')
    
    return redirect(url_for('payroll.payroll_dashboard'))

@payroll_bp.route('/payroll/delete/<int:id>')
def delete_payroll(id):
    if 'user_id' in session and session.get('user_role') == 'admin':
        payroll = Payroll.query.get(id)
        if payroll:
            db.session.delete(payroll)
            db.session.commit()
            flash('Payroll record deleted.')
    return redirect(url_for('payroll.payroll_dashboard'))