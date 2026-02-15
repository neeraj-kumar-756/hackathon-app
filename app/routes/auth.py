from flask import Blueprint,redirect,render_template,url_for,flash,session,request
from app.models.model import User, db

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/')
def root():
    if 'user_id' in session:
        if session.get('user_role') == 'admin':
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('employee.employee_dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('user_role') == 'admin':
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('employee.employee_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            
            if user.role == 'admin':
                return redirect(url_for('dashboard.dashboard'))
            return redirect(url_for('employee.employee_dashboard'))
        
        flash('Invalid email or password')
    return render_template('login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        if session.get('user_role') == 'admin':
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('employee.employee_dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'employee')
        
        if not User.query.filter_by(email=email).first():
            new_user = User(name=name, email=email, role=role, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        flash('Email already exists')
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
