from flask import Flask
from models import db

DATABASE_NAME = 'database.db'

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = "beginnerz"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    
    @app.route("/")
    def index():
        return "Hello, World!"
    
    db.init_app(app)

    from lessson.views import lessson
    app.register_blueprint(lessson, url_prefix="/lessson")

    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
