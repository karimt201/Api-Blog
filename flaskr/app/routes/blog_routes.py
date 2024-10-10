from flask import Blueprint, jsonify, request
from app.models import Blog, Category, Content, Faq
from app import db

blog_blueprint = Blueprint('blogs', __name__)


@blog_blueprint.route('/blogs', methods=['GET'])
def get_blogs():
    if request.method == 'GET':
        blog_list = Blog.query.all()
        blogs = []

        for blog in blog_list:
            blogs.append({
                'id': blog.id,
                'img': blog.img,
                'title': blog.title,
                'description': blog.description,
                'date': blog.date,
                'read_time': blog.read_time,
                'keywords': blog.keywords,
                'categories': [{'id': category.id, 'title': category.title} for category in blog.categories],                'contents': [{'id': content.id, 'title': content.title, 'description': content.description} for content in blog.contents],
                'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog.faqs],
                'user_id': blog.user_id
            })

        return jsonify({'blogs': blogs})


@blog_blueprint.route('/blog', methods=['POST'])
def post_blogs():    
    if request.method == 'POST':
        data = request.get_json()

        try:
            new_blog = Blog(
                img=data.get('img'),
                title=data.get('title'),
                description=data.get('description'),
                date=data.get('date'),
                read_time=data.get('read_time'),
                keywords=data.get('keywords', []),
                user_id=data.get('user_id')
            )
            
            if 'category_ids' in data:
                categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
                new_blog.categories = categories

            db.session.add(new_blog)
            db.session.flush()

            if 'contents' in data:
                for content_data in data['contents']:
                    new_content = Content(
                        title=content_data['title'],
                        description=content_data['description'],
                        blog_id=new_blog.id
                    )
                    db.session.add(new_content)

            if 'faqs' in data:
                for faq_data in data['faqs']:
                    new_faq = Faq(
                        question=faq_data['question'],
                        answer=faq_data['answer'],
                        blog_id=new_blog.id
                    )
                    db.session.add(new_faq)

            db.session.commit()

            return jsonify({'message': 'Blog created successfully', 'blog_id': new_blog.id}), 201

        except Exception as e:
            db.session.rollback()  
            return jsonify({'error': str(e)}), 500



@blog_blueprint.route('/blog/<int:blog_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if request.method == 'GET':
        blog_data = {
            'id': blog.id,
            'img': blog.img,
            'title': blog.title,
            'date': blog.date,
            'read_time': blog.read_time,
            'description': blog.description,
            'keywords': blog.keywords,
            'categories': [{'id': category.id, 'title': category.title, 'description': category.description} for category in blog.categories],
            'contents': [{'id': content.id, 'title': content.title, 'description': content.description} for content in blog.contents],
            'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog.faqs],
            'user_id': blog.user_id
        }
        return jsonify({'blog': blog_data})

    elif request.method == 'PUT':
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        blog.img = data.get('img', blog.img)
        blog.title = data.get('title', blog.title)
        blog.description = data.get('description', blog.description)
        blog.read_time = data.get('read_time', blog.read_time)
        blog.keywords = data.get('keywords', blog.keywords)

        if 'category_ids' in data:
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            blog.categories = categories

        try:
            db.session.commit()
            return jsonify({'message': 'Blog updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(blog)
            db.session.commit()
            return jsonify({'message': 'Blog deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        
@blog_blueprint.route('/blogs/<int:blog_id>/related-topics', methods=['GET'])
def related_topics(blog_id):
    try:
        blog = Blog.query.get_or_404(blog_id)
        blog_category = blog.categories[0]
        related_blogs = Blog.query.join(Blog.categories) \
                                .filter(Category.title == blog_category.title) \
                                .filter(Blog.id != blog_id) \
                                .limit(4) \
                                .all()

        related_blogs_data = [{
            'id': related_blog.id,
            'title': related_blog.title,
            'img': related_blog.img,
            'description': related_blog.description,  
            'keywords': related_blog.keywords,
            'user_id': related_blog.user_id
        } for related_blog in related_blogs]

        return jsonify({'related_blogs': related_blogs_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blog_blueprint.route('/contents', methods=['GET'])
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

