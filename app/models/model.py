from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, server_default='user')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    pan = db.Column(db.String(20), nullable=True)
    uan = db.Column(db.String(20), nullable=True)
    pf_number = db.Column(db.String(20), nullable=True)
    esi_number = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(50), nullable=True)

class Payroll(db.Model):
    __tablename__ = 'payrolls'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)
    attendance_days = db.Column(db.Integer, default=0)
    generated_at = db.Column(db.DateTime, default=db.func.now())

    employee = db.relationship('Employee', backref=db.backref('payrolls', lazy=True))
