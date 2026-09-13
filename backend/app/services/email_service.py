import random
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_mail import Mail, Message
from threading import Thread
from app.extensions import mail

class EmailService:
    """Сервис для работы с email"""
    
    @staticmethod
    def generate_verification_code() -> str:
        """Генерирует 6-значный код подтверждения"""
        return ''.join(random.choices('0123456789', k=6))

    @staticmethod
    def can_send_email(user, email_type='newsletter'):
        """
        Проверяет, можно ли отправить email пользователю
        email_type: 'newsletter', 'verification', 'notification'
        """
        if not user or not user.email:
            return False

        if not user.email_notifications_enabled:
            return False

        if email_type == 'newsletter' and not user.email_newsletter_enabled:
            return False
        if email_type == 'verification' and not user.email_verification_enabled:
            return False

        return True
    
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


    @staticmethod
    def send_bulk_email(app, recipients: list, subject: str, html_body: str, 
                         sender: str = None) -> dict:
        """
        Отправка массовой рассылки асинхронно
        """
        if not recipients:
            return {"success": False, "error": "Нет получателей"}

        from app.models.user import User
        with app.app_context():
            subscribed_users = User.query.filter(
                User.email.in_(recipients),
                User.email_newsletter_enabled == True,
                User.email_notifications_enabled == True
            ).all()

            subscribed_email = [u.email for u in subscribed_users]

            if not subscribed_users:
                return {
                    "success": False,
                    "error": "Нет подписанных пользователей",
                    "total": len(recipients),
                    "subscribed": 0
                }
        
        thread = Thread(
            target=EmailService._send_bulk_email_thread,
            args=(app, recipients, subject, html_body, sender)
        )
        thread.daemon = True
        thread.start()
        
        return {
            "success": True, 
            "message": f"Рассылка запущена для {len(recipients)} получателей",
            "total": len(recipients)
        }
    
    @staticmethod
    def _send_bulk_email_thread(app, recipients: list, subject: str, html_body: str, 
                                 sender: str = None):
        """Фоновый поток для отправки писем с контекстом приложения"""
        with app.app_context():
            success_count = 0
            failed_count = 0
            failed_emails = []

            from itsdangerous import URLSafeTimedSerializer
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

            for i, email in enumerate(recipients):
                try:
                    token = serializer.dumps(email, salt='unsubscribe')
                    unsubscribe_url = f"{app.config.get('FRONTEND_URL')}/unsubscribe/{token}"

                    final_html = html_body.replace(
                        '</body>',
                        f'''
                        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                            <p style="color: #999; font-size: 12px;">
                                Вы получили это письмо, потому что подписаны на рассылку MotoBind.
                                <br>
                                <a href="{unsubscribe_url}" style="color: #7c3aed; text-decoration: underline;">
                                    Отписаться от рассылки
                                </a>
                            </p>
                        </div>
                        </body>
                        '''
                    )

                    msg = Message(
                        subject=subject,
                        recipients=[email],
                        html=final_html,
                        sender=sender or app.config.get('MAIL_DEFAULT_SENDER')
                    )
                    mail.send(msg)
                    success_count += 1

                except Exception as e:
                    failed_count += 1
                    failed_emails.append(email)
            
            for email in recipients:
                try:
                    msg = Message(
                        subject=subject,
                        recipients=[email],
                        html=html_body,
                        sender=sender or app.config.get('MAIL_DEFAULT_SENDER')
                    )
                    mail.send(msg)
                    success_count += 1
                    print(f"✅ Sent to {email}")
                except Exception as e:
                    failed_count += 1
                    failed_emails.append(email)
                    print(f"❌ Failed to send to {email}: {e}")
            
            print(f"Bulk email completed: {success_count} sent, {failed_count} failed")
            
            return {"success": success_count, "failed": failed_count, "failed_emails": failed_emails}



    @staticmethod
    def can_send_reminder(user, reminder_type: str) -> bool:
        """
        Проверяет, можно ли отправить reminder-письмо.
        Учитывает глобальный email_* и под-флаги reminders_*.
        """
        if not user or not user.email:
            return False

        if not user.email_notifications_enabled:
            return False

        from app.models.reminder import Reminder
        if reminder_type == Reminder.TYPE_MILEAGE_UPDATE:
            if not user.reminders_mileage_enabled:
                return False
        elif reminder_type in (
            Reminder.TYPE_MAINTENANCE_SOON,
            Reminder.TYPE_MAINTENANCE_OVERDUE,
        ):
            if not user.reminders_maintenance_enabled:
                return False

        return True

    @staticmethod
    def send_reminder_email(user, reminder) -> bool:
        """
        Отправляет email-напоминание пользователю.

        user     — User
        reminder — Reminder

        Возвращает True при успехе, False при любой ошибке.
        Ошибки логирует, не бросает — чтобы cron шёл дальше.
        """
        try:
            moto = reminder.motorcycle
            if not moto:
                print(f"[EmailService] reminder {reminder.id} has no motorcycle")
                return False

            from app.models.reminder import Reminder

            if reminder.type == Reminder.TYPE_MILEAGE_UPDATE:
                subject, html = EmailService._render_mileage_update(user, reminder, moto)
            elif reminder.type == Reminder.TYPE_MAINTENANCE_SOON:
                subject, html = EmailService._render_maintenance_soon(user, reminder, moto)
            elif reminder.type == Reminder.TYPE_MAINTENANCE_OVERDUE:
                subject, html = EmailService._render_maintenance_overdue(user, reminder, moto)
            else:
                print(f"[EmailService] unknown reminder type: {reminder.type}")
                return False

            msg = Message(
                subject=subject,
                recipients=[user.email],
                html=html,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            )
            mail.send(msg)
            return True

        except Exception as e:
            print(f"[EmailService] Failed to send reminder to {getattr(user, 'email', '?')}: {e}")
            return False

    # ========================================================
    # ШАБЛОНЫ ПИСЕМ (приватные)
    # ========================================================

    @staticmethod
    def _render_mileage_update(user, reminder, moto) -> tuple[str, str]:
        """Письмо: 'обнови пробег'."""
        subject = f"🏍️ Обновите пробег для {moto.name}"

        from datetime import datetime, timezone
        last = moto.mileage_updated_at or moto.updated_at or moto.created_at
        if last is not None and last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - last).days if last else 0

        content = f"""
        <h2 style="color: #0F172A; margin: 0 0 12px;">Привет, {user.username}!</h2>
        <p style="color: #334155; font-size: 15px; line-height: 1.6;">
            Похоже, вы давно не обновляли пробег для <strong>{moto.name}</strong>.
            Последнее обновление было <strong>{days} дн. назад</strong>.
        </p>
        <p style="color: #334155; font-size: 15px; line-height: 1.6;">
            Свежий пробег помогает нам точнее напоминать о предстоящем ТО
            и не пропустить важное обслуживание.
        </p>
        <div style="background: #F0F0FF; padding: 14px 18px; border-radius: 10px; margin: 16px 0;">
            <div style="color: #64748B; font-size: 13px;">Текущий пробег в системе</div>
            <div style="color: #7C3AED; font-size: 22px; font-weight: 700; margin-top: 4px;">
                {moto.mileage or 0} км
            </div>
        </div>
        """

        cta_text = "Обновить пробег"
        cta_url = f"{EmailService._frontend_url()}/garage"

        return subject, EmailService._wrap_email(content, cta_text, cta_url)

    @staticmethod
    def _render_maintenance_soon(user, reminder, moto) -> tuple[str, str]:
        """Письмо: 'скоро ТО'."""
        maint = reminder.maintenance
        if not maint:
            return EmailService._render_mileage_update(user, reminder, moto)

        current = moto.mileage or 0
        km_left = max(0, (maint.planned_mileage or 0) - current)

        subject = f"🔧 Через {km_left} км — {maint.title}"

        content = f"""
        <h2 style="color: #0F172A; margin: 0 0 12px;">Привет, {user.username}!</h2>
        <p style="color: #334155; font-size: 15px; line-height: 1.6;">
            Для вашего <strong>{moto.name}</strong> приближается обслуживание:
        </p>
        <div style="background: #FFF7E6; border-left: 4px solid #F59E0B; padding: 14px 18px; border-radius: 8px; margin: 16px 0;">
            <div style="color: #0F172A; font-weight: 600; font-size: 16px;">{maint.title}</div>
            <div style="color: #64748B; font-size: 13px; margin-top: 6px;">
                Запланировано на <strong>{maint.planned_mileage} км</strong>
            </div>
        </div>
        <p style="color: #334155; font-size: 15px; line-height: 1.6;">
            Осталось проехать примерно <strong style="color: #F59E0B;">{km_left} км</strong>.
            Самое время записаться в сервис или подготовить запчасти.
        </p>
        """

        cta_text = "Перейти к обслуживанию"
        cta_url = f"{EmailService._frontend_url()}/maintenance"

        return subject, EmailService._wrap_email(content, cta_text, cta_url)

    @staticmethod
    def _render_maintenance_overdue(user, reminder, moto) -> tuple[str, str]:
        """Письмо: 'ТО просрочено'."""
        maint = reminder.maintenance
        if not maint:
            return EmailService._render_mileage_update(user, reminder, moto)

        current = moto.mileage or 0
        km_overdue = max(0, current - (maint.planned_mileage or 0))

        subject = f"⚠️ Просрочено ТО: {maint.title}"

        content = f"""
        <h2 style="color: #0F172A; margin: 0 0 12px;">Привет, {user.username}!</h2>
        <p style="color: #334155; font-size: 15px; line-height: 1.6;">
            Для вашего <strong>{moto.name}</strong> просрочено обслуживание:
        </p>
        <div style="background: #FEF2F2; border-left: 4px solid #EF4444; padding: 14px 18px; border-radius: 8px; margin: 16px 0;">
            <div style="color: #0F172A; font-weight: 600; font-size: 16px;">{maint.title}</div>
            <div style="color: #64748B; font-size: 13px; margin-top: 6px;">
                Планировалось на <strong>{maint.planned_mileage} км</strong>
            </div>
            <div style="color: #EF4444; font-weight: 600; font-size: 14px; margin-top: 8px;">
                Просрочено на ~{km_overdue} км
            </div>
        </div>
        <p style="color: #334155; font-size: 15px; line-height: 1.6;">
            Рекомендуем не откладывать — регулярное обслуживание продлевает
            жизнь мотоциклу и бережёт ваш бюджет в долгосрочной перспективе.
        </p>
        """

        cta_text = "Отметить как выполнено"
        cta_url = f"{EmailService._frontend_url()}/maintenance"

        return subject, EmailService._wrap_email(content, cta_text, cta_url)

    # ========================================================
    # ОБЩИЙ КАРКАС ПИСЬМА
    # ========================================================

    @staticmethod
    def _frontend_url() -> str:
        """URL фронта для ссылок в письме."""
        return current_app.config.get('FRONTEND_URL')

    @staticmethod
    def _wrap_email(content_html: str, cta_text: str = None, cta_url: str = None, hint_html: str = None) -> str:
        """
        Оборачивает контент в общий каркас: лого, контейнер, кнопка CTA, футер.
        """
        cta_block = ""
        if cta_text and cta_url:
            cta_block = f"""
            <div style="text-align: center; margin: 24px 0 8px;">
                <a href="{cta_url}"
                   style="display: inline-block; background: #7C3AED; color: #fff;
                          text-decoration: none; padding: 12px 28px; border-radius: 10px;
                          font-weight: 600; font-size: 15px;">
                    {cta_text}
                </a>
            </div>
            """

        hint_block = ""
        if hint_html:
            hint_block = f"""
            <p style="color: #94A3B8; font-size: 13px; text-align: center; margin: 12px 0 0;">
                {hint_html}
            </p>
            """

        return f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background: #F1F5F9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;">
            <div style="max-width: 520px; margin: 0 auto; padding: 24px 16px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="color: #7C3AED; font-size: 22px; font-weight: 700;">🏍️ MotoBind</div>
                </div>
                <div style="background: #FFFFFF; padding: 28px 26px; border-radius: 14px; box-shadow: 0 2px 12px rgba(15,23,42,0.06);">
                    {content_html}
                    {cta_block}
                    {hint_block}
                </div>
                <div style="text-align: center; color: #94A3B8; font-size: 12px; margin-top: 20px; line-height: 1.7;">
                    <p style="margin: 4px 0;">
                        Вы получаете это письмо, потому что включили напоминания в MotoBind.
                    </p>
                    <p style="margin: 4px 0;">
                        Отключить можно в
                        <a href="{EmailService._frontend_url()}/profile"
                           style="color: #7C3AED; text-decoration: underline;">настройках профиля</a>.
                    </p>
                    <p style="margin: 12px 0 0;">© 2026 MotoBind</p>
                </div>
            </div>
        </body>
        </html>
        """