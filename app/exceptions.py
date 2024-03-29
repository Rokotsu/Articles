from fastapi import HTTPException, status


class ArticleException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ArticleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class EmailAlreadyExistsException(ArticleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Почта уже существует"


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
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить статью ввиду неизвестной ошибки"


class CannotAddDataToDatabase(ArticleException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Что-то не удалось"


class TitleAlreadyExistsException(ArticleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Заголовок уже существует"


class CannotDeleteArticleException(ArticleException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Вы не можете удалить статью"


class CannotFindArticleException(ArticleException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет такой статьи"


class ArticleCannotBeEditException(ArticleException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = "Не удалось обновить ошибку"


class CannotChangeArticleException(ArticleException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    detail = "Не удалось поменять статью"


class CannotFindAuthorException(ArticleException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет такого автора"


class CannotFindDateException(ArticleException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет публикаций по такой дате"
