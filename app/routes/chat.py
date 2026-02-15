from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import os

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
        
        # Personalize the AI context for your MSME Payroll Software
        system_context = (
            "You are a helpful AI assistant for an open-source payroll software designed for MSMEs. "
            "The software automates payroll data management, generates legally compliant registers, "
            "reports, and returns for labor regulations. Assist the user with their queries."
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