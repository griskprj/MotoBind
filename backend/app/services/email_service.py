import random
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_mail import Mail, Message
from app.extensions import mail

class EmailService:
    """Сервис для работы с email"""
    
    @staticmethod
    def generate_verification_code() -> str:
        """Генерирует 6-значный код подтверждения"""
        return ''.join(random.choices('0123456789', k=6))
    
    @staticmethod
    def send_verification_email(email: str, code: str) -> bool:
        """Отправляет код подтверждения на email"""
        try:
            subject = "Подтверждение регистрации на MotoBind"
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                    .container {{ max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .header {{ text-align: center; margin-bottom: 20px; }}
                    .header h1 {{ color: #7c3aed; margin: 0; }}
                    .code {{ background: #f0f0ff; padding: 15px; text-align: center; font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #7c3aed; border-radius: 8px; margin: 20px 0; }}
                    .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; }}
                    .footer a {{ color: #7c3aed; text-decoration: none; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🏍️ MotoBind</h1>
                        <p>Добро пожаловать! Подтвердите свою регистрацию</p>
                    </div>
                    <p>Для подтверждения регистрации введите следующий код:</p>
                    <div class="code">{code}</div>
                    <p style="color: #666; font-size: 14px;">Код действителен в течение 15 минут.</p>
                    <p style="color: #999; font-size: 13px;">Если вы не регистрировались на MotoBind, проигнорируйте это письмо.</p>
                    <div class="footer">
                        <p>© 2026 MotoBind. Все права защищены.</p>
                        <p><a href="https://motobind.ru">motobind.ru</a></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    @staticmethod
    def send_password_reset_email(email: str, code: str) -> bool:
        """Отправляет код для сброса пароля"""
        try:
            subject = "Сброс пароля на MotoBind"
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                    .container {{ max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .header {{ text-align: center; margin-bottom: 20px; }}
                    .header h1 {{ color: #7c3aed; margin: 0; }}
                    .code {{ background: #f0f0ff; padding: 15px; text-align: center; font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #7c3aed; border-radius: 8px; margin: 20px 0; }}
                    .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 MotoBind</h1>
                        <p>Запрос на сброс пароля</p>
                    </div>
                    <p>Для сброса пароля введите следующий код:</p>
                    <div class="code">{code}</div>
                    <p style="color: #666; font-size: 14px;">Код действителен в течение 15 минут.</p>
                    <p style="color: #999; font-size: 13px;">Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
                    <div class="footer">
                        <p>© 2026 MotoBind. Все права защищены.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html_body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            
            mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Failed to send reset email: {e}")
            return False