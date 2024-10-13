from flask import Blueprint, jsonify, request
from app.models import Course , Lesson , User
from app import db

course_blueprint = Blueprint('courses',__name__)


@course_blueprint.route('/courses', methods=['GET', 'POST'])
def handle_courses():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 2, type=int)
        
        search_query = request.args.get("search", "", type=str)

        query = Course.query

        if search_query:
            query = query.filter(Course.title.ilike(f"%{search_query}%"))
        
        courses_paginate = query.paginate(page=page, per_page=per_page, error_out=False)        
        
        courses_data = []
        
        for course in courses_paginate.items:
            user = User.query.get(course.user_id)
            courses_data.append({
                'id': course.id,
                'title': course.title,
                'rating': course.rating,
                'pricing': course.pricing,
                'brief': course.brief,
                'img': course.img,
                'requirements': course.requirements,
                'criteria': course.criteria,
                'content': course.content,
                'starting_date': course.starting_date,
                'end_date': course.end_date,
                'description': course.description,
                'icon': course.icon,
                'username': user.username,
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
                rating=data.get('rating'),
                pricing=data.get('pricing'),
                brief=data.get('brief'),
                img=data.get('img'),
                requirements=data.get('requirements'),
                criteria=data.get('criteria'),
                content=data.get('content'),
                starting_date=data.get('starting_date'),
                end_date=data.get('end_date'),
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

@course_blueprint.route('/courses/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'GET':
        user = User.query.get(course.user_id)
        course_data = {
            'id': course.id,
            'title': course.title,
            'rating': course.rating,
            'pricing': course.pricing,
            'brief': course.brief,
            'img': course.img,
            'requirements': course.requirements,
            'criteria': course.criteria,
            'content': course.content,
            'starting_date': course.starting_date,
            'end_date': course.end_date,
            'description': course.description,
            'icon': course.icon,
            'username': user.username,
            'lessons': [{'id': lesson.id, 'title': lesson.title, 'slug': lesson.slug} for lesson in course.lessons]
        }
        return jsonify({'course': course_data})

    elif request.method == 'PUT':
        data = request.get_json()
        try:
            course.title = data.get('title', course.title)
            course.rating = data.get('rating', course.rating)
            course.pricing = data.get('pricing', course.pricing)
            course.brief = data.get('brief', course.brief)
            course.img = data.get('img', course.img)
            course.requirements = data.get('requirements', course.requirements)
            course.criteria = data.get('criteria', course.criteria)
            course.content = data.get('content', course.content)
            course.starting_date = data.get('starting_date', course.starting_date)
            course.end_date = data.get('end_date', course.end_date)
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


@course_blueprint.route('/courses/<int:course_id>/lessons', methods=['GET', 'POST'])
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


@course_blueprint.route('/lessons', methods=['GET', 'POST'])
def get_lessons():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 4, type=int)
        
        search_query = request.args.get("search", "", type=str)

        query = Lesson.query

        if search_query:
            query = query.join(Course).join(User).filter(
                (Lesson.title.ilike(f"%{search_query}%")) |
                (Course.title.ilike(f"%{search_query}%")) |
                (User.username.ilike(f"%{search_query}%"))
            )
        
        lessons_paginate = query.paginate(page=page, per_page=per_page, error_out=False)

        lessons_data = []

        for lesson in lessons_paginate.items: 
            course = Course.query.get(lesson.course_id)
            user = User.query.get(course.user_id)
            
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
        
        return jsonify({'lessons': lessons_data, 'pagination': pagination})


@course_blueprint.route('/lessons/<int:lesson_id>', methods=['GET', 'PUT', 'DELETE'])
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
