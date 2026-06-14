from datetime import datetime, timezone
from app.extensions import db
from app.models.motorcycle import Motorcycle
from app.models.maintenance import PlannedMaintenance

def check_status(maintenance_id, moto_id):
    motorcycle = Motorcycle.query.get(moto_id)
    if not motorcycle:
        return 'Мотоцикл не найден'
    
    maintenance = PlannedMaintenance.query.get(maintenance_id)
    
    if maintenance.planned_mileage:
        dif = maintenance.planned_mileage - motorcycle.mileage
        if dif <= 0:
            maintenance.status = 'overdue'
        if 0 < dif <= 200:
            maintenance.status = 'pending'

    db.session.commit()

    return maintenance.to_dict()