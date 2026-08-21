from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.extensions import mail

def generate_verification_token(email):
    """Генерация токена для подтверждения email"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification-salt')

def verify_token(token, expiration=3600):
    """Проверка токена"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='email-verification-salt',
            max_age=expiration
        )
        return email
    except Exception:
        return None

def send_verification_email(user):
    """Отправка письма с подтверждением"""
    token = generate_verification_token(user.email)
    verification_url = url_for('auth.verify_email', token=token, _external=True)
    
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A0A0F; padding: 40px; color: #E0E0E0;">
            <div style="max-width: 500px; margin: 0 auto; background: #181824; padding: 40px; border-radius: 16px; border: 1px solid #2d2d3d;">
                <h1 style="color: #8B5CF6; font-size: 24px; margin-bottom: 20px;">MotoBind</h1>
                <h2 style="font-size: 20px; margin-bottom: 12px;">Подтвердите email</h2>
                <p style="color: #8b8b9e; margin-bottom: 24px;">Привет, {user.username}! Перейдите по ссылке ниже, чтобы подтвердить свой email.</p>
                <a href="{verification_url}" style="display: inline-block; padding: 12px 32px; background: #8B5CF6; color: #fff; border-radius: 10px; text-decoration: none; font-weight: 600;">Подтвердить</a>
                <p style="color: #5a5a72; font-size: 14px; margin-top: 24px;">Ссылка действует 1 час.</p>
                <p style="color: #5a5a72; font-size: 14px;">Если вы не регистрировались в MotoBind, просто проигнорируйте это письмо.</p>
            </div>
        </body>
    </html>
    """
    
    msg = Message(
        'Подтверждение email - MotoBind',
        recipients=[user.email],
        html=html
    )
    
    mail.send(msg)