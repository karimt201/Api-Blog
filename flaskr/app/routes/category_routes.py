from flask import Blueprint, jsonify, request
from app.models import Category , Blog
from app import db

category_blueprint = Blueprint('categories',__name__)

@category_blueprint.route('/categories', methods=['GET', 'POST'])
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


@category_blueprint.route('/category/<int:category_id>/blogs', methods=['GET'])
def handle_blogs(category_id):
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 4, type=int)
        
        blogs_paginate = Blog.query.filter(Blog.categories.any(id=category_id)).paginate(page=page, per_page=per_page, error_out=False)        
        blogs_data = []
        for blog in blogs_paginate.items:
            blogs_data.append({
                'id': blog.id,
                'img': blog.img,
                'title': blog.title,
                'description': blog.description,
                'keywords': blog.keywords,
                'user_id': blog.user_id
            })
        
        pagination = {
            "count": blogs_paginate.total,
            "page": page,
            "per_page": per_page,
            "pages": blogs_paginate.pages,
        }
        
        return jsonify({'blogs': blogs_data, 'pagination': pagination})


@category_blueprint.route('/category/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
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
