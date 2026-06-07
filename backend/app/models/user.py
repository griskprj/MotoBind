from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    """ User model """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(32), default='motorcyclist') # motorcyclist, admin, motoclub
    refresh_token = db.Column(db.String(512))

    motorcycles = db.relationship('Motorcycle', backref='motorcycle_owner', lazy='dynamic', cascade='all, delete-orphan')


    def set_password(self, password):
        """ Set hash password """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ Check password """
        return check_password_hash(self.password, password)

    def to_dict(self, include_moto: bool = False):
        """ Serialize user data to JSON """
        data = {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'role': self.role
        }
        if include_moto:
            data['motorcycles'] = [m.to_dict() for m in self.motorcycles]
        
        return data