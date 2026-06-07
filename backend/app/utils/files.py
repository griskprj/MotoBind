import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'
}


def allowed_file(filename):
    """ File check """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_moto_photo(file, moto_id):
    """ Save moto photo """
    if not file or not allowed_file(file.filename):
        return None

    filename = secure_filename(f"{moto_id}_{file.filename}")
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'user_moto')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    return f"user_moto/{filename}"

def delete_file(relative_path):
    """ Delete file """
    if not relative_path:
        return

    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], relative_path)
    if os.path.exists(full_path):
        os.remove(full_path)
