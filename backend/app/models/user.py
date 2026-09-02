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
    location = db.Column(db.String(128), nullable=True)
    motorcycle = db.Column(db.String(128), nullable=True)
    experience = db.Column(db.String(20), nullable=True)
    social_links = db.Column(db.JSON, nullable=True)
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
    last_login = db.Column(db.DateTime, nullable=True)

    verification_code = db.Column(db.String(6), nullable=True)
    verification_code_expires = db.Column(db.DateTime, nullable=True)

    reset_password_token = db.Column(db.String(256), nullable=True)
    reset_password_expires = db.Column(db.DateTime, nullable=True)

    motorcycles = db.relationship(
        "Motorcycle",
        backref="motorcycle_owner",
        lazy=True,
        cascade="all, delete-orphan",
    )

    maintenances = db.relationship('Maintenance', back_populates='author', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan')  
    posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set hash password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password, password)

    def to_dict(self, include_moto: bool = False, include_stats: bool = False):
        """Serialize user data to JSON"""
        data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "bio": self.bio,
            "location": self.location,
            "motorcycle": self.motorcycle,
            "experience": self.experience,
            "social_links": self.social_links,
            "avatar": self.avatar,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
        if include_moto:
            data["motorcycles"] = [m.to_dict() for m in self.motorcycles]

        if include_stats:
            data['stats'] = {
                'posts_count': len(self.posts) if hasattr(self, 'posts') else 0,
                'likes_received': sum(p.likes_count for p in self.posts) if hasattr(self,' posts') else 0,
                'comments_received': sum(p.comments_count for p in self.posts) if hasattr(self,' posts') else 0,
            }

        return data
