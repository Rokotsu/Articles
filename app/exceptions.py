from fastapi import HTTPException, status


class ArticleException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ArticleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED

class ArticleCannotBeAddException(ArticleException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось добавить статью ввиду неизвестной ошибки"

class CannotAddDataToDatabase(ArticleException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Что-то не удалось"