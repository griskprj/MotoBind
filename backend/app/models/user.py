from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    bio = db.Column(db.String(128), nullable=True)
    avatar = db.Column(db.String(256), nullable=True)
    role = db.Column(
        db.String(32), default="motorcyclist"
    )  # motorcyclist, admin, motoclub
    refresh_token = db.Column(db.String(512))
    status = db.Column(db.String, default="active")
    is_premium = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    verification_code = db.Column(db.String(6), nullable=True)
    verification_code_expires = db.Column(db.DateTime, nullable=True)

    motorcycles = db.relationship(
        "Motorcycle",
        backref="motorcycle_owner",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def set_password(self, password):
        """Set hash password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password, password)

    def to_dict(self, include_moto: bool = False):
        """Serialize user data to JSON"""
        data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "bio": self.bio,
            "avatar": self.avatar,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_moto:
            data["motorcycles"] = [m.to_dict() for m in self.motorcycles]

        return data
