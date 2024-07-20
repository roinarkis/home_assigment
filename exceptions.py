class ClassNameNotFound(BaseException):
    def __init__(self, message: str):
        super().__init__(message)


class URlNotFound(BaseException):
    def __init__(self, message: str):
        super().__init__(message)
