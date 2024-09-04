from app import db
from sqlalchemy import ARRAY
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy=True)

# class Meta(db.Model):
#     __tablename__ = 'metas'
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(255), nullable=False)
#     header_id = db.Column(db.Integer, db.ForeignKey('headers.id'), nullable=False)

# class Header(db.Model):
#     __tablename__ = 'headers'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     image = db.Column(db.String(255), nullable=False)
#     meta = db.relationship('Meta', backref='header', lazy=True)
#     blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    read_time = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    keywords = db.Column(ARRAY(db.String(50)),default=[])
    # header = db.relationship('Header', backref='blog', lazy=True)
    contents = db.relationship('Content', backref='blog', lazy=True)
    Categorys = db.relationship('Category', backref='blog', lazy=True)
    faqs = db.relationship('Faq', backref='blog', lazy=True)
    # popular_topics = db.relationship('PopularTopic', backref='blog', lazy=True)
    # topics = db.relationship('Topic', backref='blog', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self,id, img, title, description,read_time,date, user_id,keywords):
        self.id = id
        self.img = img
        self.keywords = keywords if keywords is not None else []
        self.date = date
        self.read_time = read_time
        self.title = title
        self.description = description
        self.user_id = user_id

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

    def __init__(self,id, blog_id, title, description):
        self.id = id
        self.title = title
        self.description = description
        self.blog_id = blog_id
    
class Category(db.Model):
    __tablename__ = 'Categorys'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

    def __init__(self,id, blog_id, title, description):
        self.id = id
        self.title = title
        self.description = description
        self.blog_id = blog_id

class Faq(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
