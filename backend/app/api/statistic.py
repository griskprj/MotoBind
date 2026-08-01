from app.services.statistic_service import StatisticService
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

statistic = Blueprint("statistic", __name__)


@statistic.route("/dashboard-data", methods=["GET"])
@jwt_required()
def get_dashboard_data():
    """Получить данные для дашборда"""
    user_id = get_jwt_identity()
    data = StatisticService.get_dashboard_data(user_id=user_id)
    return jsonify(data), 200


@statistic.route("/dashboard-charts", methods=["GET"])
@jwt_required()
def get_dashboard_charts():
    """Получить данные для графиков дашборда"""
    user_id = get_jwt_identity()
    data = StatisticService.get_dashboard_charts(user_id)
    return jsonify(data), 200


@statistic.route("/garage", methods=["GET"])
@jwt_required()
def get_garage_stat():
    """Получить данные для гаража"""
    user_id = get_jwt_identity()
    data = StatisticService.get_garage_stats(user_id)
    return jsonify(data), 200


@statistic.route("/garage/<int:moto_id>", methods=["GET"])
@jwt_required()
def get_moto_garage(moto_id):
    """Получить данные о мотоцикле для гаража"""
    user_id = get_jwt_identity()
    data = StatisticService.get_moto_garage_stats(moto_id, user_id)
    return jsonify(data), 200


@statistic.route("/repair", methods=["GET"])
@jwt_required()
def get_repair_stats():
    """Получить статистику для страницы ремонта"""
    user_id = get_jwt_identity()
    data = StatisticService.get_repair_stats(user_id)
    return jsonify(data), 200


@statistic.route("/maintenance", methods=["GET"])
@jwt_required()
def get_maintenance_stats():
    """Получить статистику для страницы обслуживания"""
    user_id = get_jwt_identity()
    data = StatisticService.get_maintenance_stats(user_id)
    return jsonify(data), 200


@statistic.route("/registrations-chart", methods=["GET"])
@jwt_required()
def get_registrations_chart():
    """Получить данные для графика регистраций (только для админа)"""
    user_id = get_jwt_identity()
    data = StatisticService.get_registrations_chart(user_id)
    return jsonify(data), 200
