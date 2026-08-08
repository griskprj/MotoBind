import os
from io import BytesIO
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}

# Конфигурация сжатия
IMAGE_QUALITY = 85  # 0-100, 85 — хороший баланс
MAX_WIDTH = 1920    # Максимальная ширина для фото мотоциклов
MAX_WIDTH_AVATAR = 500  # Максимальная ширина для аватаров
WEBP_QUALITY = 80   # Качество WebP


def allowed_file(filename):
    """File check"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def compress_image(file, max_width, quality=IMAGE_QUALITY, output_format="webp"):
    """
    Сжимает изображение и возвращает BytesIO
    output_format: 'webp' (рекомендуется) или 'jpeg'
    """
    try:
        # Открываем изображение
        img = Image.open(file)
        
        # Конвертируем в RGB (для JPEG/WebP)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Сохраняем прозрачность для WebP
            if output_format == 'webp' and img.mode in ('RGBA', 'LA'):
                pass  # WebP поддерживает прозрачность
            else:
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
        
        # Уменьшаем если ширина больше max_width
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Сохраняем в BytesIO
        output = BytesIO()
        
        if output_format == 'webp':
            # WebP — супер сжатие, поддерживает прозрачность
            img.save(output, format='WEBP', quality=quality, method=6)
        elif output_format == 'jpeg':
            # JPEG — для фото без прозрачности
            img.save(output, format='JPEG', quality=quality, optimize=True)
        else:
            # PNG — без сжатия
            img.save(output, format='PNG', optimize=True)
        
        output.seek(0)
        return output
    
    except Exception as e:
        current_app.logger.error(f"Ошибка сжатия: {e}")
        # Если сжатие не удалось — возвращаем оригинал
        file.seek(0)
        return file


def save_moto_photo(file, moto_id):
    """Save moto photo with compression"""
    if not file or not allowed_file(file.filename):
        return None

    # Сжимаем в WebP
    compressed = compress_image(
        file, 
        max_width=MAX_WIDTH, 
        quality=WEBP_QUALITY,
        output_format="webp"
    )
    
    # Имя файла — всегда .webp
    filename = secure_filename(f"{moto_id}_{file.filename}")
    filename = filename.rsplit(".", 1)[0] + ".webp"  # Меняем расширение
    
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "user_moto")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    
    # Сохраняем сжатый файл
    with open(filepath, 'wb') as f:
        f.write(compressed.getvalue())
    
    return f"user_moto/{filename}"


def save_user_avatar(file, user_id):
    """Save user avatar with compression"""
    if not file or not allowed_file(file.filename):
        return None

    # Сжимаем в WebP с меньшим размером
    compressed = compress_image(
        file,
        max_width=MAX_WIDTH_AVATAR,
        quality=WEBP_QUALITY,
        output_format="webp"
    )
    
    # Имя файла — всегда .webp
    original_filename = secure_filename(file.filename)
    filename = f"avatar_{user_id}_{original_filename}"
    filename = filename.rsplit(".", 1)[0] + ".webp"
    
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "avatars")
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    
    # Сохраняем сжатый файл
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