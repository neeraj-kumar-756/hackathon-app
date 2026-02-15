from flask import Flask
import os
from app.models.model import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:database@localhost:5432/test_db')
    
    # Fix for SQLAlchemy: Render uses postgres://, SQLAlchemy needs postgresql://
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SECRET_KEY']='my-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI']=database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.employee import employee_bp
    from app.routes.report import report_bp
    from app.routes.chat import chat_bp
    from app.routes.company import company_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(company_bp)

    return app