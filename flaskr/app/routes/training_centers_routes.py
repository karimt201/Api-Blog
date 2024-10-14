from flask import Blueprint, jsonify, request
from app.models import Training_Centers , Cities , Course , Apply_form
from app import db

training_centers_blueprint = Blueprint('training_centers', __name__)


@training_centers_blueprint.route('/training-centers', methods=['GET', 'POST'])
def handle_training_centers():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 2, type=int)
        search_query = request.args.get("search", "", type=str)

        query = Training_Centers.query

        if search_query:
            query = query.filter(Training_Centers.title.ilike(f"%{search_query}%"))
        
        center_paginate = query.paginate(page=page, per_page=per_page, error_out=False)        

        centers_data = []
        for center in center_paginate:
            centers_data.append({
                'id': center.id,
                'title': center.title,
                'location': center.location,
                'img': center.img,
                'address': center.address,
                'courses': [{'id': course.id, 'title': course.title} for course in center.courses]
            })
            
        pagination = {
            "count": center_paginate.total,
            "page": page,
            "per_page": per_page,
            "pages": center_paginate.pages,
        }
            
        return jsonify({'training_centers': centers_data , 'pagination': pagination})

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_center = Training_Centers(
                title=data['title'],
                location=data['location'],
                img=data['img'],
                address=data['address']
            )
            
            if 'course_ids' in data:
                courses = Course.query.filter(Course.id.in_(data['course_ids'])).all()
                new_center.courses = courses

            db.session.add(new_center)
            db.session.commit()
            return jsonify({'message': 'Training center created successfully', 'id': new_center.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@training_centers_blueprint.route('/training-centers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_training_center(id):
    center = Training_Centers.query.get_or_404(id)

    if request.method == 'GET':
        center_data = {
            'id': center.id,
            'title': center.title,
            'location': center.location,
            'img': center.img,
            'address': center.address,
            'courses': [{'id': course.id, 'title': course.title} for course in center.courses]
        }
        return jsonify({'training_center': center_data})

    elif request.method == 'PUT':
        data = request.get_json()
        try:
            center.title = data.get('title', center.title)
            center.location = data.get('location', center.location)
            center.img = data.get('img', center.img)
            center.address = data.get('address', center.address)
            
            if 'course_ids' in data:
                courses = Course.query.filter(Course.id.in_(data['course_ids'])).all()
                center.courses = courses

            db.session.commit()
            return jsonify({'message': 'Training center updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(center)
            db.session.commit()
            return jsonify({'message': 'Training center deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@training_centers_blueprint.route('/cities', methods=['GET'])
def get_cities():
    search_query = request.args.get("search", "", type=str)

    query = Cities.query

    if search_query:
        query = query.filter(
            (Cities.title.ilike(f"%{search_query}%"))
        )
        
    cities = query.all()


    result = [{'id': city.id, 'title': city.title} for city in cities]
    return jsonify(result), 200

@training_centers_blueprint.route('/city', methods=['POST'])
def add_city():
    data = request.get_json()

    if isinstance(data, list):
        created_cities = []
        try:
            for city_data in data:
                title = city_data.get('title')

                if not title:
                    return jsonify({'error': 'Title is required for each city'}), 400

                new_city = Cities(title=title)
                db.session.add(new_city)
                db.session.commit()

                created_cities.append({
                    'id': new_city.id,
                    'title': new_city.title
                })

            return jsonify({
                'message': 'Cities created successfully',
                'cities': created_cities
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        title = data.get('title')

        if not title:
            return jsonify({'error': 'Title is required'}), 400

        new_city = Cities(title=title)

        try:
            db.session.add(new_city)
            db.session.commit()
            return jsonify({
                'message': 'City created successfully',
                'city': {'id': new_city.id, 'title': new_city.title}
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
import csv
import os
CSV_FILE_PATH = 'apply_forms_data.csv'

def initialize_csv():
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'phone number', 'job', 'gender', 'email', 'employment states', 'Location'])

def append_to_csv(apply_form):
    initialize_csv()

    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        city = apply_form.city

        writer.writerow([
            apply_form.id,
            apply_form.name,
            apply_form.phone_number,
            apply_form.job,
            apply_form.gender,
            apply_form.email,
            apply_form.employment_states,
            city.title
        ])

@training_centers_blueprint.route('/apply-form', methods=['GET', 'POST'])
def handle_apply_forms():
    if request.method == 'GET':
        apply_form_lst = Apply_form.query.all()
        apply_forms = []

        for form in apply_form_lst:
            city = form.city 
            apply_forms.append({
                'id': form.id,
                'name': form.name,
                'phone_number': form.phone_number,
                'job': form.job,
                'gender': form.gender,
                'email': form.email,
                'employment_states': form.employment_states,
                'city': {'id': city.id, 'title': city.title} if city else None
            })

        return jsonify({'apply_forms': apply_forms})

    elif request.method == 'POST':
        data = request.get_json()

        new_apply_form = Apply_form(
            name=data['name'],
            phone_number=data['phone_number'],
            job=data['job'],
            gender=data['gender'],
            email=data['email'],
            employment_states=data['employment_states'],
            location_id=data['location_id']
        )

        db.session.add(new_apply_form)
        db.session.commit()
        
        append_to_csv(new_apply_form)


        return jsonify({
            'message': 'Apply_form created successfully',
            'apply_form': {
                'id': new_apply_form.id,
                'name': new_apply_form.name,
                'phone_number': new_apply_form.phone_number,
                'job': new_apply_form.job,
                'gender': new_apply_form.gender,
                'email': new_apply_form.email,
                'employment_states': new_apply_form.employment_states,
                'location_id': new_apply_form.location_id,
            }
        }), 201
