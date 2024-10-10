# from flask import jsonify, request
# from app import app , db 
# from app.models import Blog , Content , Category , Faq , User , Course, Lesson , Training_Centers , Cities , Apply_form , Events , Speakers , Agenda


# @app.route('/home', methods=['GET'])
# def Homepage():
    
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per-page", 2, type=int)
    
#     blog_paginate = Blog.query.paginate(page=page, per_page=per_page, error_out=False)
#     blogs = []

#     for blog in blog_paginate:
#         blogs.append({
#             'id' : blog.id,
#             'img': blog.img,
#             'title': blog.title,
#             'description': blog.description,
#             'keywords': blog.keywords,
#             'user_id': blog.user_id,
#         })
#     pagination = {
#         "count": blog_paginate.total,
#         "page": page,
#         "per_page": per_page,
#         "pages": blog_paginate.pages,
#     }
    

#     return jsonify({'blogs': blogs , 'pagination': pagination})

# @app.route('/blogs', methods=['GET'])
# def get_blogs():
#     if request.method == 'GET':
#         blog_list = Blog.query.all()
#         blogs = []

#         for blog in blog_list:
#             blogs.append({
#                 'id': blog.id,
#                 'img': blog.img,
#                 'title': blog.title,
#                 'description': blog.description,
#                 'date': blog.date,
#                 'read_time': blog.read_time,
#                 'keywords': blog.keywords,
#                 'categories': [{'id': category.id, 'title': category.title} for category in blog.categories],                'contents': [{'id': content.id, 'title': content.title, 'description': content.description} for content in blog.contents],
#                 'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog.faqs],
#                 'user_id': blog.user_id
#             })

#         return jsonify({'blogs': blogs})


# @app.route('/blog', methods=['POST'])
# def post_blogs():    
#     if request.method == 'POST':
#         data = request.get_json()

#         try:
#             new_blog = Blog(
#                 img=data.get('img'),
#                 title=data.get('title'),
#                 description=data.get('description'),
#                 date=data.get('date'),
#                 read_time=data.get('read_time'),
#                 keywords=data.get('keywords', []),
#                 user_id=data.get('user_id')
#             )
            
#             if 'category_ids' in data:
#                 categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
#                 new_blog.categories = categories

#             db.session.add(new_blog)
#             db.session.flush()

#             if 'contents' in data:
#                 for content_data in data['contents']:
#                     new_content = Content(
#                         title=content_data['title'],
#                         description=content_data['description'],
#                         blog_id=new_blog.id
#                     )
#                     db.session.add(new_content)

#             if 'faqs' in data:
#                 for faq_data in data['faqs']:
#                     new_faq = Faq(
#                         question=faq_data['question'],
#                         answer=faq_data['answer'],
#                         blog_id=new_blog.id
#                     )
#                     db.session.add(new_faq)

#             db.session.commit()

#             return jsonify({'message': 'Blog created successfully', 'blog_id': new_blog.id}), 201

#         except Exception as e:
#             db.session.rollback()  
#             return jsonify({'error': str(e)}), 500



# @app.route('/blog/<int:blog_id>', methods=['GET', 'PUT', 'DELETE'])
# def handle_blog(blog_id):
#     blog = Blog.query.get_or_404(blog_id)

#     if request.method == 'GET':
#         blog_data = {
#             'id': blog.id,
#             'img': blog.img,
#             'title': blog.title,
#             'date': blog.date,
#             'read_time': blog.read_time,
#             'description': blog.description,
#             'keywords': blog.keywords,
#             'categories': [{'id': category.id, 'title': category.title, 'description': category.description} for category in blog.categories],
#             'contents': [{'id': content.id, 'title': content.title, 'description': content.description} for content in blog.contents],
#             'faqs': [{'id': faq.id, 'question': faq.question, 'answer': faq.answer} for faq in blog.faqs],
#             'user_id': blog.user_id
#         }
#         return jsonify({'blog': blog_data})

#     elif request.method == 'PUT':
#         data = request.get_json()
        
#         if not data:
#             return jsonify({'error': 'No input data provided'}), 400
        
