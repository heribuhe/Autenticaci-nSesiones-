from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.auth_blueprint import auth
from app.models import db, User
from app.forms import LoginForm
from app.controlador_juego import init_routes

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2004@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

init_routes(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"

 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)
