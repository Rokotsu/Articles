from fastapi import APIRouter, Response

from app.exceptions import (
    CannotAddDataToDatabase,
    EmailAlreadyExistsException,
    UserAlreadyExistsException,
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.schemas import SUser, SUserAuth

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


# Регистрация юзера
@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    """
    Регистрация нового пользователя.

    Args: \n
        user_data (SUserAuth): Данные пользователя (имя пользователя, email, пароль). \n

    Raises: \n
        409: Пользователь с таким именем уже существует. \n
        409: Пользователь с таким email уже существует. \n
        500: Не удалось добавить пользователя в базу данных. \n

    Returns: \n
        str: "Зарегистрирован" Пользователь был успешно зарегистрирован. \n
    """
    existing_user = await UserDAO.find_one_or_none(username=user_data.username)
    if existing_user:
        raise UserAlreadyExistsException
    existing_email = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_email:
        raise EmailAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role="user",
    )
    if not new_user:
        raise CannotAddDataToDatabase
    return "Зарегистрирован"


# Идёт проверка по логину и паролю, а не email.
@router_auth.post("/login")
async def login_user(response: Response, user_data: SUser) -> str:
    """
    Авторизация пользователя.

    Args: \n
        response (Response): Ответ сервера. \n
        user_data (SUser): Данные пользователя (имя пользователя, пароль). \n

    Returns: \n
        str: "залогинился" Пользователь успешно авторизован. \n
    """
    user = await authenticate_user(user_data.username, user_data.password)
    access_token = create_access_token({"sub": str(user.username)})
    response.set_cookie("article_access_token", access_token, httponly=True)
    return "Залогинился"


@router_auth.post("/logout")
async def logout_user(response: Response):
    """
    Разлогинивание пользователя.

    Args: \n
        response (Response): Ответ сервера. \n

    Returns: \n
        str: "Разлогинился" Пользователь успешно разлогинился. \n
    """
    response.delete_cookie("article_access_token")
    return "Разлогинился"
