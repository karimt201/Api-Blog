from flask import jsonify, request
from app import app, db
from app.models import Blog , Content , Category

@app.route('/home', methods=['GET'])
def Homepage():
    
    blog_list = Blog.query.all()
    blogs = []

    for blog in blog_list:
        blogs.append({
            'id' : blog.id,
            'img': blog.img,
            'title': blog.title,
            'description': blog.description,
            'keywords': blog.keywords,
            'user_id': blog.user_id
        })

    return jsonify({'blogs': blogs})

@app.route('/blogs', methods=['GET'])
def get_blogs():
    
    blog_list = Blog.query.all()
    blogs = []

    for blog in blog_list:
        blogs.append({
            'id' : blog.id,
            'img': blog.img,
            'title': blog.title,
            'description': blog.description,
            'date' : blog.date,
            'read_time' : blog.read_time,
            'keywords': blog.keywords,
            'Categorys': [{'id': category.id, 'title': category.title , 'description': category.description} for category in blog.Categorys],
            'contents': [{'id': content.id, 'title': content.title , 'description': content.description} for content in blog.contents],
            'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog.faqs],
            'user_id': blog.user_id
        })

    return jsonify({'blogs': blogs})

@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog_obj = Blog.query.filter_by(id=blog_id).first()

    blog = {
        'img': blog_obj.img,
        'title': blog_obj.title,
        'date' : blog_obj.date,
        'read_time' : blog_obj.read_time,
        'description': blog_obj.description,
        'keywords': blog_obj.keywords,
        'Categorys': [{'id': category.id, 'title': category.title , 'description': category.description} for category in blog_obj.Categorys],
        'contents': [{'id': content.id, 'title': content.title , 'description': content.description} for content in blog_obj.contents],
        'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog_obj.faqs],
        'user_id': blog_obj.user_id
    }
    
    return jsonify({'blog': blog})

@app.route('/contents', methods=['GET'])
def get_blogs_contents():
    
    content_lst = Content.query.all()
    contents = []

    for content in content_lst:
        contents.append({
            'id' : content.id,
            'title': content.title,
            'description': content.description,
            'blog_id': content.blog_id
        })

    return jsonify({'Content': contents})

@app.route('/categorys', methods=['GET'])
def get_blogs_categorys():
    
    category_lst = Category.query.all()
    categorys = []

    for category in category_lst:
        categorys.append({
            'id' : category.id,
            'title': category.title,
            'description': category.description,
            'blog_id': category.blog_id
        })

    return jsonify({'Category': categorys})

@app.route('/Relatedtopics', methods=['GET'])
def Related_topics():
    
    blog_list = Blog.query.all()
    blogs = []

    for blog in blog_list:
        blogs.append({
            'id' : blog.id,
            'img': blog.img,
            'title': blog.title,
            'keywords': blog.keywords,
            'user_id': blog.user_id
        })

    return jsonify({'blogs': blogs})


