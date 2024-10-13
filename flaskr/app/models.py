from app import db
from sqlalchemy.dialects.postgresql import ARRAY

blog_category_association = db.Table('blog_category',
    db.Column('blog_id', db.Integer, db.ForeignKey('blogs.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

training_centers_courses = db.Table('training_centers_courses',
    db.Column('training_center_id', db.Integer, db.ForeignKey('training_centers.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
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
    events = db.relationship('Events', backref='author', lazy=True)


class Category(db.Model):
    __tablename__ = 'categories'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blogs = db.relationship('Blog', secondary=blog_category_association, back_populates='categories')

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

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

class Faq(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(50))
    pricing = db.Column(db.String(50))
    brief = db.Column(db.String(255))
    img = db.Column(db.String(255))
    requirements = db.Column(ARRAY(db.String(255)), default=[])
    criteria = db.Column(ARRAY(db.String(255)), default=[])
    content = db.Column(ARRAY(db.String(255)), default=[])
    starting_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    description = db.Column(db.Text)
    icon = db.Column(db.String(255))  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    lessons = db.relationship('Lesson', backref='course', lazy=True, cascade="all, delete-orphan")
    training_centers = db.relationship('Training_Centers', 
                                        secondary=training_centers_courses, 
                                        back_populates='courses')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(32), nullable=False)
    date = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(255)) 

class Training_Centers(db.Model):
    __tablename__ = 'training_centers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    img = db.Column(db.String(100))
    address = db.Column(db.String(100))
    courses = db.relationship('Course', 
                                secondary=training_centers_courses, 
                                back_populates='training_centers')

class Apply_form(db.Model):
    __tablename__ = 'apply_form'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    job = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50))  
    years_of_experience = db.Column(db.String(50), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)

class Cities(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    apply_forms = db.relationship('Apply_form', backref='city', lazy=True, cascade="all, delete-orphan")

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    icon = db.Column(db.String(100))
    img = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    date = db.Column(db.String(100))
    starting_time = db.Column(db.String(100))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    agenda = db.relationship('Agenda', backref='events', lazy=True , cascade='all, delete-orphan')
    speakers = db.relationship('Speakers', backref='events', lazy=True , cascade='all, delete-orphan')
    
class Speakers(db.Model):
    __tablename__ = 'speakers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    img = db.Column(db.String(100))
    Position = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)


class Agenda(db.Model):
    __tablename__ = 'agenda'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    agenda_type = db.Column(db.String(100))
    status = db.Column(db.String(100))
    starting_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    keywords = db.Column(ARRAY(db.String(255)), default=[])
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
