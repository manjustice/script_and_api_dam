from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rdn_data.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


if __name__ == "config":
    from models import Date, DAMResult
