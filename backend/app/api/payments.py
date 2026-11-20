from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import limiter
from app.services.payment_service import PaymentService
from app.utils.helpers import get_current_user_id


payments = Blueprint("payments", __name__)


@payments.route("/slots", methods=["GET"])
@jwt_required()
def get_slot_balance():
    return jsonify(PaymentService.get_slots(get_current_user_id())), 200


@payments.route("/slots/purchase", methods=["POST"])
@jwt_required()
def create_slot_purchase():
    return jsonify(PaymentService.create_slot_order(get_current_user_id())), 201


@payments.route("/slots/purchases/<int:order_id>", methods=["GET"])
@jwt_required()
def get_slot_purchase_status(order_id):
    return jsonify(
        PaymentService.get_order_status(get_current_user_id(), order_id)
    ), 200


@payments.route("/robokassa/result", methods=["GET", "POST"])
@limiter.limit("60 per minute")
def robokassa_result():
    response = PaymentService.handle_result(request.values.to_dict())
    return response, 200, {"Content-Type": "text/plain; charset=utf-8"}
