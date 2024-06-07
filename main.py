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

    from Lesson.views import lesson
    app.register_blueprint(lesson, url_prefix="/lesson")

    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
