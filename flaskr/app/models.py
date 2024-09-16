from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blogs = db.relationship('Blog', backref='category', lazy=True)  

    def __init__(self, title, description):
        self.title = title
        self.description = description

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    read_time = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    keywords = db.Column(ARRAY(db.String(50)), default=[])
    contents = db.relationship('Content', backref='blog', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  
    faqs = db.relationship('Faq', backref='blog', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, img, title, description, read_time, user_id, category_id, keywords=None):
        self.img = img
        self.title = title
        self.description = description
        self.read_time = read_time
        self.keywords = keywords if keywords is not None else []
        self.user_id = user_id
        self.category_id = category_id  

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

    def __init__(self, title, description, blog_id):
        self.title = title
        self.description = description
        self.blog_id = blog_id

class Faq(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
