from uuid import uuid4

from fastapi import Form, BackgroundTasks, Path, HTTPException, Depends, Cookie
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from .router import router
from ..dependencies import get_session
from ..models import User, UserSession, UserEmailVerify
from ..settings import templating, pwd_context
from ..utils.email import send_message


@router.get('/register', name='register')
async def register(request: Request):
    return templating.TemplateResponse(
        'auth/register.html',
        {
            'request': request
        }
    )


@router.post('/register')
async def register(
        request: Request,
        background_task: BackgroundTasks,
        email: str = Form(),
        password: str = Form()
):
    with User.session() as session:
        user = User(email=email, password=pwd_context.hash(password))
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            return templating.TemplateResponse(
                'auth/register.html',
                {
                    'request': request,
                    'error': 'Email is not unique'
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )
        else:
            session.refresh(user)
    with UserEmailVerify.session() as session:
        user_session = UserEmailVerify(id=str(uuid4()), user_id=user.id)
        session.add(user_session)
        session.commit()
        session.refresh(user_session)
    background_task.add_task(
        send_message,
        f'http://127.0.0.1:8000/verify/{user_session.id}',
        user.email,
    )
    return templating.TemplateResponse(
        'auth/register.html',
        {
            'request': request,
        },
    )


@router.get('/verify/{pk}')
async def verify(pk: str = Path()):
    with UserEmailVerify.session() as session:
        user = session.get(UserEmailVerify, pk)
        if user:
            user.user.is_active = True
            session.delete(user)
            session.commit()
            return RedirectResponse('/login')
        raise HTTPException(400)


@router.get('/login', name='login')
async def login(request: Request):
    return templating.TemplateResponse('auth/login.html', {'request': request})


@router.post('/login')
async def login(
        request: Request,
        response: Response,
        email: str = Form(),
        password: str = Form()
):
    with User.session() as session:
        user = session.scalar(select(User).filter_by(email=email))
        if user and user.is_active:
            if pwd_context.verify(password, user.password):
                user_session = UserSession(id=str(uuid4()), user_id=user.id)
                session.add(user_session)
                session.commit()
                session.refresh(user_session)
                response.set_cookie('sessionid', user_session.id)
                return RedirectResponse('/profile', headers=response.headers)
            return templating.TemplateResponse('auth/login.html', {'request': request}, status_code=401)
        return templating.TemplateResponse('auth/login.html', {'request': request}, status_code=401)


@router.get('/profile', name='profile')
@router.post('/profile')
async def profile(request: Request, user: User = Depends(get_session)):
    return templating.TemplateResponse('auth/profile.html', {'request': request})


@router.get('/logout')
async def logout(sessionid: str = Cookie()):
    with UserSession.session() as session:
        session.execute(delete(UserSession).filter_by(id=sessionid))
        session.commit()
    return RedirectResponse('/login')
