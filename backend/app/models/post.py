from datetime import datetime
from app.extensions import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), nullable=True)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship('User', backref='posts_authored')
    likes = db.relationship('PostLike', backref='post', cascade='all, delete-orphan')
    comments = db.relationship('PostComment', backref='post', cascade='all, delete-orphan')

    def to_dict(self, include_comments=False):
        result = {
            'id': self.id,
            'author_id': self.author_id,
            'author': self.author.username if self.author else None,
            'author_avatar': self.author.avatar if self.author else None,
            'content': self.content,
            'image': self.image,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
        }
        
        if include_comments:
            result['comments'] = [c.to_dict() for c in self.comments[:5]]
        
        return result