from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.model import User

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