from app.models.user import User
from app.extensions import db
from app.exceptions import NotFoundError, ValidationError, ForbiddenError

class AdminService:
    """ Сервис для работы с админ-панелью """

    @staticmethod
    def create_user(email: str, password: str, username: str, role: str, status: str) -> User:
           ''' Создает нового пользователя '''
           if User.query.filter_by(email=email).first():
               raise ValidationError("Пользователь с таким email уже существует")
           
           if User.query.filter_by(username=username).first():
               raise ValidationError("Имя пользователя занято")
           
           user = User(email=email, username=username, role=role, status=status)
           user.set_password(password)
   
           db.session.add(user)
           db.session.commit()
   
           return user