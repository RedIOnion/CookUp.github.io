from flask import Flask
from flask_login import LoginManager

from models import User, db
from routes import Init

import os;

base_folder = os.getcwd()

staticPath = os.path.join(base_folder, "static")
templatePath = os.path.join(base_folder, "templates")    
app = Flask(__name__, template_folder= templatePath, static_folder= staticPath)

app.config["SECRET_KEY"] = "very secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

Init(app, staticPath)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)