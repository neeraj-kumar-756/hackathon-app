from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import os
from app.models.model import Employee, Company, Payroll, db
from sqlalchemy import func
from datetime import datetime

# Try importing SarvamAI, handle if not present
try:
    from sarvamai import SarvamAI
except ImportError:
    SarvamAI = None

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat_interface():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('chat.html')

@chat_bp.route('/api/chat', methods=['POST'])
def chat_api():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    api_key = os.environ.get('SARVAM_API_KEY')
    if not api_key:
        return jsonify({'error': 'Server configuration error: API Key missing'}), 500
        
    if not SarvamAI:
        return jsonify({'error': 'SarvamAI library not installed'}), 500

    try:
        client = SarvamAI(api_subscription_key=api_key)
        
        # Fetch Context Data from Database
        # 1. Company Info
        company = Company.query.first()
        company_details = "Not Configured"
        if company:
            company_details = f"Name: {company.name}, Address: {company.address}, PF Code: {company.pf_code}, ESI Code: {company.esi_code}"

        # 2. Employee Stats & List
        total_employees = Employee.query.count()
        employees = Employee.query.all()
        emp_list_str = "; ".join([f"{e.name} ({e.designation}, {e.department or 'N/A'})" for e in employees])

        # 3. Payroll Stats
        now = datetime.now()
        current_month = now.strftime('%B')
        current_year = now.year
        payroll_processed = db.session.query(func.sum(Payroll.net_salary)).filter_by(month=current_month, year=current_year).scalar() or 0.0

        # Personalize the AI context for your MSME Payroll Software
        system_context = (
            "You are a helpful AI assistant for an open-source payroll software designed for MSMEs. "
            "You have access to the following live system data:\n"
            f"Company: {company_details}\n"
            f"Current Month: {current_month} {current_year}\n"
            f"Total Employees: {total_employees}\n"
            f"Payroll Processed: Rs. {payroll_processed:,.2f}\n"
            f"Employee Directory: {emp_list_str}\n\n"
            "The software automates oss msme finance management, generates legally compliant registers (Muster Roll), "
            "reports (Form 16, PF/ESI), and returns for labor regulations. "
            "Answer user queries based on this data. If asked about specific employees, use the directory."
        )

        response = client.chat.completions(
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extract the response content
        # Assuming SarvamAI follows standard completion response structure
        ai_reply = response.choices[0].message.content
        
        return jsonify({'response': ai_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500