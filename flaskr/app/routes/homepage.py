from flask import Blueprint, jsonify, request
from app.models import Blog

homepage_blueprint = Blueprint('homepage', __name__)

@homepage_blueprint.route('/home', methods=['GET'])
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