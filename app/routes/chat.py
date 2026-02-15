from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import os
from app.models.model import Employee, Company, Payroll, User, db
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
        
        # Fetch Context Data from Database (RAG - Retrieval Augmented Generation)
        
        # 1. Company Info
        company = Company.query.first()
        company_info = "Not Configured"
        if company:
            company_info = (
                f"Name: {company.name}, Address: {company.address}, "
                f"GST: {company.gst_number}, PAN: {company.pan_number}, "
                f"PF Code: {company.pf_code}, ESI Code: {company.esi_code}, "
                f"PT Circle: {company.pt_circle}"
            )

        # 2. User Info (Admins/Staff)
        users = User.query.all()
        users_info = "\n".join([f"- {u.name} ({u.role}, {u.email})" for u in users])

        # 3. Employee Directory
        employees = Employee.query.all()
        employees_info = "\n".join([
            f"- {e.name} (ID: {e.id}, {e.designation}, Dept: {e.department}, "
            f"Salary: {e.basic_salary}, Joined: {e.joining_date}, "
            f"PAN: {e.pan}, UAN: {e.uan})" 
            for e in employees
        ])

        # 4. Payroll History (Recent)
        # Limit to last 20 records to keep context size manageable
        recent_payrolls = Payroll.query.order_by(Payroll.year.desc(), Payroll.month.desc()).limit(20).all()
        payroll_info = "\n".join([
            f"- {p.month} {p.year}: {p.employee.name} (Net: {p.net_salary}, Attendance: {p.attendance_days} days)"
            for p in recent_payrolls
        ])

        # Personalize the AI context for your MSME Payroll Software
        system_context = (
            "You are a helpful AI assistant for 'OSS MSME Finance', an open-source payroll software. "
            "You have access to the following live database records (RAG Context):\n\n"
            
            "=== COMPANY DETAILS ===\n"
            f"{company_info}\n\n"
            
            "=== SYSTEM USERS (Admins/Staff) ===\n"
            f"{users_info}\n\n"
            
            "=== EMPLOYEE DIRECTORY ===\n"
            f"{employees_info}\n\n"
            
            "=== RECENT PAYROLL RECORDS ===\n"
            f"{payroll_info}\n\n"
            
            "Instructions:\n"
            "1. Use the provided data to answer user queries accurately.\n"
            "2. If asked about a specific employee, check the directory.\n"
            "3. If asked about payroll, check the recent records.\n"
            "4. If the information is not in the context, politely say you don't have that data.\n"
            "5. Be concise and professional."
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