#         blog.img = data.get('img', blog.img)
#         blog.title = data.get('title', blog.title)
#         blog.description = data.get('description', blog.description)
#         blog.read_time = data.get('read_time', blog.read_time)
#         blog.keywords = data.get('keywords', blog.keywords)

#         if 'category_ids' in data:
#             categories = Category.query.filter(Category.id.in_(data['category_ids'])).all()
#             blog.categories = categories

#         try:
#             db.session.commit()
#             return jsonify({'message': 'Blog updated successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(blog)
#             db.session.commit()
#             return jsonify({'message': 'Blog deleted successfully'}), 200
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500


# @app.route('/users', methods=['GET', 'POST'])
# def get_blogs_users():
#     if request.method == 'GET':
        
#         user_lst = User.query.all()
#         users = []

#         for user in user_lst:
#             users.append({
#                 'id' : user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'password': user.password,
#                 'img': user.img,
#             })
            

#         return jsonify({'users': users})
    
#     elif request.method == 'POST':
#         data = request.get_json()

#         new_user = User(
#             username=data['username'],
#             email=data['email'],
#             password=data['password'],
#             img=data['img']
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({
#             'message': 'User created successfully'
#         }), 201


# @app.route('/categories', methods=['GET', 'POST'])
# def handle_categories():
#     if request.method == 'GET':
#         category_lst = Category.query.all()
#         categories = []

#         for category in category_lst:
#             categories.append({
#                 'id': category.id,
#                 'title': category.title,
#                 'description': category.description,
#             })

#         return jsonify({'categories': categories})

#     elif request.method == 'POST':
#         data = request.get_json()

#         new_category = Category(
#             title=data['title'],
#             description=data['description']
#         )

#         db.session.add(new_category)
#         db.session.commit()

#         return jsonify({
#             'message': 'Category created successfully',
#             'category': {
#                 'id': new_category.id,
#                 'title': new_category.title,
#                 'description': new_category.description,
#             }
#         }), 201


# @app.route('/category/<int:category_id>/blogs', methods=['GET'])
# def handle_blogs(category_id):
#     if request.method == 'GET':
#         page = request.args.get("page", 1, type=int)
#         per_page = request.args.get("per-page", 4, type=int)
        
#         blogs_paginate = Blog.query.filter(Blog.categories.any(id=category_id)).paginate(page=page, per_page=per_page, error_out=False)        
#         blogs_data = []
#         for blog in blogs_paginate.items:
#             blogs_data.append({
#                 'id': blog.id,
#                 'img': blog.img,
#                 'title': blog.title,
#                 'description': blog.description,
#                 'keywords': blog.keywords,
#                 'user_id': blog.user_id
#             })
        
#         pagination = {
#             "count": blogs_paginate.total,
#             "page": page,
#             "per_page": per_page,
#             "pages": blogs_paginate.pages,
#         }
        
#         return jsonify({'blogs': blogs_data, 'pagination': pagination})


# @app.route('/category/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
# def handle_category(category_id):
#     category = Category.query.get_or_404(category_id)

#     if request.method == 'GET':
#         category_data = {
#             'id': category.id,
#             'title': category.title,
#             'description': category.description,
#             'Blogs': [{
#             'id' : blog.id,
#             'img': blog.img,
#             'title': blog.title,
#             'description': blog.description,
#             'keywords': blog.keywords,
#             'user_id': blog.user_id} for blog in category.blogs],

#         }
#         return jsonify({'category': category_data})

#     elif request.method == 'PUT':
#         data = request.get_json()
        
#         if not data:
#             return jsonify({'error': 'No input data provided'}), 400
        
#         category.title = data.get('title', category.title)
#         category.description = data.get('description', category.description)

#         try:
#             db.session.commit()
#             return jsonify({'message': 'Blog updated successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(category)
#             db.session.commit()
#             return jsonify({'message': 'Blog deleted successfully'}), 200
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500



# @app.route('/blogs/<int:blog_id>/related-topics', methods=['GET'])
# def related_topics(blog_id):
#     try:
#         blog = Blog.query.get_or_404(blog_id)
#         blog_category = blog.categories[0]
#         related_blogs = Blog.query.join(Blog.categories) \
#                                 .filter(Category.title == blog_category.title) \
#                                 .filter(Blog.id != blog_id) \
#                                 .limit(4) \
#                                 .all()

#         related_blogs_data = [{
#             'id': related_blog.id,
#             'title': related_blog.title,
#             'img': related_blog.img,
#             'description': related_blog.description,  
#             'keywords': related_blog.keywords,
#             'user_id': related_blog.user_id
#         } for related_blog in related_blogs]

#         return jsonify({'related_blogs': related_blogs_data})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @app.route('/contents', methods=['GET'])
# def get_blogs_contents():
    
#     content_lst = Content.query.all()
#     contents = []

#     for content in content_lst:
#         contents.append({
#             'id' : content.id,
#             'title': content.title,
#             'description': content.description,
#             'blog_id': content.blog_id
#         })

#     return jsonify({'Content': contents})


# @app.route('/courses', methods=['GET', 'POST'])
# def handle_courses():
#     if request.method == 'GET':
#         page = request.args.get("page", 1, type=int)
#         per_page = request.args.get("per-page", 2, type=int)
        
#         search_query = request.args.get("search", "", type=str)

#         query = Course.query

#         if search_query:
#             query = query.filter(Course.title.ilike(f"%{search_query}%"))
        
#         courses_paginate = query.paginate(page=page, per_page=per_page, error_out=False)        
        
#         courses_data = []
        
#         for course in courses_paginate.items:
#             user = User.query.get(course.user_id)
#             courses_data.append({
#                 'id': course.id,
#                 'title': course.title,
#                 'rating': course.rating,
#                 'pricing': course.pricing,
#                 'brief': course.brief,
#                 'img': course.img,
#                 'requirements': course.requirements,
#                 'criteria': course.criteria,
#                 'content': course.content,
#                 'starting_date': course.starting_date,
#                 'end_date': course.end_date,
#                 'description': course.description,
#                 'icon': course.icon,
#                 'username': user.username,
#                 'lessons': [{'id': lesson.id, 'title': lesson.title, 'slug': lesson.slug} for lesson in course.lessons]
#             })
        
#         pagination = {
#             "count": courses_paginate.total,
#             "page": page,
#             "per_page": per_page,
#             "pages": courses_paginate.pages,
#         }
        
#         return jsonify({'courses': courses_data , 'pagination': pagination})

#     elif request.method == 'POST':
#         data = request.get_json()
#         try:
#             new_course = Course(
#                 title=data.get('title'),
#                 rating=data.get('rating'),
#                 pricing=data.get('pricing'),
#                 brief=data.get('brief'),
#                 img=data.get('img'),
#                 requirements=data.get('requirements'),
#                 criteria=data.get('criteria'),
#                 content=data.get('content'),
#                 starting_date=data.get('starting_date'),
#                 end_date=data.get('end_date'),
#                 description=data.get('description'),
#                 icon=data.get('icon'),
#                 user_id=data.get('user_id')
#             )
#             db.session.add(new_course)
#             db.session.commit()
#             return jsonify({'message': 'Course created successfully', 'course_id': new_course.id}), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

# @app.route('/courses/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
# def handle_course(course_id):
#     course = Course.query.get_or_404(course_id)

#     if request.method == 'GET':
#         course_data = {
#             'id': course.id,
#             'title': course.title,
#             'rating': course.rating,
#             'pricing': course.pricing,
#             'brief': course.brief,
#             'img': course.img,
#             'requirements': course.requirements,
#             'criteria': course.criteria,
#             'content': course.content,
#             'starting_date': course.starting_date,
#             'end_date': course.end_date,
#             'description': course.description,
#             'icon': course.icon,
#             'user_id': course.user_id,
#             'lessons': [{'id': lesson.id, 'title': lesson.title, 'slug': lesson.slug} for lesson in course.lessons]
#         }
#         return jsonify({'course': course_data})

#     elif request.method == 'PUT':
#         data = request.get_json()
#         try:
#             course.title = data.get('title', course.title)
#             course.rating = data.get('rating', course.rating)
#             course.pricing = data.get('pricing', course.pricing)
#             course.brief = data.get('brief', course.brief)
#             course.img = data.get('img', course.img)
#             course.requirements = data.get('requirements', course.requirements)
#             course.criteria = data.get('criteria', course.criteria)
#             course.content = data.get('content', course.content)
#             course.starting_date = data.get('starting_date', course.starting_date)
#             course.end_date = data.get('end_date', course.end_date)
#             course.description = data.get('description', course.description)
#             course.icon = data.get('icon', course.icon)
#             db.session.commit()
#             return jsonify({'message': 'Course updated successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(course)
#             db.session.commit()
#             return jsonify({'message': 'Course deleted successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500


# @app.route('/courses/<int:course_id>/lessons', methods=['GET', 'POST'])
# def handle_lessons(course_id):
#     course = Course.query.get_or_404(course_id)

#     if request.method == 'GET':
#         page = request.args.get("page", 1, type=int)
#         per_page = request.args.get("per-page", 4, type=int)
#         lessons_paginate = Lesson.query.paginate(page=page, per_page=per_page, error_out=False)
    
#         lessons_data = []

#         for lesson in lessons_paginate:
#             courses = Course.query.filter_by(id=lesson.course_id).all()
#             for course in courses:
#                 users = User.query.filter_by(id=course.user_id).all()
#                 for user in users:
#                     lessons_data.append({
#                         'id': lesson.id,
#                         'title': lesson.title,
#                         'slug': lesson.slug,
#                         'date': lesson.date,
#                         'content': lesson.content,
#                         'thumbnail': lesson.thumbnail,
#                         'course_title': course.title,
#                         'user_img': user.img,
#                         'username': user.username,
#                     })
                    
#         pagination = {
#             "count": lessons_paginate.total,
#             "page": page,
#             "per_page": per_page,
#             "pages": lessons_paginate.pages,
#         }
            
            
#         return jsonify({'lessons': lessons_data ,  'pagination': pagination })

#     elif request.method == 'POST':
#         data = request.get_json()
#         try:
#             new_lesson = Lesson(
#                 course_id=course.id,
#                 title=data.get('title'),
#                 slug=data.get('slug'),
#                 date=data.get('date'),
#                 content=data.get('content'),
#                 thumbnail=data.get('thumbnail')
#             )
#             db.session.add(new_lesson)
#             db.session.commit()
#             return jsonify({'message': 'Lesson created successfully', 'lesson_id': new_lesson.id}), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500


# @app.route('/lessons', methods=['GET', 'POST'])
# def get_lessons():
#     if request.method == 'GET':
#         page = request.args.get("page", 1, type=int)
#         per_page = request.args.get("per-page", 4, type=int)
        
#         search_query = request.args.get("search", "", type=str)

#         query = Lesson.query

#         if search_query:
#             query = query.join(Course).join(User).filter(
#                 (Lesson.title.ilike(f"%{search_query}%")) |
#                 (Course.title.ilike(f"%{search_query}%")) |
#                 (User.username.ilike(f"%{search_query}%"))
#             )
        
#         lessons_paginate = query.paginate(page=page, per_page=per_page, error_out=False)

#         lessons_data = []

#         for lesson in lessons_paginate.items: 
#             course = Course.query.get(lesson.course_id)
#             user = User.query.get(course.user_id)
            
#             lessons_data.append({
#                 'id': lesson.id,
#                 'title': lesson.title,
#                 'slug': lesson.slug,
#                 'date': lesson.date,
#                 'content': lesson.content,
#                 'thumbnail': lesson.thumbnail,
#                 'course_title': course.title,
#                 'user_img': user.img,
#                 'username': user.username,
#             })
                    
#         pagination = {
#             "count": lessons_paginate.total,
#             "page": page,
#             "per_page": per_page,
#             "pages": lessons_paginate.pages,
#         }
        
#         return jsonify({'lessons': lessons_data, 'pagination': pagination})


# @app.route('/lessons/<int:lesson_id>', methods=['GET', 'PUT', 'DELETE'])
# def handle_lesson(lesson_id):
#     lesson = Lesson.query.get_or_404(lesson_id)

#     if request.method == 'GET':
#         lesson_data = {
#             'id': lesson.id,
#             'title': lesson.title,
#             'slug': lesson.slug,
#             'date': lesson.date,
#             'content': lesson.content,
#             'thumbnail': lesson.thumbnail,
#             'course_id': lesson.course_id
#         }
#         return jsonify({'lesson': lesson_data})

#     elif request.method == 'PUT':
#         data = request.get_json()
#         try:
#             lesson.title = data.get('title', lesson.title)
#             lesson.slug = data.get('slug', lesson.slug)
#             lesson.slug = data.get('date', lesson.date)
#             lesson.content = data.get('content', lesson.content)
#             lesson.thumbnail = data.get('thumbnail', lesson.thumbnail)
#             db.session.commit()
#             return jsonify({'message': 'Lesson updated successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(lesson)
#             db.session.commit()
#             return jsonify({'message': 'Lesson deleted successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500
        
# @app.route('/training-centers', methods=['GET', 'POST'])
# def handle_training_centers():
#     if request.method == 'GET':
#         page = request.args.get("page", 1, type=int)
#         per_page = request.args.get("per-page", 2, type=int)
#         search_query = request.args.get("search", "", type=str)

#         query = Training_Centers.query

#         if search_query:
#             query = query.filter(Training_Centers.title.ilike(f"%{search_query}%"))
        
#         center_paginate = query.paginate(page=page, per_page=per_page, error_out=False)        

#         centers_data = []
#         for center in center_paginate:
#             centers_data.append({
#                 'id': center.id,
#                 'title': center.title,
#                 'location': center.location,
#                 'img': center.img,
#                 'address': center.address,
#                 'courses': [{'id': course.id, 'title': course.title} for course in center.courses]
#             })
            
#         pagination = {
#             "count": center_paginate.total,
#             "page": page,
#             "per_page": per_page,
#             "pages": center_paginate.pages,
#         }
            
#         return jsonify({'training_centers': centers_data , 'pagination': pagination})

#     elif request.method == 'POST':
#         data = request.get_json()
#         try:
#             new_center = Training_Centers(
#                 title=data['title'],
#                 location=data['location'],
#                 img=data['img'],
#                 address=data['address']
#             )
            
#             if 'course_ids' in data:
#                 courses = Course.query.filter(Course.id.in_(data['course_ids'])).all()
#                 new_center.courses = courses

#             db.session.add(new_center)
#             db.session.commit()
#             return jsonify({'message': 'Training center created successfully', 'id': new_center.id}), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500


# @app.route('/training-centers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def handle_training_center(id):
#     center = Training_Centers.query.get_or_404(id)

#     if request.method == 'GET':
#         center_data = {
#             'id': center.id,
#             'title': center.title,
#             'location': center.location,
#             'img': center.img,
#             'address': center.address,
#             'courses': [{'id': course.id, 'title': course.title} for course in center.courses]
#         }
#         return jsonify({'training_center': center_data})

#     elif request.method == 'PUT':
#         data = request.get_json()
#         try:
#             center.title = data.get('title', center.title)
#             center.location = data.get('location', center.location)
#             center.img = data.get('img', center.img)
#             center.address = data.get('address', center.address)
            
#             if 'course_ids' in data:
#                 courses = Course.query.filter(Course.id.in_(data['course_ids'])).all()
#                 center.courses = courses

#             db.session.commit()
#             return jsonify({'message': 'Training center updated successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#     elif request.method == 'DELETE':
#         try:
#             db.session.delete(center)
#             db.session.commit()
#             return jsonify({'message': 'Training center deleted successfully'})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

# @app.route('/cities', methods=['GET'])
# def get_cities():
#     search_query = request.args.get("search", "", type=str)

#     query = Cities.query

#     if search_query:
#         query = query.filter(
#             (Cities.title.ilike(f"%{search_query}%"))
#         )
        
#     cities = query.all()


#     result = [{'id': city.id, 'title': city.title} for city in cities]
#     return jsonify(result), 200

# @app.route('/city', methods=['POST'])
# def add_city():
#     data = request.get_json()

#     if isinstance(data, list):
#         created_cities = []
#         try:
#             for city_data in data:
#                 title = city_data.get('title')

#                 if not title:
#                     return jsonify({'error': 'Title is required for each city'}), 400

#                 new_city = Cities(title=title)
#                 db.session.add(new_city)
#                 db.session.commit()

#                 created_cities.append({
#                     'id': new_city.id,
#                     'title': new_city.title
#                 })

#             return jsonify({
#                 'message': 'Cities created successfully',
#                 'cities': created_cities
#             }), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500
#     else:
#         title = data.get('title')

#         if not title:
#             return jsonify({'error': 'Title is required'}), 400

#         new_city = Cities(title=title)

#         try:
#             db.session.add(new_city)
#             db.session.commit()
#             return jsonify({
#                 'message': 'City created successfully',
#                 'city': {'id': new_city.id, 'title': new_city.title}
#             }), 201
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500
    
# import csv
# import os
# CSV_FILE_PATH = 'apply_forms_data.csv'

# def initialize_csv():
#     if not os.path.exists(CSV_FILE_PATH):
#         with open(CSV_FILE_PATH, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['id', 'name', 'phone_number', 'job', 'gender', 'years_of_experience', 'Location'])

# def append_to_csv(apply_form):
#     initialize_csv()

#     with open(CSV_FILE_PATH, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         city = apply_form.city

#         writer.writerow([
#             apply_form.id,
#             apply_form.name,
#             apply_form.phone_number,
#             apply_form.job,
#             apply_form.gender,
#             apply_form.years_of_experience,
#             city.title
#         ])

# @app.route('/apply_form', methods=['GET', 'POST'])
# def handle_apply_forms():
#     if request.method == 'GET':
#         apply_form_lst = Apply_form.query.all()
#         apply_forms = []

#         for form in apply_form_lst:
#             city = form.city 
#             apply_forms.append({
#                 'id': form.id,
#                 'name': form.name,
#                 'phone_number': form.phone_number,
#                 'job': form.job,
#                 'gender': form.gender,
#                 'years_of_experience': form.years_of_experience,
#                 'city': {'id': city.id, 'title': city.title} if city else None
#             })

#         return jsonify({'apply_forms': apply_forms})

#     elif request.method == 'POST':
#         data = request.get_json()

#         new_apply_form = Apply_form(
#             name=data['name'],
#             phone_number=data['phone_number'],
#             job=data['job'],
#             gender=data['gender'],
#             years_of_experience=data['years_of_experience'],
#             location_id=data['location_id']
#         )

#         db.session.add(new_apply_form)
#         db.session.commit()
        
#         append_to_csv(new_apply_form)


#         return jsonify({
#             'message': 'Apply_form created successfully',
#             'apply_form': {
#                 'id': new_apply_form.id,
#                 'name': new_apply_form.name,
#                 'phone_number': new_apply_form.phone_number,
#                 'job': new_apply_form.job,
#                 'gender': new_apply_form.gender,
#                 'years_of_experience': new_apply_form.years_of_experience,
#                 'location_id': new_apply_form.location_id,
#             }
#         }), 201

# @app.route('/events' , methods = ['GET','POST'])
# def get_events():
#     if request.method == 'GET':
#         event_list = Events.query.all()
#         events = []
        
#         for event in event_list:
#             events.append({
#                 'id' : event.id,
#                 'title' : event.title,
#                 'icon' : event.icon,
#                 'subtitle' : event.subtitle,
#                 'date' : event.date,
#                 'starting_time' : event.starting_time,
#                 'description' : event.description,
#                 'user_id' : event.user_id,
#                 })
#         return jsonify({'events' : events})
    
#     elif request.method == 'POST':
#         data = request.get_json()
        
#         new_event = Events(
#             title = data['title'], 
#             icon = data['icon'], 
#             subtitle = data['subtitle'], 
#             date = data['date'], 
#             starting_time = data['starting_time'], 
#             description = data['description'], 
#             user_id = data['user_id'], 
#         )
        
#         db.session.add(new_event)
#         db.session.commit()
        
#         return jsonify({
#             'message' : 'event created successfully'
#         }),201
    
# @app.route('/events/<int:event_id>', methods = ['GET','PUT','DELETE'])
# def handle_event(event_id):
#     event = Events.query.get_or_404(event_id)
    
#     if request.method == 'GET':
#         event_data = {
#                 'id' : event.id,
#                 'title' : event.title,
#                 'icon' : event.icon,
#                 'subtitle' : event.subtitle,
#                 'date' : event.date,
#                 'starting_time' : event.starting_time,
#                 'description' : event.description,
#                 'user_id' : event.user_id,
#                 'agenda' : [{
#                     'title' : agenda.title,
#                     'agenda_type' : agenda.agenda_type,
#                     'status' : agenda.status,
#                     'starting_date' : agenda.starting_date,
#                     'end_date' : agenda.end_date,
#                     'keywords' : agenda.keywords,
#                     }for agenda in event.agenda],
#                 'speakers' : [{
#                     'name' : speaker.name,
#                     'img' : speaker.img,
#                     'Position' : speaker.Position,
#                     'company_name' : speaker.company_name,
#                     }for speaker in event.speakers],  
#                 }
#         return jsonify({'event': event_data})
    
#     elif request.method == 'PUT':
#         data = request.get_json()
#         event.title = data.get('title', event.title)
#         event.icon = data.get('icon', event.icon)
#         event.subtitle = data.get('subtitle', event.subtitle)
#         event.date = data.get('date', event.date)
#         event.starting_time = data.get('starting_time', event.starting_time)
#         event.description = data.get('description', event.description)

#         db.session.commit()
#         return jsonify({'message': 'Event updated successfully'})

#     elif request.method == 'DELETE':
#         db.session.delete(event)
#         db.session.commit()
#         return jsonify({'message': 'Event deleted successfully'})

# @app.route('/speakers' , methods =['GET','POST'])
# def get_post_speakers():
#     if request.method == 'GET':
        
#         speaker_list = Speakers.query.all()
#         speakers = []
        
#         for speaker in speaker_list :
#             speakers.append({
#                 'id' : speaker.id,
#                 'name' : speaker.name,
#                 'img' : speaker.img,
#                 'position' : speaker.Position,
#                 'company_name' : speaker.company_name,
#                 'event_id' : speaker.event_id,
#             })
#         return jsonify({'speakers' : speakers})
    
#     elif request.method == 'POST' :
#         data = request.get_json()
        
#         new_speaker = Speakers(
#             name = data['name'],
#             img = data['img'],
#             Position = data['position'],
#             company_name = data['company_name'],
#             event_id = data['event_id']
#         )
        
#         db.session.add(new_speaker)
#         db.session.commit()
        
#         return jsonify({'message' : 'speaker created successfully'}),201
    


# @app.route('/agenda' , methods =['GET','POST'])
# def get_post_agenda():
#     if request.method == 'GET':
        
#         agenda_list = Agenda.query.all()
#         agendas = []
        
#         for agenda in agenda_list :
#             agendas.append({
#                 'id' : agenda.id,
#                 'title' : agenda.title,
#                 'agenda_type' : agenda.agenda_type,
#                 'status' : agenda.status,
#                 'starting_date' : agenda.starting_date,
#                 'end_date' : agenda.end_date,
#                 'keywords' : agenda.keywords,
#                 'event_id' : agenda.event_id,
#             })
#         return jsonify({'agendas' : agendas})
    
#     elif request.method == 'POST' :
#         data = request.get_json()
        
#         new_agenda = Agenda(
#             title = data['title'],
#             agenda_type = data['agenda_type'],
#             status = data['status'],
#             starting_date = data['starting_date'],
#             end_date = data['end_date'],
#             keywords = data['keywords'],
#             event_id = data['event_id']
#         )
        
#         db.session.add(new_agenda)
#         db.session.commit()
        
#         return jsonify({'message' : 'agenda created successfully'}),201
    
