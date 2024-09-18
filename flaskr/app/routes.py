from flask import jsonify, request
from app import app , db
from app.models import Blog , Content , Category , Faq


@app.route('/home', methods=['GET'])
def Homepage():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 2, type=int)
    
    blog_list = Blog.query.all()
    blog_paginate = Blog.query.paginate(page=page, per_page=per_page, error_out=False)
    blogs = []

    for blog in blog_list:
        blogs.append({
            'id' : blog.id,
            'img': blog.img,
            'title': blog.title,
            'description': blog.description,
            'keywords': blog.keywords,
            'user_id': blog.user_id,
        })
    pagination = {
        "count": blog_paginate.total,
        "page": page,
        "per_page": per_page,
        "pages": blog_paginate.pages,
    }
    

    return jsonify({'blogs': blogs , 'pagination': pagination})

@app.route('/blogs', methods=['GET', 'POST'])
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
    
    if request.method == 'POST':
        data = request.get_json()

        try:
            new_blog = Blog(
                img=data.get('img'),
                title=data.get('title'),
                description=data.get('description'),
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



@app.route('/blogs/<int:blog_id>', methods=['GET', 'PUT', 'DELETE'])
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
            'categories': [{'id': category.id, 'title': category.title , 'description': category.description} for category in blog.categories],            'contents': [{'id': content.id, 'title': content.title, 'description': content.description} for content in blog.contents],
            'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog.faqs],
            'user_id': blog.user_id
        }
        return jsonify({'blog': blog_data})

    elif request.method == 'PUT':
        data = request.get_json()
        blog.img = data.get('img', blog.img)
        blog.title = data.get('title', blog.title)
        blog.description = data.get('description', blog.description)
        blog.read_time = data.get('read_time', blog.read_time)
        blog.keywords = data.get('keywords', blog.keywords)
        
        if 'category_ids' in data:
            categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
            blog.categories = categories
        

        db.session.commit()

        return jsonify({'message': 'Blog updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(blog)
        db.session.commit()
        return jsonify({'message': 'Blog deleted successfully'}), 200


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

@app.route('/categorys', methods=['GET', 'POST'])
def handle_categories():
    if request.method == 'GET':
        category_lst = Category.query.all()
        categories = []

        for category in category_lst:
            categories.append({
                'id': category.id,
                'title': category.title,
                'description': category.description,
            })

        return jsonify({'categories': categories})

    elif request.method == 'POST':
        data = request.get_json()

        if not data or 'title' not in data or 'description' not in data:
            return jsonify({'error': 'Title and description are required'}), 400

        new_category = Category(
            title=data['title'],
            description=data['description']
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            'message': 'Category created successfully',
            'category': {
                'id': new_category.id,
                'title': new_category.title,
                'description': new_category.description,
            }
        }), 201

@app.route('/related-topics', methods=['GET'])
def related_topics():
    category_name = request.args.get('category', None)

    if category_name:
        blog_list = Blog.query.join(Blog.categories).filter(Category.title == category_name).limit(4).all()
    else:
        blog_list = Blog.query.limit(4).all()

    blogs = []

    for blog in blog_list:
        blogs.append({
            'id': blog.id,
            'img': blog.img,
            'title': blog.title,
            'keywords': blog.keywords,
            'user_id': blog.user_id
        })

    return jsonify({'blogs': blogs})
