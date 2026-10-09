from app.exceptions import NotFoundError
from app.extensions import db
from app.models.business_client_vehicle import BusinessClientVehicle
from app.services.business_client_service import BusinessClientService


class BusinessClientVehicleService:
    """CRUD по мотоциклам клиента."""

    @staticmethod
    def list_for_client(user_id: int, client_id: int) -> list[BusinessClientVehicle]:
        client = BusinessClientService.get_by_id(user_id, client_id)
        return (
            BusinessClientVehicle.query.filter_by(business_client_id=client.id)
            .order_by(BusinessClientVehicle.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        user_id: int, client_id: int, vehicle_id: int
    ) -> BusinessClientVehicle:
        client = BusinessClientService.get_by_id(user_id, client_id)
        vehicle = db.session.get(BusinessClientVehicle, vehicle_id)
        if not vehicle or vehicle.business_client_id != client.id:
            raise NotFoundError("Мотоцикл не найден")
        return vehicle

    @staticmethod
    def create(user_id: int, client_id: int, **kwargs) -> BusinessClientVehicle:
        client = BusinessClientService.get_by_id(user_id, client_id)

        vehicle = BusinessClientVehicle(
            business_client_id=client.id,
            name=kwargs.get("name"),
            years=kwargs.get("years"),
            volume=kwargs.get("volume"),
            mileage=kwargs.get("mileage") or 0,
            vin=kwargs.get("vin"),
            license_plate=kwargs.get("license_plate"),
            color=kwargs.get("color") or "#FFFFFF",
            note=kwargs.get("note"),
        )
        db.session.add(vehicle)
        db.session.commit()
        return vehicle

    @staticmethod
    def update(
        user_id: int, client_id: int, vehicle_id: int, **updates
    ) -> BusinessClientVehicle:
        vehicle = BusinessClientVehicleService.get_by_id(user_id, client_id, vehicle_id)

        for key, value in updates.items():
            if hasattr(vehicle, key) and value is not None:
                setattr(vehicle, key, value)

        db.session.commit()
        return vehicle

    @staticmethod
    def delete(user_id: int, client_id: int, vehicle_id: int) -> None:
        vehicle = BusinessClientVehicleService.get_by_id(user_id, client_id, vehicle_id)
        db.session.delete(vehicle)
        db.session.commit()
