from app import db
from sqlalchemy.dialects.postgresql import ARRAY

blog_category_association = db.Table('blog_category',
    db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    img = db.Column(db.String(128), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy=True)
    courses = db.relationship('Course', backref='author', lazy=True)
    
    def __init__(self, username, email,password,img):
        self.username = username
        self.email = email
        self.password = password
        self.img = img

class Category(db.Model):
    __tablename__ = 'categories'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blogs = db.relationship('Blog', secondary=blog_category_association, back_populates='categories')

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
    date = db.Column(db.String(50), nullable=False)
    keywords = db.Column(ARRAY(db.String(50)), default=[])
    contents = db.relationship('Content', backref='blog', lazy=True , cascade='delete')
    faqs = db.relationship('Faq', backref='blog', lazy=True , cascade='delete')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    categories = db.relationship('Category', secondary=blog_category_association, back_populates='blogs')

    def __init__(self, img, title, description, read_time,date, user_id, keywords=None):
        self.img = img
        self.title = title
        self.description = description
        self.date = date
        self.read_time = read_time
        self.keywords = keywords if keywords is not None else []
        self.user_id = user_id

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

training_centers_courses = db.Table('training_centers_courses',
    db.Column('training_center_id', db.Integer, db.ForeignKey('training_centers.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(50))
    pricing = db.Column(db.String(50))
    brief = db.Column(db.String(255))
    img = db.Column(db.String(255))
    requirements = db.Column(db.String(255))
    criteria = db.Column(db.String(255))
    content = db.Column(db.Text)
    startingdate = db.Column(db.String(50))
    enddate = db.Column(db.String(50))
    description = db.Column(db.Text)
    icon = db.Column(db.String(255))  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    lessons = db.relationship('Lesson', backref='course', lazy=True, cascade="all, delete-orphan")
    trainingcenters = db.relationship('TrainingCenters', secondary=training_centers_courses, backref=db.backref('courses_list', lazy=True))

    def __init__(self, title, rating, pricing, brief, img, requirements, criteria, content, startingdate, enddate, description, icon, user_id):
        self.title = title
        self.rating = rating
        self.pricing = pricing
        self.brief = brief
        self.img = img
        self.requirements = requirements
        self.criteria = criteria
        self.content = content
        self.startingdate = startingdate
        self.enddate = enddate
        self.description = description
        self.icon = icon
        self.user_id = user_id

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(32), nullable=False)
    date = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(255)) 

    def __init__(self, course_id, title, slug, date, content, thumbnail=None):
        self.course_id = course_id
        self.title = title
        self.slug = slug
        self.date = date
        self.content = content
        self.thumbnail = thumbnail

class TrainingCenters(db.Model):
    __tablename__ = 'training_centers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    img = db.Column(db.String(100))
    address = db.Column(db.String(100))
    courses = db.relationship('Course', secondary=training_centers_courses, backref=db.backref('training_centers_list', lazy=True))
