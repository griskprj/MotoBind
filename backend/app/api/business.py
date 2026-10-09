from app.decorators import business_owner_required
from app.schemas.business import (
    CreateBusinessAccountSchema,
    CreateBusinessClientSchema,
    CreateVehicleSchema,
    LinkClientToUserSchema,
    UpdateBusinessAccountSchema,
    UpdateBusinessClientSchema,
    UpdateVehicleSchema,
)
from app.services.business_client_service import BusinessClientService
from app.services.business_client_vehicle_service import BusinessClientVehicleService
from app.services.business_service import BusinessAccountService
from app.utils.helpers import get_current_user_id
from flask import Blueprint, g, jsonify, request
from flask_jwt_extended import jwt_required

business = Blueprint("business", __name__)


# ============================================================
# БИЗНЕС-АККАУНТ
# ============================================================


@business.route("/account", methods=["POST"])
@jwt_required()
def create_account():
    """Создать бизнес-аккаунт (master или station)."""
    data = CreateBusinessAccountSchema.model_validate(request.get_json() or {})

    account = BusinessAccountService.create(
        user_id=get_current_user_id(),
        type=data.type,
        name=data.name,
        description=data.description,
        city=data.city,
        address=data.address,
        phone=data.phone,
        email=data.email,
        website=data.website,
    )
    return jsonify(account.to_dict(include_owner=True)), 201


@business.route("/account/me", methods=["GET"])
@jwt_required()
@business_owner_required
def get_my_account():
    """Мой бизнес-аккаунт."""
    return jsonify(g.business_account.to_dict(include_counts=True)), 200


@business.route("/public/<string:slug>", methods=["GET"])
def get_public_account(slug):
    """
    Публичная карточка бизнес-аккаунта. Без авторизации.
    Не отдаёт клиентов, только шапку.
    """
    account = BusinessAccountService.get_by_slug(slug)

    data = account.to_dict(include_owner=True)
    if "owner" in data:
        data["owner"].pop("id", None)

    return jsonify(data), 200


@business.route("/account/me", methods=["PUT"])
@jwt_required()
@business_owner_required
def update_my_account():
    """Обновить мой бизнес-аккаунт."""
    data = UpdateBusinessAccountSchema.model_validate(request.get_json() or {})

    account = BusinessAccountService.update(
        user_id=get_current_user_id(),
        **data.get_updates(),
    )
    return jsonify(account.to_dict()), 200


@business.route("/account/me/logo", methods=["POST"])
@jwt_required()
@business_owner_required
def upload_logo():
    if "logo" not in request.files:
        return jsonify({"error": "Файл не найден"}), 400

    file = request.files["logo"]
    if file.filename == "":
        return jsonify({"error": "Файл не выбран"}), 400

    account = BusinessAccountService.update_logo(get_current_user_id(), file)
    return jsonify(account.to_dict()), 200


@business.route("/account/me/logo", methods=["DELETE"])
@jwt_required()
@business_owner_required
def delete_logo():
    account = BusinessAccountService.delete_logo(get_current_user_id())
    return jsonify(account.to_dict()), 200


# ============================================================
# КЛИЕНТЫ
# ============================================================


@business.route("/clients", methods=["GET"])
@jwt_required()
@business_owner_required
def list_clients():
    search = request.args.get("search", "")
    clients = BusinessClientService.list_for_user(
        user_id=get_current_user_id(),
        search=search,
    )
    return jsonify([c.to_dict() for c in clients]), 200


@business.route("/clients", methods=["POST"])
@jwt_required()
@business_owner_required
def create_client():
    data = CreateBusinessClientSchema.model_validate(request.get_json() or {})

    client = BusinessClientService.create(
        user_id=get_current_user_id(),
        name=data.name,
        phone=data.phone,
        email=data.email,
        note=data.note,
    )
    return jsonify(client.to_dict()), 201


@business.route("/clients/<int:client_id>", methods=["GET"])
@jwt_required()
@business_owner_required
def get_client(client_id):
    client = BusinessClientService.get_by_id(get_current_user_id(), client_id)
    return jsonify(client.to_dict(include_vehicles=True)), 200


