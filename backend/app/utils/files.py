import os
import uuid
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}


def allowed_file(filename):
    """File check"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_user_avatar(file, user_id):
    """Save user avatar"""
    if not file or not allowed_file(file.filename):
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    unique_id = str(uuid.uuid4())[:8]
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"avatar_{user_id}_{timestamp}_{unique_id}.{ext}")
    
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "avatars")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    return f"avatars/{filename}"

def save_user_avatar(file, user_id):
    """Save user avatar"""
    if not file or not allowed_file(file.filename):
        return None

    filename = secure_filename(f"avatar_{user_id}_{file.filename}")
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "avatars")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    return f"avatars/{filename}"


def delete_file(relative_path):
    """Delete file"""
    if not relative_path:
        return

    full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], relative_path)
    if os.path.exists(full_path):
        os.remove(full_path)


def get_file_url(relative_path):
    """Get full URL for file"""
    if not relative_path:
        return None
    
    base_url = current_app.config.get('BASE_URL', '')
    return f"{base_url}/uploads/{relative_path}"