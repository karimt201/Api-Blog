from flask import jsonify, request
from app import app , db 
from app.models import Blog , Content , Category , Faq , User , Course, Lesson
from flasgger import swag_from


@swag_from('./static/swagger.yaml')
@app.route('/home', methods=['GET'])
def Homepage():
    
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 2, type=int)
    
    blog_paginate = Blog.query.paginate(page=page, per_page=per_page, error_out=False)
    blogs = []

    for blog in blog_paginate:
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

@swag_from('./static/swagger.yaml')
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


@swag_from('./static/swagger.yaml')
@app.route('/blog/<int:blog_id>', methods=['GET', 'PUT', 'DELETE'])
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


@app.route('/users', methods=['GET', 'POST'])
def get_blogs_users():
    if request.method == 'GET':
        
        user_lst = User.query.all()
        users = []

        for user in user_lst:
            users.append({
                'id' : user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password,
                'img': user.img,
            })
            

        return jsonify({'users': users})
    
    elif request.method == 'POST':
        data = request.get_json()

        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            img=data['img']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'User created successfully'
        }), 201


@app.route('/categories', methods=['GET', 'POST'])
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

@app.route('/category/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_category(category_id):
    category = Category.query.get_or_404(category_id)

    if request.method == 'GET':
        category_data = {
            'id': category.id,
            'title': category.title,
            'description': category.description,
            'Blogs': [{
            'id' : blog.id,
            'img': blog.img,
            'title': blog.title,
            'description': blog.description,
            'keywords': blog.keywords,
            'user_id': blog.user_id} for blog in category.blogs],

        }
        return jsonify({'category': category_data})

    elif request.method == 'PUT':
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        category.title = data.get('title', category.title)
        category.description = data.get('description', category.description)

        try:
            db.session.commit()
            return jsonify({'message': 'Blog updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Blog deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500



@app.route('/blogs/<int:blog_id>/related-topics', methods=['GET'])
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

@swag_from('./static/swagger.yaml')
@app.route('/courses', methods=['GET', 'POST'])
def handle_courses():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 2, type=int)
        courses_paginate = Course.query.paginate(page=page, per_page=per_page, error_out=False)
        courses_data = []
        for course in courses_paginate:
            courses_data.append({
                'id': course.id,
                'title': course.title,
                'description': course.description,
                'icon': course.icon,
                'user_id': course.user_id,
                'lessons': [{'id': lesson.id, 'title': lesson.title, 'slug': lesson.slug} for lesson in course.lessons]
            })
        pagination = {
            "count": courses_paginate.total,
            "page": page,
            "per_page": per_page,
            "pages": courses_paginate.pages,
        }
        return jsonify({'courses': courses_data , 'pagination': pagination})

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_course = Course(
                title=data.get('title'),
                description=data.get('description'),
                icon=data.get('icon'),
                user_id=data.get('user_id')
            )
            db.session.add(new_course)
            db.session.commit()
            return jsonify({'message': 'Course created successfully', 'course_id': new_course.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@swag_from('./static/swagger.yaml')
@app.route('/courses/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'GET':
        course_data = {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'icon': course.icon,
            'user_id': course.user_id,
            'lessons': [{'id': lesson.id, 'title': lesson.title, 'slug': lesson.slug} for lesson in course.lessons]
        }
        return jsonify({'course': course_data})

    elif request.method == 'PUT':
        data = request.get_json()
        try:
            course.title = data.get('title', course.title)
            course.description = data.get('description', course.description)
            course.icon = data.get('icon', course.icon)
            db.session.commit()
            return jsonify({'message': 'Course updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(course)
            db.session.commit()
            return jsonify({'message': 'Course deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@swag_from('./static/swagger.yaml')
@app.route('/courses/<int:course_id>/lessons', methods=['GET', 'POST'])
def handle_lessons(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 4, type=int)
        lessons_paginate = Lesson.query.paginate(page=page, per_page=per_page, error_out=False)
    
        lessons_data = []

        for lesson in lessons_paginate:
            courses = Course.query.filter_by(id=lesson.course_id).all()
            for course in courses:
                users = User.query.filter_by(id=course.user_id).all()
                for user in users:
                    lessons_data.append({
                        'id': lesson.id,
                        'title': lesson.title,
                        'slug': lesson.slug,
                        'date': lesson.date,
                        'content': lesson.content,
                        'thumbnail': lesson.thumbnail,
                        'course_title': course.title,
                        'user_img': user.img,
                        'username': user.username,
                    })
                    
        pagination = {
            "count": lessons_paginate.total,
            "page": page,
            "per_page": per_page,
            "pages": lessons_paginate.pages,
        }
            
            
        return jsonify({'lessons': lessons_data ,  'pagination': pagination })

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_lesson = Lesson(
                course_id=course.id,
                title=data.get('title'),
                slug=data.get('slug'),
                date=data.get('date'),
                content=data.get('content'),
                thumbnail=data.get('thumbnail')
            )
            db.session.add(new_lesson)
            db.session.commit()
            return jsonify({'message': 'Lesson created successfully', 'lesson_id': new_lesson.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@swag_from('./static/swagger.yaml')
@app.route('/lessons', methods=['GET', 'POST'])
def get_lessons():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 4, type=int)
        lessons_paginate = Lesson.query.paginate(page=page, per_page=per_page, error_out=False)
    
        lessons_data = []

        for lesson in lessons_paginate:
            courses = Course.query.filter_by(id=lesson.course_id).all()
            for course in courses:
                users = User.query.filter_by(id=course.user_id).all()
                for user in users:
                    lessons_data.append({
                        'id': lesson.id,
                        'title': lesson.title,
                        'slug': lesson.slug,
                        'date': lesson.date,
                        'content': lesson.content,
                        'thumbnail': lesson.thumbnail,
                        'course_title': course.title,
                        'user_img': user.img,
                        'username': user.username,
                    })
                    
        pagination = {
            "count": lessons_paginate.total,
            "page": page,
            "per_page": per_page,
            "pages": lessons_paginate.pages,
        }
            
            
        return jsonify({'lessons': lessons_data ,  'pagination': pagination })

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_lesson = Lesson(
                course_id=course.id,
                title=data.get('title'),
                slug=data.get('slug'),
                date=data.get('date'),
                content=data.get('content'),
                thumbnail=data.get('thumbnail')
            )
            db.session.add(new_lesson)
            db.session.commit()
            return jsonify({'message': 'Lesson created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@swag_from('./static/swagger.yaml')
@app.route('/lessons/<int:lesson_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    if request.method == 'GET':
        lesson_data = {
            'id': lesson.id,
            'title': lesson.title,
            'slug': lesson.slug,
            'date': lesson.date,
            'content': lesson.content,
            'thumbnail': lesson.thumbnail,
            'course_id': lesson.course_id
        }
        return jsonify({'lesson': lesson_data})

    elif request.method == 'PUT':
        data = request.get_json()
        try:
            lesson.title = data.get('title', lesson.title)
            lesson.slug = data.get('slug', lesson.slug)
            lesson.slug = data.get('date', lesson.date)
            lesson.content = data.get('content', lesson.content)
            lesson.thumbnail = data.get('thumbnail', lesson.thumbnail)
            db.session.commit()
            return jsonify({'message': 'Lesson updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(lesson)
            db.session.commit()
            return jsonify({'message': 'Lesson deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
