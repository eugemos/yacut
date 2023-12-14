class ProgramError(Exception):
    pass


class InvalidInputData(ProgramError):
    # pass
    def __init__(self, message):
        super().__init__()
        self.message = message


class ShortLinkAlreadyExists(ProgramError):
    message = 'Предложенный вариант короткой ссылки уже существует.'


class InvalidAPIUsage(ProgramError):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)
