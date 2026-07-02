from app.utils.check_maintenance_status import check_status

def calculate_node_health(node, planned_maintenances, moto):
    """
    Комбинированный подход: учитывает и просроченные, и ближайшие обслуживания
    """
    if not planned_maintenances:
        return 100
    
    total = len(planned_maintenances)
    overdue = 0
    soon = 0
    
    for pm in planned_maintenances:
        status = check_status(pm, moto)
        if status == 'overdue':
            overdue += 1
        elif status == 'soon':
            soon += 1
    
    if total == 0:
        return 100
    
    health = 100 - (overdue / total) * 100 * 0.8
    
    health -= (soon / total) * 100 * 0.2
    
    if not moto.mileage:
        health -= 10
    
    return round(max(0, min(100, health)), 1)