from flask import Flask
from flask_login import LoginManager
from app.db import Session_users, User

app = Flask(__name__)
app.config["SECRET_KEY"] = "AprioriKS"
login_manager = LoginManager()
login_manager.login_view="login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id: int):
    with Session_users() as session:
        return session.query(User).where(User.id==user_id).first()