@business.route("/clients/<int:client_id>", methods=["PUT"])
@jwt_required()
@business_owner_required
def update_client(client_id):
    data = UpdateBusinessClientSchema.model_validate(request.get_json() or {})

    client = BusinessClientService.update(
        user_id=get_current_user_id(),
        client_id=client_id,
        **data.get_updates(),
    )
    return jsonify(client.to_dict()), 200


@business.route("/clients/<int:client_id>", methods=["DELETE"])
@jwt_required()
@business_owner_required
def delete_client(client_id):
    BusinessClientService.delete(get_current_user_id(), client_id)
    return jsonify({"message": "Клиент удалён"}), 200


# ============================================================
# МОТОЦИКЛЫ КЛИЕНТА
# ============================================================


@business.route("/clients/<int:client_id>/vehicles", methods=["GET"])
@jwt_required()
@business_owner_required
def list_vehicles(client_id):
    vehicles = BusinessClientVehicleService.list_for_client(
        user_id=get_current_user_id(),
        client_id=client_id,
    )
    return jsonify([v.to_dict() for v in vehicles]), 200


@business.route("/clients/<int:client_id>/vehicles", methods=["POST"])
@jwt_required()
@business_owner_required
def create_vehicle(client_id):
    data = CreateVehicleSchema.model_validate(request.get_json() or {})

    vehicle = BusinessClientVehicleService.create(
        user_id=get_current_user_id(),
        client_id=client_id,
        name=data.name,
        years=data.years,
        volume=data.volume,
        mileage=data.mileage,
        vin=data.vin,
        license_plate=data.license_plate,
        color=data.color,
        note=data.note,
    )
    return jsonify(vehicle.to_dict()), 201


@business.route("/clients/<int:client_id>/vehicles/<int:vehicle_id>", methods=["PUT"])
@jwt_required()
@business_owner_required
def update_vehicle(client_id, vehicle_id):
    data = UpdateVehicleSchema.model_validate(request.get_json() or {})

    vehicle = BusinessClientVehicleService.update(
        user_id=get_current_user_id(),
        client_id=client_id,
        vehicle_id=vehicle_id,
        **data.get_updates(),
    )
    return jsonify(vehicle.to_dict()), 200


@business.route(
    "/clients/<int:client_id>/vehicles/<int:vehicle_id>", methods=["DELETE"]
)
@jwt_required()
@business_owner_required
def delete_vehicle(client_id, vehicle_id):
    BusinessClientVehicleService.delete(
        user_id=get_current_user_id(),
        client_id=client_id,
        vehicle_id=vehicle_id,
    )
    return jsonify({"message": "Мотоцикл удалён"}), 200


# ============================================================
# СВЯЗЫВАНИЕ КЛИЕНТА С USER
# ============================================================


@business.route("/clients/<int:client_id>/link", methods=["POST"])
@jwt_required()
@business_owner_required
def link_client(client_id):
    """Связать клиента с реальным пользователем по email."""
    data = LinkClientToUserSchema.model_validate(request.get_json() or {})

    client = BusinessClientService.link_to_user(
        user_id=get_current_user_id(),
        client_id=client_id,
        email=data.email,
    )
    return jsonify(client.to_dict()), 200


@business.route("/clients/<int:client_id>/link", methods=["DELETE"])
@jwt_required()
@business_owner_required
def unlink_client(client_id):
    """Отвязать клиента от реального пользователя."""
    client = BusinessClientService.unlink_from_user(
        user_id=get_current_user_id(),
        client_id=client_id,
    )
    return jsonify(client.to_dict()), 200


@business.route("/my-masters", methods=["GET"])
@jwt_required()
def my_masters():
    """
    Возвращает все BusinessClient, привязанные к текущему пользователю.

    Используется на стороне клиента в гараже.
    """
    records = BusinessClientService.list_for_client_user(get_current_user_id())

    result = []
    for client_record in records:
        account = client_record.business_account
        result.append(
            {
                "client_id": client_record.id,
                "linked_at": client_record.linked_at.isoformat()
                if client_record.linked_at
                else None,
                "business": account.to_dict(include_owner=True) if account else None,
                "vehicles": [v.to_dict() for v in client_record.vehicles],
            }
        )

    return jsonify(result), 200
