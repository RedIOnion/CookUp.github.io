import os
from flask import Flask
from models import db

def CreateApp(secret_key=None):
    base_folder = os.getcwd()
    
    app = Flask(__name__,
        template_folder=os.path.join(base_folder, "templates"),
        static_folder=os.path.join(base_folder, "static")
    )

    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app