from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models.motorcycle import Motorcycle
from app.models.maintenance import PlannedMaintenance
from app.models.maintenance_node import MaintenanceNode
from app.models.user import User
from app.exceptions import NotFoundError, BusinessLogicError, ForbiddenError
from app.utils.calculate_node_health import calculate_node_health
from app.utils.check_maintenance_status import check_status

def gen_maintenance_nodes(moto_id, user_id):
    """
    Генерирует узлы обслуживания

    parametrs:
        - moto_id: ID мотоцикла
        - user_id: ID пользователя

    returns:
        - Возвращает объект список всех узлов обслуживания
    """

    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("Пользователь не найден")

    moto = Motorcycle.query.options(
        selectinload(Motorcycle.planned_maintenances),
        selectinload(Motorcycle.maintenance_nodes)
    ).get(moto_id)

    if not moto:
        raise NotFoundError("Мотоцикл не найден")

    if int(moto.owner_id) != int(user_id) and user.role != 'admin':
        raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

    planned_by_category = {}
    for pm in moto.planned_maintenances:
        category = pm.category
        if category not in planned_by_category:
            planned_by_category[category] = []
        planned_by_category[category].append(pm)
    
    result = []
    for node in moto.maintenance_nodes:
        planned_maintenances = planned_by_category.get(node.category, [])
        
        planned_maintenances_data = []
        for pm in planned_maintenances:
            planned_maintenances_data.append({
                'id': pm.id,
                'title': pm.title,
                'planned_mileage': pm.planned_mileage,
                'status': check_status(pm, moto)
            })
        
        node_health = calculate_node_health(node, planned_maintenances, moto)
        
        node_data = {
            'id': node.id,
            'title': node.title,
            'category': node.category,
            'health': node_health,
            'planned_maintenances': planned_maintenances_data,
            'maintenances_count': len(planned_maintenances_data)
        }
        result.append(node_data)
    
    return result