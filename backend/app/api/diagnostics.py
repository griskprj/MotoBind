from app.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.extensions import db
from app.models.diagnostic_report import DiagnosticReport
from app.models.manual import Manual
from app.models.motorcycle import Motorcycle
from app.schemas.diagnostic import (
    DiagnosticReportResponseSchema,
    SaveDiagnosticReportSchema,
)
from app.schemas.manual import ManualForDiagnosticSchema
from app.utils.helpers import get_current_user_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

diagnostics = Blueprint("diagnostics", __name__)


@diagnostics.route("/reports", methods=["POST"])
@jwt_required()
def save_report():
    """Сохраняет отчёт диагностики."""
    user_id = get_current_user_id()
    data = SaveDiagnosticReportSchema.model_validate(request.get_json() or {})

    report = DiagnosticReport(
        user_id=user_id,
        motorcycle_id=data.motorcycle_id,
        mileage=data.mileage,
        locked_group=data.locked_group,
        symptoms=data.symptoms,
        answers=data.answers,
        results=[r.model_dump() for r in data.results],
    )
    db.session.add(report)
    db.session.commit()

    return (
        jsonify(DiagnosticReportResponseSchema.model_validate(report).model_dump()),
        201,
    )


@diagnostics.route("/reports", methods=["GET"])
@jwt_required()
def list_reports():
    """
    Список отчётов текущего пользователя.

    Query params:
      - motorcycle_id: фильтр по мотоциклу
      - limit: по умолчанию 20, макс 100
    """
    user_id = get_current_user_id()
    moto_id = request.args.get("motorcycle_id", type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)

    query = DiagnosticReport.query.filter_by(user_id=user_id)
    if moto_id:
        query = query.filter_by(motorcycle_id=moto_id)

    reports = query.order_by(DiagnosticReport.created_at.desc()).limit(limit).all()

    return (
        jsonify(
            [
                DiagnosticReportResponseSchema.model_validate(r).model_dump()
                for r in reports
            ]
        ),
        200,
    )


@diagnostics.route("/reports/<int:report_id>", methods=["GET"])
@jwt_required()
def get_report(report_id):
    """Один отчёт по id."""
    user_id = get_current_user_id()
    report = db.session.get(DiagnosticReport, report_id)

    if not report:
        raise NotFoundError("Отчёт не найден")
    if report.user_id != user_id:
        raise ForbiddenError("Нет доступа к отчёту")

    return (
        jsonify(DiagnosticReportResponseSchema.model_validate(report).model_dump()),
        200,
    )


@diagnostics.route("/reports/<int:report_id>", methods=["DELETE"])
@jwt_required()
def delete_report(report_id):
    """Удаление отчёта."""
    user_id = get_current_user_id()
    report = db.session.get(DiagnosticReport, report_id)

    if not report:
        raise NotFoundError("Отчёт не найден")
    if report.user_id != user_id:
        raise ForbiddenError("Нет доступа к отчёту")

    db.session.delete(report)
    db.session.commit()

    return jsonify({"message": "Отчёт удалён"}), 200


@diagnostics.route("/rules/<string:rule_id>/manuals", methods=["GET"])
@jwt_required()
def find_manuals_for_rule(rule_id):
    """
    Возвращает мануалы, подходящие под правило диагностики.

    Query params:
      - moto_id: обязательный, id мотоцикла
      - category: опциональный, узел правила (если не передан — берём из rule_id по маппингу)

    Логика поиска:
      1. approved-мануалы
      2. название мотоцикла совпадает (ilike)
      3. category совпадает
      4. сортировка: по created_at desc
    """
    user_id = get_current_user_id()
    moto_id = request.args.get("moto_id", type=int)
    category = request.args.get("category", type=str)

    if not moto_id:
        raise ValidationError("Не передан moto_id")

    moto = db.session.get(Motorcycle, moto_id)
    if not moto:
        raise NotFoundError("Мотоцикл не найден")
    if moto.owner_id != user_id:
        raise ForbiddenError("Нет доступа к мотоциклу")

    if not category:
        return jsonify([]), 200

    manuals = (
        Manual.query.filter(
            Manual.status == "approved",
            Manual.motorcycle.ilike(moto.name),
            Manual.category == category,
        )
        .order_by(Manual.created_at.desc())
        .limit(5)
        .all()
    )

    return (
        jsonify(
            [ManualForDiagnosticSchema.model_validate(m).model_dump() for m in manuals]
        ),
        200,
    )
