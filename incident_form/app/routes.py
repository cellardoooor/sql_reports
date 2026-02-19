from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app
from .models import Incident
from .forms import IncidentForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    form = IncidentForm()
    return render_template('index.html', form=form)

@bp.route('/api/server-time', methods=['GET'])
def server_time():
    return jsonify({
        'datetime': datetime.now().isoformat()
    })

@bp.route('/api/incident', methods=['POST'])
def create_incident():
    # Получаем JSON данные и фильтруем null значения
    json_data = request.get_json() or {}
    filtered_data = {k: v for k, v in json_data.items() if v is not None}
    
    form = IncidentForm(data=filtered_data)
    
    if form.validate_on_submit():
        try:
            data = {
                'fio': form.fio.data,
                'event_datetime': form.event_datetime.data,
                'tag': form.tag.data,
                'validity_days': form.validity_days.data,  # Может быть None
                'event_description': form.event_description.data,
                'engineer_actions': form.engineer_actions.data
            }
            
            incident_id = Incident.create(data)
            
            current_app.logger.info(f"Incident {incident_id} created successfully")
            
            return jsonify({
                'success': True,
                'message': 'Событие успешно зарегистрировано',
                'id': incident_id
            }), 201
            
        except Exception as e:
            current_app.logger.error(f"Error creating incident: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Ошибка при сохранении в базу данных',
                'error': str(e)
            }), 500
    else:
        errors = {}
        for field_name, error_messages in form.errors.items():
            errors[field_name] = error_messages[0]
        
        return jsonify({
            'success': False,
            'message': 'Ошибка валидации',
            'errors': errors
        }), 400

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })
