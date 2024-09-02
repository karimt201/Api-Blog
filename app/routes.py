from flask import jsonify, request
from app import app, db
from app.models import Blog, Header, Meta

@app.route('/', methods=['GET', 'POST'])
def add_get_blogs():
    if request.method == 'POST':

        data = request.json
        required_fields = ['img', 'title', 'description', 'user_id']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        blog_img = data['img']
        blog_title = data['title']
        blog_description = data['description']
        blog_user_id = data['user_id']

        new1_blog = Blog(blog_img, blog_title, blog_description, blog_user_id)
        db.session.add(new1_blog)
        db.session.commit()

        return jsonify({'message': 'Blog created successfully'}), 201

    blog_list = Blog.query.all()
    blogs = []

    for blog in blog_list:
        blogs.append({
            'img': blog.img,
            'title': blog.title,
            'description': blog.description,
            'header': [{
                'id': header.id,
                'title': header.title,
                'description': header.description,
                'image': header.image,
                'meta' :[{
                'id': meta.id,
                'category': meta.category,
                'read_time': meta.read_time,
                'date': meta.date}for meta in header.meta]
                } for header in blog.header],
            'contents': [{'id': content.id, 'title': content.title , 'description': content.description} for content in blog.contents],
            'keywords': [{'id': keyword.id, 'name': keyword.name} for keyword in blog.keywords],
            'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog.faqs],
            'topics': [{'id': topic.id, 'name': topic.title} for topic in blog.topics],
            'user_id': blog.user_id
        })

    return jsonify({'blogs': blogs})

@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog_obj = Blog.query.filter_by(id=blog_id).first()

    blog = {
        'img': blog_obj.img,
        'title': blog_obj.title,
        'description': blog_obj.description,
        'header': [{
            'id': header.id,
            'title': header.title,
            'description': header.description,
            'image': header.image,
            'meta' :[{
                'id': meta.id,
                'category': meta.category,
                'read_time': meta.read_time,
                'date': meta.date}for meta in header.meta]
            } for header in blog_obj.header],
        'contents': [{'id': content.id, 'title': content.title , 'description': content.description} for content in blog_obj.contents],
        'keywords': [{'id': keyword.id, 'name': keyword.name} for keyword in blog_obj.keywords],
        'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog_obj.faqs],
        'topics': [{'id': topic.id, 'name': topic.title} for topic in blog_obj.topics],
        'user_id': blog_obj.user_id
    }
    
    return jsonify({'blog': blog})
