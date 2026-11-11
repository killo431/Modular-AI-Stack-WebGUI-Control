import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .config import settings

basic = HTTPBasic()

def require_auth(credentials: HTTPBasicCredentials = Depends(basic)) -> str:
    expected_user = settings.admin_username.encode()
    expected_pass = settings.admin_password.encode()
    supplied_user = credentials.username.encode()
    supplied_pass = credentials.password.encode()
    user_ok = secrets.compare_digest(supplied_user, expected_user)
    pass_ok = bool(expected_pass) and secrets.compare_digest(supplied_pass, expected_pass)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
