import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

app = Flask(__name__)

# Настройки почты (явно прописываем)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.yandex.ru')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True') == 'True'
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'motobind@yandex.ru')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'motobind@yandex.ru')

print("📧 Настройки почты:")
print(f"  Server: {app.config['MAIL_SERVER']}")
print(f"  Port: {app.config['MAIL_PORT']}")
print(f"  SSL: {app.config['MAIL_USE_SSL']}")
print(f"  TLS: {app.config['MAIL_USE_TLS']}")
print(f"  Username: {app.config['MAIL_USERNAME']}")
print(f"  Password: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else '❌ НЕ УСТАНОВЛЕН!'}")
print()

mail = Mail(app)

with app.app_context():
    try:
        msg = Message(
            'Тестовое письмо от MotoBind',
            recipients=['grisky@icloud.com'],  # Замени на свой email
            body='Привет! Это тестовое письмо для проверки SMTP. Если ты это читаешь — всё работает! 🎉'
        )
        mail.send(msg)
        print('✅ Письмо отправлено!')
    except Exception as e:
        print(f'❌ Ошибка: {e}')