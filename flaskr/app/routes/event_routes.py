from flask import Blueprint, jsonify, request
from app.models import Events , Speakers , Agenda
from app import db

event_blueprint = Blueprint('events',__name__)

@event_blueprint.route('/events' , methods = ['GET','POST'])
def get_events():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 2, type=int)
        
        search_query = request.args.get("search", "", type=str)

        query = Events.query

        if search_query:
            query = query.filter(Events.title.ilike(f"%{search_query}%"))
        
        events_paginate = query.paginate(page=page, per_page=per_page, error_out=False)        
        
        events_data = []
        
        for event in events_paginate:
            events_data.append({
                'id' : event.id,
                'title' : event.title,
                'icon' : event.icon,
                'img' : event.img,
                'subtitle' : event.subtitle,
                'date' : event.date,
                'starting_time' : event.starting_time,
                'description' : event.description,
                'user_id' : event.user_id,
                })
            
        pagination = {
            "count": events_paginate.total,
            "page": page,
            "per_page": per_page,
            "pages": events_paginate.pages,
        }
        
        return jsonify({'events' : events_data , 'pagination': pagination})
    
    elif request.method == 'POST':
        data = request.get_json()
        
        new_event = Events(
            title = data['title'], 
            icon = data['icon'], 
            img = data['img'], 
            subtitle = data['subtitle'], 
            date = data['date'], 
            starting_time = data['starting_time'], 
            description = data['description'], 
            user_id = data['user_id'], 
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return jsonify({
            'message' : 'event created successfully'
        }),201
    
@event_blueprint.route('/events/<int:event_id>', methods = ['GET','PUT','DELETE'])
def handle_event(event_id):
    event = Events.query.get_or_404(event_id)
    
    if request.method == 'GET':
        event_data = {
                'id' : event.id,
                'title' : event.title,
                'icon' : event.icon,
                'img' : event.img,
                'subtitle' : event.subtitle,
                'date' : event.date,
                'starting_time' : event.starting_time,
                'description' : event.description,
                'user_id' : event.user_id,
                'agenda' : [{
                    'title' : agenda.title,
                    'location' : agenda.location,
                    'agenda_type' : agenda.agenda_type,
                    'status' : agenda.status,
                    'starting_date' : agenda.starting_date,
                    'end_date' : agenda.end_date,
                    'keywords' : agenda.keywords,
                    }for agenda in event.agenda],
                'speakers' : [{
                    'name' : speaker.name,
                    'img' : speaker.img,
                    'Position' : speaker.Position,
                    'company_name' : speaker.company_name,
                    }for speaker in event.speakers],  
                }
        return jsonify({'event': event_data})
    
    elif request.method == 'PUT':
        data = request.get_json()
        event.title = data.get('title', event.title)
        event.icon = data.get('icon', event.icon)
        event.img = data.get('img', event.img)
        event.subtitle = data.get('subtitle', event.subtitle)
        event.date = data.get('date', event.date)
        event.starting_time = data.get('starting_time', event.starting_time)
        event.description = data.get('description', event.description)

        db.session.commit()
        return jsonify({'message': 'Event updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'})

@event_blueprint.route('/speakers' , methods =['GET','POST'])
def get_post_speakers():
    if request.method == 'GET':
        
        speaker_list = Speakers.query.all()
        speakers = []
        
        for speaker in speaker_list :
            speakers.append({
                'id' : speaker.id,
                'name' : speaker.name,
                'img' : speaker.img,
                'position' : speaker.Position,
                'company_name' : speaker.company_name,
                'event_id' : speaker.event_id,
            })
        return jsonify({'speakers' : speakers})
    
    elif request.method == 'POST' :
        data = request.get_json()
        
        new_speaker = Speakers(
            name = data['name'],
            img = data['img'],
            Position = data['position'],
            company_name = data['company_name'],
            event_id = data['event_id']
        )
        
        db.session.add(new_speaker)
        db.session.commit()
        
        return jsonify({'message' : 'speaker created successfully'}),201
    


@event_blueprint.route('/agenda' , methods =['GET','POST'])
def get_post_agenda():
    if request.method == 'GET':
        
        agenda_list = Agenda.query.all()
        agendas = []
        
        for agenda in agenda_list :
            agendas.append({
                'id' : agenda.id,
                'title' : agenda.title,
                'location' : agenda.location,
                'agenda_type' : agenda.agenda_type,
                'status' : agenda.status,
                'starting_date' : agenda.starting_date,
                'end_date' : agenda.end_date,
                'keywords' : agenda.keywords,
                'event_id' : agenda.event_id,
            })
        return jsonify({'agendas' : agendas})
    
    elif request.method == 'POST' :
        data = request.get_json()
        
        new_agenda = Agenda(
            title = data['title'],
            location = data['location'],
            agenda_type = data['agenda_type'],
            status = data['status'],
            starting_date = data['starting_date'],
            end_date = data['end_date'],
            keywords = data['keywords'],
            event_id = data['event_id']
        )
        
        db.session.add(new_agenda)
        db.session.commit()
        
        return jsonify({'message' : 'agenda created successfully'}),201
    
