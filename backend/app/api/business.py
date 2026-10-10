from app.decorators import business_owner_required
from app.extensions import db
from app.schemas.booking import (
    CompleteBookingSchema,
    DeclineBookingSchema,
    RescheduleBookingSchema,
)
from app.schemas.business import (
    CreateBusinessAccountSchema,
    CreateBusinessClientSchema,
    CreateVehicleSchema,
    LinkClientToUserSchema,
    UpdateBusinessAccountSchema,
    UpdateBusinessClientSchema,
    UpdateVehicleSchema,
)
from app.services.booking_service import BookingService
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


@business.route("/catalog", methods=["GET"])
@jwt_required()
def catalog():
    """
    Публичный каталог мастеров и СТО.
    Только активные, с одобренными услугами.
    """
    from app.models.business_account import BusinessAccount
    from app.models.service import Service, ServiceStatus
    from sqlalchemy import func, or_

    search = request.args.get("search", "").strip()
    ftype = request.args.get("type") or None
    city = request.args.get("city") or None

    # Подсчёт одобренных услуг на аккаунт
    services_count_sq = (
        db.session.query(
            Service.business_account_id,
            func.count(Service.id).label("cnt"),
        )
        .filter(Service.status == ServiceStatus.APPROVED)
        .group_by(Service.business_account_id)
        .subquery()
    )

    query = db.session.query(
        BusinessAccount, func.coalesce(services_count_sq.c.cnt, 0)
    ).outerjoin(
        services_count_sq,
        services_count_sq.c.business_account_id == BusinessAccount.id,
    )

    if search:
        q = f"%{search}%"
        query = query.filter(
            or_(
                BusinessAccount.name.ilike(q),
                BusinessAccount.city.ilike(q),
            )
        )

    if ftype in ("master", "station"):
        query = query.filter(BusinessAccount.type == ftype)

    if city:
        query = query.filter(BusinessAccount.city == city)

    rows = query.order_by(BusinessAccount.name.asc()).limit(200).all()

    masters = []
    for account, cnt in rows:
        d = account.to_dict(include_owner=False)
        d["services_count"] = int(cnt or 0)
        masters.append(d)

    return jsonify({"masters": masters}), 200


@business.route("/catalog/cities", methods=["GET"])
def catalog_cities():
    """Список городов с активными мастерами."""
    from app.models.business_account import BusinessAccount

    rows = (
        db.session.query(BusinessAccount.city)
        .filter(BusinessAccount.city.isnot(None))
        .filter(BusinessAccount.city != "")
        .distinct()
        .order_by(BusinessAccount.city.asc())
        .all()
    )
    cities = [r[0] for r in rows if r[0]]
    return jsonify({"cities": cities}), 200


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


# ============================================================
# ЗАЯВКИ (СТОРОНА МАСТЕРА)
# ============================================================


@business.route("/bookings", methods=["GET"])
@jwt_required()
@business_owner_required
def list_bookings():
    """Список заявок моего бизнес-аккаунта."""
    status = request.args.get("status") or None
    records = BookingService.list_for_master(get_current_user_id(), status=status)
    return jsonify([r.to_dict(include_relations=True) for r in records]), 200


@business.route("/bookings/<int:booking_id>", methods=["GET"])
@jwt_required()
@business_owner_required
def get_booking_detail(booking_id):
    """Детали заявки."""
    record = BookingService.get_for_master(get_current_user_id(), booking_id)
    return jsonify(record.to_dict(include_relations=True)), 200


@business.route("/bookings/<int:booking_id>/confirm", methods=["POST"])
@jwt_required()
@business_owner_required
def confirm_booking(booking_id):
    record = BookingService.confirm(get_current_user_id(), booking_id)
    return jsonify(record.to_dict(include_relations=True)), 200


@business.route("/bookings/<int:booking_id>/decline", methods=["POST"])
@jwt_required()
@business_owner_required
def decline_booking(booking_id):
    data = DeclineBookingSchema.model_validate(request.get_json() or {})
    record = BookingService.decline(
        get_current_user_id(), booking_id, reason=data.reason
    )
    return jsonify(record.to_dict(include_relations=True)), 200


@business.route("/bookings/<int:booking_id>/reschedule", methods=["POST"])
@jwt_required()
@business_owner_required
def reschedule_booking(booking_id):
    data = RescheduleBookingSchema.model_validate(request.get_json() or {})
    record = BookingService.reschedule(
        get_current_user_id(), booking_id, scheduled_at=data.scheduled_at
    )
    return jsonify(record.to_dict(include_relations=True)), 200


@business.route("/bookings/<int:booking_id>/start", methods=["POST"])
@jwt_required()
@business_owner_required
def start_booking(booking_id):
    record = BookingService.start(get_current_user_id(), booking_id)
    return jsonify(record.to_dict(include_relations=True)), 200


@business.route("/bookings/<int:booking_id>/complete", methods=["POST"])
@jwt_required()
@business_owner_required
def complete_booking(booking_id):
    data = CompleteBookingSchema.model_validate(request.get_json() or {})
    record = BookingService.complete(
        master_user_id=get_current_user_id(),
        booking_id=booking_id,
        price_final=data.price_final,
        master_note=data.master_note,
    )
    return jsonify(record.to_dict(include_relations=True)), 200
