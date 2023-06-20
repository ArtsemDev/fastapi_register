from fastapi import Cookie, HTTPException, status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.models import UserSession


def get_session(sessionid: str = Cookie()):
    with UserSession.session() as session:
        user_session = session.get(UserSession, sessionid)
        if user_session:
            if user_session.user:
                return user_session.user
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
