from datetime import datetime, timezone

from app.extensions import db


class BusinessClient(db.Model):
    """
    Клиент бизнес-аккаунта.

    Может быть привязан к реальному User (если email совпал),
    либо существовать автономно.
    """

    __tablename__ = "business_clients"

    id = db.Column(db.Integer, primary_key=True)
    business_account_id = db.Column(
        db.Integer,
        db.ForeignKey("business_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), index=True)
    email = db.Column(db.String(120), index=True)
    note = db.Column(db.Text)

    linked_at = db.Column(db.DateTime)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # relationships
    business_account = db.relationship(
        "BusinessAccount",
        back_populates="clients",
    )
    user = db.relationship("User", foreign_keys=[user_id])
    vehicles = db.relationship(
        "BusinessClientVehicle",
        back_populates="client",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def to_dict(self, include_vehicles: bool = False):
        data = {
            "id": self.id,
            "business_account_id": self.business_account_id,
            "user_id": self.user_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "note": self.note,
            "is_linked": self.user is not None,
            "linked_at": self.linked_at.isoformat() if self.linked_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_vehicles:
            data["vehicles"] = [v.to_dict() for v in self.vehicles]

        return data
