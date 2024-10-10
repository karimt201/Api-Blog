from flask import Blueprint, jsonify, request
from app import db
from app.models import User

user_blueprint = Blueprint('users',__name__)


@user_blueprint.route('/users', methods=['GET', 'POST'])
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

