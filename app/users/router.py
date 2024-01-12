from fastapi import APIRouter, Depends, Response

from app.exceptions import (
    CannotAddDataToDatabase,
    UserAlreadyExistsException
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current