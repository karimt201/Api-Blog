from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from flask_restx import Api


app = Flask(__name__)


CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:qwerty@localhost:5432/Blog"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Blog API",
        "description": "API documentation for a blog application built with Flask and PostgreSQL.",
        "version": "1.0"
    }
}
app.config['SWAGGER'] = {
    'title': 'Flask Blog API',
    'uiversion': 2
}
Swagger(app, template=template)

from app import models , routes