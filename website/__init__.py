from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
# from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, 
                static_url_path='/',
                static_folder='static',
                template_folder='templates',
                )

    app.config['SECRET_KEY'] = 'SADMAN420'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root@localhost/sadman"
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    
    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Admin, Customer, Payment, Coupon
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(email):
        user = Customer.query.filter_by(email=email).first()
        if user:
            print(user)
            return user
        else:
            user = Admin.query.filter_by(email=email).first()
            print("Admin", user)
            return user

    return app