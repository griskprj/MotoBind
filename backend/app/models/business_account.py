from datetime import datetime, timezone

from app.extensions import db


class BusinessType:
    """Тип бизнес-аккаунта."""

    MASTER = "master"
    STATION = "station"


class BusinessAccount(db.Model):
    """
    Бизнес-аккаунт: частный мастер или СТО.

    Один пользователь — один бизнес-аккаунт.
    """

    __tablename__ = "business_accounts"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    type = db.Column(
        db.String(16),
        nullable=False,
        default=BusinessType.MASTER,
        index=True,
    )

    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)

    logo_url = db.Column(db.String(256))

    city = db.Column(db.String(64), index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(256))

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
    owner = db.relationship("User", foreign_keys=[owner_id])
    clients = db.relationship(
        "BusinessClient",
        back_populates="business_account",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def to_dict(self, include_owner: bool = False, include_counts: bool = False):
        data = {
            "id": self.id,
            "owner_id": self.owner_id,
            "type": self.type,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "logo_url": self.logo_url,
            "city": self.city,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_owner and self.owner:
            data["owner"] = {
                "id": self.owner.id,
                "username": self.owner.username,
                "avatar": self.owner.avatar,
            }

        if include_counts:
            data["clients_count"] = len(self.clients) if self.clients else 0

        return data
