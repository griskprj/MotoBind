from sqlalchemy import func
from datetime import datetime, timezone
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.models.post import Post

class User(db.Model):
    """User model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(32), default="motorcyclist")
    status = db.Column(db.String, default="active")

    avatar = db.Column(db.String(256), nullable=True)
    location = db.Column(db.String(128), nullable=True)
    motorcycle = db.Column(db.String(128), nullable=True)
    experience = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.String(128), nullable=True)
    social_links = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login = db.Column(db.DateTime, nullable=True)

    refresh_token = db.Column(db.String(512))
    is_premium = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)

    verification_code = db.Column(db.String(6), nullable=True)
    verification_code_expires = db.Column(db.DateTime, nullable=True)

    reset_password_token = db.Column(db.String(256), nullable=True)
    reset_password_expires = db.Column(db.DateTime, nullable=True)

    email_notifications_enabled = db.Column(db.Boolean, default=True)
    email_newsletter_enabled = db.Column(db.Boolean, default=True)
    email_verification_enabled = db.Column(db.Boolean, default=True)

    reminders_mileage_enabled = db.Column(db.Boolean, default=True, nullable=False)
    reminders_maintenance_enabled = db.Column(db.Boolean, default=True, nullable=False)

    motorcycles = db.relationship(
        "Motorcycle",
        back_populates="owner",
        lazy=True,
        cascade="all, delete-orphan",
    )

    reminders = db.relationship(
        "Reminder",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    maintenances = db.relationship(
        'Maintenance', 
        back_populates='author', 
        lazy='dynamic'
    )
    notifications = db.relationship(
        'Notification', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )

    posts = db.relationship(
        'Post', 
        back_populates='author', 
        cascade='all, delete-orphan'
    )
    
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
            "last_login": self.last_login.isoformat() if self.last_login else None,
            'email_notifications_enabled': self.email_notifications_enabled,
            'email_newsletter_enabled': self.email_newsletter_enabled,
            'email_verification_enabled': self.email_verification_enabled,
            'reminders_mileage_enabled': self.reminders_mileage_enabled,
            'reminders_maintenance_enabled': self.reminders_maintenance_enabled,
        }
        
        if include_moto:
            data["motorcycles"] = [m.to_dict() for m in self.motorcycles]

        if include_stats:
            stats = db.session.query(
                func.count(Post.id).label("posts_count"),
                func.coalesce(func.sum(Post.likes_count), 0).label("likes_received"),
                func.coalesce(func.sum(Post.comments_count), 0).label("comments_received"),
            ).filter(Post.author_id == self.id).one()
            data["stats"] = {
                "posts_count": stats.posts_count,
                "likes_received": stats.likes_received,
                "comments_received": stats.comments_received
            }

        return data
