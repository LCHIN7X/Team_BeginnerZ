from flask import Flask
from models import db
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from .celery import make_celery


DATABASE_NAME = 'database.db'
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "beginnerz"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    
    from user.models import User
    from user.views import views
    app.register_blueprint(views, url_prefix="/views")

    from trade import views as trade_views  
    app.register_blueprint(trade_views.trade, url_prefix="/trade")

    from ranking.views import rank
    app.register_blueprint(rank, url_prefix="/rank")
    
    db.init_app(app)

    mail.init_app(app)

    celery = make_celery(app)
   

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "views.login"
    login_manager.init_app(app)

    @login_manager.user_loader 
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
