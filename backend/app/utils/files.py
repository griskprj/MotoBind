import os
from io import BytesIO
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}

# Конфигурация сжатия
IMAGE_QUALITY = 85
MAX_WIDTH = 1920
MAX_WIDTH_AVATAR = 500
WEBP_QUALITY = 80

def allowed_file(filename):
    """File check"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def compress_image(file, max_width, quality=IMAGE_QUALITY, output_format="webp"):
    """
    Сжимает изображение и возвращает BytesIO
    output_format: 'webp' (рекомендуется) или 'jpeg'
    """
    try:
        img = Image.open(file)
        
        if img.mode in ('RGBA', 'LA', 'P'):
            if output_format == 'webp' and img.mode in ('RGBA', 'LA'):
                pass
            else:
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
        
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        output = BytesIO()
        
        if output_format == 'webp':
            img.save(output, format='WEBP', quality=quality, method=6)
        elif output_format == 'jpeg':
            img.save(output, format='JPEG', quality=quality, optimize=True)
        else:
            img.save(output, format='PNG', optimize=True)
        
        output.seek(0)
        return output
    
    except Exception as e:
        current_app.logger.error(f"Ошибка сжатия: {e}")
        file.seek(0)
        return file


def save_moto_photo(file, moto_id):
    """Save moto photo with compression"""
    if not file or not allowed_file(file.filename):
        return None

    compressed = compress_image(
        file, 
        max_width=MAX_WIDTH, 
        quality=WEBP_QUALITY,
        output_format="webp"
    )
    
    filename = secure_filename(f"{moto_id}_{file.filename}")
    filename = filename.rsplit(".", 1)[0] + ".webp"
    
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "user_moto")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(compressed.getvalue())
    
    return f"user_moto/{filename}"


def save_user_avatar(file, user_id):
    """Save user avatar with compression"""
    if not file or not allowed_file(file.filename):
        return None

    compressed = compress_image(
        file,
        max_width=MAX_WIDTH_AVATAR,
        quality=WEBP_QUALITY,
        output_format="webp"
    )
    
    original_filename = secure_filename(file.filename)
    filename = f"avatar_{user_id}_{original_filename}"
    filename = filename.rsplit(".", 1)[0] + ".webp"
    
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "avatars")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(compressed.getvalue())
    
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


def save_step_image(file, manual_id, step_id):
    """Save step image with compression"""
    if not file or not allowed_file(file.filename):
        return None

    compressed = compress_image(
        file, 
        max_width=MAX_WIDTH, 
        quality=WEBP_QUALITY,
        output_format="webp"
    )
    
    filename = secure_filename(f"step_{manual_id}_{step_id}_{file.filename}")
    filename = filename.rsplit(".", 1)[0] + ".webp"
    
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "manual_steps")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(compressed.getvalue())
    
    return f"manual_steps/{filename}"