"""
Кастомные исключения для API
"""
from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from datetime import datetime
import traceback

class APIException(Exception):
    """ Базовое исключение для всех API-ошибок """
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class ValidationError(APIException):
    """ Ошибка валидации (400) """
    def __init__(self, message="Ошибка валидации", errors=None):
        super().__init__(message, status_code=400, payload={"errors": errors or {}})

class ConflictError(APIException):
    """ Конфликт (409) """
    def __init__(self, message="Конфликт данных"):
        super().__init__(message, status_code=409)

class NotFoundError(APIException):
    """ Объект не найден (404) """
    def __init__(self, message="Объект не найден"):
        super().__init__(message, status_code=404)
    
class UnauthorizedError(APIException):
    """ Не авторизован (401) """
    def __init__(self, message="Не авторизован"):
        super().__init__(message, status_code=401)

class ForbiddenError(APIException):
    """ Доступ запрещен """
    def __init__(self, message="Доступ запрещен"):
        super().__init__(message, status_code=403)

class BusinessLogicError(APIException):
    """ Ошибка бизнес-логики (422) """
    def __init__(self, message="Ошибка бизнес-логики"):
        super().__init__(message, status_code=422)


def register_error_handlers(app):
    """ Регистрирует глобальные обработчики ошибок для приложения """

    @app.errorhandler(APIException)
    def handle_api_exception(e):
        """ Обработчик кастомных исключений """
        response = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status":  e.status_code,
            "error": e.message,
            "path": request.path
        }
        return jsonify(response), e.status_code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """ Обработчик всех остальных исключений (500) """
        app.logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")

        response = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 500,
            "error": "Внутренняя ошибка сервера",
            "path": request.path
        }

        if app.config.get("DEBUG"):
            response["detail"] = str(e)
            response["traceback"] = traceback.format_exc().split("\n")
        
        return jsonify(response), 500