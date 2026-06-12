from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from app.extensions import db
from app.models.user import User
from app.models.motorcycle import Motorcycle


statistic = Blueprint('statistic', __name__)


@statistic.route('/dashboard-data')
@jwt_required()
def get_data():
    """ Get data for dashobard (user, motorcycle, pending maintenance) """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    motorcycle = [m.to_dict(include_planned_maintenance=True) for m in user.motorcycles]
    planned_maintenances = []

    for moto in motorcycle:
        maintenances = [record.to_dict() for record in moto['planned_maintenances']]
        if len(maintenances) > 0:
            planned_maintenances.append(maintenances)

    return jsonify({
        'user': user.to_dict(),
        'motorcycles': motorcycle,
        'maintenance': planned_maintenances
    })
