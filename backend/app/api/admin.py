from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.exceptions import ForbiddenError
from app.decorators import admin_required

admin = Blueprint('admin', __name__)
