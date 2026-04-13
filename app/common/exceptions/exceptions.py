class LoginError(Exception):
    """Ошибка авторизации"""

    pass


class NotFoundError(Exception):
    """Объект не найден"""

    pass


class AlreadyExistsError(Exception):
    """Ошибка наличествования"""

    pass


class ConflictError(Exception):
    """Конфликт запроса"""

    pass
