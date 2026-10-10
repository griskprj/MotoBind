from app.schemas.booking import CancelBookingSchema, CreateBookingSchema
from app.services.booking_service import BookingService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

booking = Blueprint("booking", __name__)


# ============================================================
# КЛИЕНТ
# ============================================================


@booking.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    """Создать заявку на обслуживание."""
    data = CreateBookingSchema.model_validate(request.get_json() or {})

    record = BookingService.create(
        client_user_id=get_current_user_id(),
        business_account_id=data.business_account_id,
        service_id=data.service_id,
        motorcycle_id=data.motorcycle_id,
        scheduled_at=data.scheduled_at,
        client_note=data.client_note,
    )
    return jsonify(record.to_dict(include_relations=True)), 201


@booking.route("/my", methods=["GET"])
@jwt_required()
def my_bookings():
    """Мои заявки (клиент)."""
    status = request.args.get("status") or None
    records = BookingService.list_for_client(get_current_user_id(), status=status)
    return jsonify([r.to_dict(include_relations=True) for r in records]), 200


@booking.route("/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_booking(booking_id):
    """Детали моей заявки как клиента."""
    record = BookingService.get_for_client(get_current_user_id(), booking_id)
    return jsonify(record.to_dict(include_relations=True)), 200


@booking.route("/<int:booking_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_booking(booking_id):
    """Отменить заявку (клиент)."""
    data = CancelBookingSchema.model_validate(request.get_json() or {})
    record = BookingService.cancel_by_client(
        client_user_id=get_current_user_id(),
        booking_id=booking_id,
        reason=data.reason,
    )
    return jsonify(record.to_dict(include_relations=True)), 200
