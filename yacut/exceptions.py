class ProgramError(Exception):
    """Базовый класс всех собственных исключений программы."""
    pass


class InvalidInputData(ProgramError):
    """Возникает при валидации входных данных."""
    def __init__(self, message):
        super().__init__()
        self.message = message


class ShortLinkAlreadyExists(ProgramError):
    """Возникает, когда предложенный пользователем вариант короткой ссылки
    уже существует.
    """
    message = 'Предложенный вариант короткой ссылки уже существует.'


class InvalidAPIUsage(ProgramError):
    """Возникает, когда какие-либо ошибки возникают при обращении к API."""
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)
